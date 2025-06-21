import 'package:flutter/material.dart';

class ConfigToggleTile extends StatelessWidget {
  final String title;
  final String keyPath;
  final bool value;
  final ValueChanged<bool> onChanged;

  const ConfigToggleTile({
    super.key,
    required this.title,
    required this.keyPath,
    required this.value,
    required this.onChanged,
  });

  @override
  Widget build(BuildContext context) {
    return SwitchListTile(
      title: Text(title),
      value: value,
      onChanged: (val) {
        if (val != null) {
          onChanged(val);
        }
      },
    );
  }
}
