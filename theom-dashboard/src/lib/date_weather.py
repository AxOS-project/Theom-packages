from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCalendarWidget, QFrame, QApplication
from PyQt6.QtCore import QTimer, QDateTime, Qt, QThread, pyqtSignal, QObject, QRunnable, QThreadPool
from PyQt6.QtGui import QColor, QTextCharFormat

from astral import LocationInfo
from astral.sun import sun
from datetime import datetime
from detect_theme import current_theme
import pytz
import asyncio
import aiohttp
import sys


class Calendar(QCalendarWidget):
    def __init__(self):
        super().__init__()
        self.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)

        base_format = QTextCharFormat()

        theme_output = current_theme()

        if theme_output == "dark":
            # only give these colors in dark theme because they blend too much with white.
            base_format.setBackground(QColor("#1f1f1f"))
            base_format.setForeground(QColor("#e0e0e0"))

        for day in (Qt.DayOfWeek.Monday, Qt.DayOfWeek.Tuesday, Qt.DayOfWeek.Wednesday,
                    Qt.DayOfWeek.Thursday, Qt.DayOfWeek.Friday):
            self.setWeekdayTextFormat(day, base_format)

        weekend_format = QTextCharFormat()
        weekend_format.setBackground(QColor("#2e2e2e"))
        weekend_format.setForeground(QColor("#ff6f61"))
        self.setWeekdayTextFormat(Qt.DayOfWeek.Saturday, weekend_format)
        self.setWeekdayTextFormat(Qt.DayOfWeek.Sunday, weekend_format)


class LocationFetcher(QObject):
    location_ready = pyqtSignal(object)

    def fetch(self):
        asyncio.run(self._async_fetch())

    async def _async_fetch(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://ipinfo.io/json", timeout=5) as resp:
                    data = await resp.json()

                    loc = data.get("loc", "")
                    lat, lon = map(float, loc.split(","))
                    timezone = data.get("timezone", "Europe/London")
                    city = data.get("city", "Unknown")
                    region = data.get("region", "")

                    location = LocationInfo(
                        name=city,
                        region=region,
                        timezone=timezone,
                        latitude=lat,
                        longitude=lon
                    )

                    self.location_ready.emit(location)
        except Exception as e:
            print("⚠️ Internet/location error:", e)
            fallback = LocationInfo("London", "England", "Europe/London", 51.5074, -0.1278)
            self.location_ready.emit(fallback)


class WeatherFetchRunnable(QRunnable):
    def __init__(self, city, update_signal):
        super().__init__()
        self.city = city
        self.update_signal = update_signal

    def run(self):
        asyncio.run(self.async_fetch())

    async def async_fetch(self):
        lat = self.city.latitude
        lon = self.city.longitude
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as response:
                    data = await response.json()
                    weather = data.get("current_weather", {})

                    temp = weather.get("temperature")
                    windspeed = weather.get("windspeed")
                    condition = "N/A"
                    if temp is not None:
                        if temp > 25:
                            condition = "Sunny"
                        elif temp > 15:
                            condition = "Cloudy"
                        else:
                            condition = "Cold"

                    weather_text = f"🌤️ Weather: {condition}, {temp}°C, Wind {windspeed} km/h"

                    # Emit signal to update UI safely
                    self.update_signal.emit(weather_text)
        except Exception as e:
            self.update_signal.emit("🌤️ Weather: Internet error")
            print("Error fetching weather:", e)


class DateWeatherWidget(QWidget):
    weather_updated = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        container = QFrame()
        container.setFrameShape(QFrame.Shape.StyledPanel)

        layout = QVBoxLayout(container)
        layout.setSpacing(10)

        title = QLabel("Date & Weather")
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.calendar = Calendar()
        layout.addWidget(self.calendar)

        self.time_label = QLabel()
        self.time_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-bottom: 20px")
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.time_label)

        self.weather_container = QFrame()
        self.weather_container.setFrameShape(QFrame.Shape.StyledPanel)
        self.weather_container.setObjectName("WeatherBox")
        #self.weather_container.setStyleSheet("background-color: #333333; border-radius: 8px; padding: 10px;")
        weather_layout = QVBoxLayout(self.weather_container)

        self.weather_label = QLabel("🌤️ Weather: Loading...")
        self.weather_label.setWordWrap(True)
        self.weather_label.setStyleSheet("font-size: 14px; background-color: transparent")
        weather_layout.addWidget(self.weather_label)
        layout.addWidget(self.weather_container)

        self.sun_container = QFrame()
        self.sun_container.setFrameShape(QFrame.Shape.StyledPanel)
        self.sun_container.setObjectName("SunBox")
        #self.sun_container.setStyleSheet("background-color: #333333; border-radius: 8px; padding: 10px;")
        sun_layout = QVBoxLayout(self.sun_container)

        self.sunrise_label = QLabel("🌅 Sunrise: Loading...")
        self.sunrise_label.setStyleSheet("font-size: 14px; background-color: transparent;")
        sun_layout.addWidget(self.sunrise_label)

        self.sunset_label = QLabel("🌇 Sunset: Loading...")
        self.sunset_label.setStyleSheet("font-size: 14px; background-color: transparent;")
        sun_layout.addWidget(self.sunset_label)

        layout.addWidget(self.sun_container)

        self.city = None
        self.setup_location_fetching()

        self.time_timer = QTimer(self)
        self.time_timer.timeout.connect(self.update_time)
        self.time_timer.start(1000)

        self.weather_updated.connect(self.weather_label.setText)

        outer_layout = QVBoxLayout(self)
        outer_layout.addWidget(container)

    def setup_location_fetching(self):
        self.fetcher = LocationFetcher()
        self.fetcher_thread = QThread()
        self.fetcher.moveToThread(self.fetcher_thread)
        self.fetcher.location_ready.connect(self.set_location)
        self.fetcher_thread.started.connect(self.fetcher.fetch)
        self.fetcher_thread.start()

    def set_location(self, location):
        self.city = location
        self.update_weather()
        self.update_sun_times()

        self.weather_timer = QTimer(self)
        self.weather_timer.timeout.connect(self.update_weather)
        self.weather_timer.start(60000)

        self.sun_timer = QTimer(self)
        self.sun_timer.timeout.connect(self.update_sun_times)
        self.sun_timer.start(3600000)

    def update_time(self):
        current = QDateTime.currentDateTime()
        self.time_label.setText(current.toString("ddd MMM dd  hh:mm:ss"))

    def update_weather(self):
        if self.city is None:
            return
        runnable = WeatherFetchRunnable(self.city, self.weather_updated)
        QThreadPool.globalInstance().start(runnable)

    def update_sun_times(self):
        if self.city is None:
            return
        try:
            s = sun(self.city.observer, date=datetime.now(pytz.timezone(self.city.timezone)))
            sunrise = s['sunrise'].astimezone(pytz.timezone(self.city.timezone)).strftime('%H:%M')
            sunset = s['sunset'].astimezone(pytz.timezone(self.city.timezone)).strftime('%H:%M')
            self.sunrise_label.setText(f"🌅 Sunrise: {sunrise}")
            self.sunset_label.setText(f"🌇 Sunset: {sunset}")
        except Exception as e:
            self.sunrise_label.setText("🌅 Sunrise: Error")
            self.sunset_label.setText("🌇 Sunset: Error")
            print("Error getting sun times:", e)
