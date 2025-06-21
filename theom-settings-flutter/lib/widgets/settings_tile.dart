import 'package:flutter/material.dart';

class SettingsTile extends StatelessWidget {
  final String title;
  final String? subtitle;
  final Future<void> Function()? onTap;
  final IconData? trailingIcon;

  const SettingsTile({
    required this.title,
    this.subtitle,
    this.onTap,
    this.trailingIcon,
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return ListTile(
      title: Text(title),
      subtitle: subtitle != null ? Text(subtitle!) : null,
      trailing: trailingIcon != null ? Icon(trailingIcon) : null,
      onTap: () {
        if (onTap != null) {
          onTap!();
        }
      },
    );
  }
}
