import 'package:flutter/material.dart';
import 'app.dart';
import 'config/get_theme_config.dart';
import 'package:theom_settings/config/cache.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  final themeString = await readThemeFromConfig();
  final themeMode =
      themeString.trim().toLowerCase() == 'dark' ? ThemeMode.dark : ThemeMode.light;

  await ConfigCache().loadOnce([
    // System keys
    'osd.osd',
    'compositor.compositing',
    'compositor.compositing_mode',
    'bar.polybar_layout',
    'bar.use_eww',
    // General keys
    'appearance.theme',
  ]);

  runApp(SettingsApp(themeMode: themeMode));
}
