import 'package:flutter/material.dart';
import 'card_box.dart';

class CompactSlider extends StatelessWidget {
  final String label;
  const CompactSlider({super.key, required this.label});

  @override
  Widget build(BuildContext context) {
    return CardBox(
      child: Row(
        children: [
          Text(label),
          const SizedBox(width: 10),
          Expanded(
            child: Slider(
              value: 0.5,
              onChanged: (_) {},
            ),
          ),
        ],
      ),
    );
  }
}
