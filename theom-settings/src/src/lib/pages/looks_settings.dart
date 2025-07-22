import 'package:flutter/material.dart';
import '../config/cache.dart';
import '../widgets/config_dropdown_tile.dart';
import '../widgets/config_toggle_tile.dart';
import '../widgets/config_textfield_tile.dart';
import '../widgets/settings_section_title.dart';
import '../widgets/theme_selector_tile.dart';
import '../widgets/animation_selector_tile.dart';
import '../widgets/wallpaperpath_selector_tile.dart';

class LooksSettings extends StatefulWidget {
  const LooksSettings({super.key});

  @override
  State<LooksSettings> createState() => _LooksSettingsState();
}

class _LooksSettingsState extends State<LooksSettings> {
  final keys = [
    'compositor.animations',
    'appearance.wallpaper',
  ];

  bool loading = true;

  @override
  void initState() {
    super.initState();
    ConfigCache().loadOnce(keys).then((_) {
      setState(() {
        loading = false;
      });
    });
  }

  void _updateValue(String key, String value) {
    ConfigCache().set(key, value);
    setState(() {});
  }

  @override
  Widget build(BuildContext context) {
    //if (loading) {
    //  return const Center(child: CircularProgressIndicator());
    //}

return ListView(
  padding: const EdgeInsets.all(16),
  children: [
    const SettingsSectionTitle('Theme'),
    ThemeSelectorTile(
      currentTheme: ConfigCache().get('appearance.theme') ?? 'light',
      onChanged: (val) => _updateValue('appearance.theme', val),
    ),

    const SizedBox(height: 24),
    const SettingsSectionTitle('Animations'),
    AnimationSelectorTile(
      currentAnimation: ConfigCache().get('compositor.animations') ?? 'none',
      onChanged: (val) => _updateValue('compositor.animations', val),
    ),

    const SizedBox(height: 24),
    const SettingsSectionTitle('Wallpaper'),
    WallpaperSelectorTile(
      wallpaperPath: ConfigCache().get('appearance.wallpaper') ?? '',
      onChange: (val) => _updateValue('appearance.wallpaper', val),
    ),
  ],
);

  }
}
