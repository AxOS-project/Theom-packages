import 'dart:io';
import 'package:flutter/material.dart';
import 'app_theme.dart';
import 'dashboard_page.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  final isDark = await _getPreferredTheme();

  runApp(DashboardApp(isDark: isDark));
}

Future<bool> _getPreferredTheme() async {
  try {
    final result = await Process.run('theom-config', ['appearance.theme']);
    final theme = result.stdout.toString().trim().toLowerCase();
    return theme == 'dark';
  } catch (e) {
    return true;
  }
}

class DashboardApp extends StatelessWidget {
  final bool isDark;

  const DashboardApp({super.key, required this.isDark});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Desktop Dashboard',
      theme: isDark ? AppThemes.dark : AppThemes.light,
      home: const DashboardPage(),
    );
  }
}
