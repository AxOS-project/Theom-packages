import 'package:flutter/material.dart';
import '../functions/volume_info.dart';
import '../widgets/card_box.dart';

class VolumeSlider extends StatefulWidget {
  const VolumeSlider({super.key});

  @override
  State<VolumeSlider> createState() => _VolumeSliderState();
}

class _VolumeSliderState extends State<VolumeSlider> {
  double _volume = 50;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _loadVolume();
    });
  }

  void _loadVolume() async {
    final v = await getVolume();
    setState(() => _volume = v);
  }

  void _onChange(double v) {
    setState(() => _volume = v);
  }

  void _onChangeEnd(double v) {
    setVolume(v);
  }

  @override
  Widget build(BuildContext context) {
    return CardBox(
      child: Row(
        children: [
          const Text("Volume"),
          const SizedBox(width: 10),
          Expanded(
            child: Slider(
              value: _volume,
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
