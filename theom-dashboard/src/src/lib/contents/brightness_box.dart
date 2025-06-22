import 'package:flutter/material.dart';
import '../functions/brightness_info.dart';
import '../widgets/card_box.dart';

class BrightnessBox extends StatefulWidget {
  const BrightnessBox({super.key});

  @override
  State<BrightnessBox> createState() => _BrightnessBoxState();
}

class _BrightnessBoxState extends State<BrightnessBox> {
  double _brightness = 50;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _loadBrightness();
    });
  }

  void _loadBrightness() async {
    final v = await getBrightness();
    setState(() => _brightness = v);
  }

  void _onChange(double v) {
    setState(() => _brightness = v);
  }

  void _onChangeEnd(double v) {
    setBrightness(v);
  }

  @override
  Widget build(BuildContext context) {
    return CardBox(
      child: Row(
        children: [
          const Text("Brightness"),
          const SizedBox(width: 10),
          Expanded(
            child: Slider(
              value: _brightness,
              onChanged: _onChange,
              onChangeEnd: _onChangeEnd,
              min: 0,
              max: 100,
            ),
          ),
        ],
      ),
    );
  }
}
