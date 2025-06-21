import 'package:flutter/material.dart';
import 'app_theme.dart';
import 'pages/home_page.dart';

class SettingsApp extends StatelessWidget {
  final ThemeMode themeMode;
  const SettingsApp({required this.themeMode, super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Theom Settings',
      debugShowCheckedModeBanner: false,
      theme: AppThemes.light,
      darkTheme: AppThemes.dark,
      themeMode: themeMode,
      home: const SettingsHomePage(),
    );
  }
}
