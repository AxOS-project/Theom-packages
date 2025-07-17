import 'package:flutter/material.dart';

class ConfigTextFieldTile extends StatelessWidget {
  final String title;
  final String keyPath;
  final String currentValue;
  final ValueChanged<String> onChanged;

  const ConfigTextFieldTile({
    super.key,
    required this.title,
    required this.keyPath,
    required this.currentValue,
    required this.onChanged,
  });

  @override
  Widget build(BuildContext context) {
    return ListTile(
      title: Text(title),
      contentPadding: const EdgeInsets.symmetric(horizontal: 16.0),
      trailing: SizedBox(
        width: 368,
        child: TextField(
          controller: TextEditingController(text: currentValue)
            ..selection = TextSelection.collapsed(offset: currentValue.length),
          onChanged: onChanged,
          decoration: const InputDecoration(
            isDense: true,
            border: OutlineInputBorder(),
            contentPadding: EdgeInsets.symmetric(horizontal: 8, vertical: 8),
          ),
        ),
      ),
    );
  }
}
