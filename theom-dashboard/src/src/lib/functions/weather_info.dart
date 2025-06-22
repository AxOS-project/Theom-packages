import 'dart:io';

class WeatherData {
  final double temperature;
  final String condition;
  final String description;

  WeatherData({
    required this.temperature,
    required this.condition,
    required this.description,
  });
}

Future<WeatherData> getWeatherSummary() async {
  try {
    final result = await Process.run('curl', ['-s', 'wttr.in/?format=%t+%C']);
    if (result.exitCode != 0) {
      return WeatherData(temperature: 0, condition: 'N/A', description: 'Unable to fetch weather.');
    }

    final output = result.stdout.toString().trim();
    final parts = output.split(' ');

    if (parts.isEmpty || parts.length < 2) {
      return WeatherData(temperature: 0, condition: 'N/A', description: 'Invalid weather data.');
    }

    final tempStr = parts[0].replaceAll('+', '').replaceAll('°C', '');
    final temp = double.tryParse(tempStr) ?? 0;
    final condition = parts.sublist(1).join(' ');

    String desc = 'Enjoy your day!';
    final cond = condition.toLowerCase();

    if (cond.contains('sun')) {
      desc = 'Perfect day to go outside.';
    } else if (cond.contains('rain')) {
      desc = 'Don’t forget your umbrella!';
    } else if (cond.contains('cloud')) {
      desc = 'Might want a light jacket.';
    } else if (cond.contains('snow')) {
      desc = 'Stay warm out there!';
    }

    return WeatherData(
      temperature: temp,
      condition: condition,
      description: desc,
    );
  } catch (e) {
    return WeatherData(temperature: 0, condition: 'N/A', description: 'Error retrieving weather.');
  }
}
