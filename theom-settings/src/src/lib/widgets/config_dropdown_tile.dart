import 'package:flutter/material.dart';

class ConfigDropdownTile extends StatelessWidget {
  final String title;
  final String keyPath;
  final String currentValue;
  final List<String> options;
  final ValueChanged<String> onChanged;

  const ConfigDropdownTile({
    super.key,
    required this.title,
    required this.keyPath,
    required this.currentValue,
    required this.options,
    required this.onChanged,
  });

  @override
  Widget build(BuildContext context) {
    return ListTile(
      title: Text(title),
      contentPadding: const EdgeInsets.symmetric(horizontal: 16.0),
      trailing: Theme(
        data: Theme.of(context).copyWith(
          focusColor: Colors.transparent,
        ),
        child: DropdownButtonHideUnderline(
          child: DropdownButton<String>(
            isDense: true,
            value: currentValue.isEmpty ? null : currentValue,
            onChanged: (val) {
              if (val != null) {
                onChanged(val);
                // Force rebuild to drop lingering visual state
                FocusScope.of(context).requestFocus(FocusNode());
              }
            },
            items: options
                .map((opt) => DropdownMenuItem(
                      value: opt,
                      child: Text(opt),
                    ))
                .toList(),
          ),
        ),
      ),
    );
  }
}
