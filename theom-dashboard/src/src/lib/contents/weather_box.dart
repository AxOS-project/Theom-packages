import 'package:flutter/material.dart';
import '../functions/weather_info.dart';
import '../widgets/card_box.dart';

class WeatherBox extends StatefulWidget {
  const WeatherBox({super.key});

  @override
  State<WeatherBox> createState() => _WeatherBoxState();
}

class _WeatherBoxState extends State<WeatherBox> {
  WeatherData? weather;

  @override
  void initState() {
    super.initState();
    _loadWeather();
  }

  void _loadWeather() async {
    final w = await getWeatherSummary();
    setState(() => weather = w);
  }

    IconData _getIcon(String condition) {
        final c = condition.toLowerCase();
        if (c.contains("sun")) return Icons.wb_sunny;
        if (c.contains("clear")) return Icons.wb_sunny;
        if (c.contains("partly") || c.contains("cloud")) return Icons.cloud;
        if (c.contains("rain")) return Icons.grain;
        if (c.contains("storm") || c.contains("thunder")) return Icons.flash_on;
        if (c.contains("snow")) return Icons.ac_unit;
        if (c.contains("fog") || c.contains("mist")) return Icons.blur_on;
        return Icons.wb_cloudy;
    }


  @override
  Widget build(BuildContext context) {
    if (weather == null) {
      return const CardBox(child: Center(child: CircularProgressIndicator()));
    }

    return CardBox(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(_getIcon(weather!.condition), size: 40),
          const SizedBox(height: 8),
          Text(
            '${weather!.temperature.toStringAsFixed(1)}°C',
            style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 4),
          Text(
            weather!.condition,
            style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w500),
          ),
          const SizedBox(height: 4),
          Text(
            weather!.description,
            textAlign: TextAlign.center,
            style: const TextStyle(fontSize: 12),
          ),
        ],
      ),
    );
  }
}
