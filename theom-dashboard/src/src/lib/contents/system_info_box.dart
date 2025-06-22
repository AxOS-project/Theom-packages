import 'dart:async';
import 'package:flutter/material.dart';
import '../functions/system_info.dart';
import '../widgets/card_box.dart';

class SystemInfoBox extends StatefulWidget {
  const SystemInfoBox({super.key});

  @override
  State<SystemInfoBox> createState() => _SystemInfoBoxState();
}

class _SystemInfoBoxState extends State<SystemInfoBox> {
  double cpu = 0, ram = 0, temp = 0;
  late Timer _timer;

  @override
  void initState() {
    super.initState();
    _loadInfo(); // initial load
    _timer = Timer.periodic(const Duration(seconds: 2), (_) => _loadInfo());
  }

  void _loadInfo() async {
    final info = await getSystemInfo();
    if (!mounted) return;
    setState(() {
      cpu = info['cpu'] ?? 0;
      ram = info['ram'] ?? 0;
      temp = info['temp'] ?? 0;
    });
  }

  @override
  void dispose() {
    _timer.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return CardBox(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          _buildRow("CPU", cpu),
          _buildRow("RAM", ram),
          _buildRow("Temp", temp, isTemp: true),
        ],
      ),
    );
  }

  Widget _buildRow(String label, double value, {bool isTemp = false}) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 6, horizontal: 12),
      child: Row(
        children: [
          SizedBox(width: 60, child: Text(label)),
          Expanded(
            child: Slider(
              value: isTemp ? (value / 100).clamp(0.0, 1.0) : value.clamp(0.0, 100.0),
              onChanged: null, // read-only
              min: 0,
              max: isTemp ? 1.0 : 100.0,
            ),
          ),
          Text(
            isTemp ? "${value.toStringAsFixed(1)}°C" : "${value.toStringAsFixed(1)}%",
            style: const TextStyle(fontSize: 12),
          ),
        ],
      ),
    );
  }
}
