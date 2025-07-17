import 'package:flutter/material.dart';
import '../config/cache.dart';
import '../widgets/config_dropdown_tile.dart';
import '../widgets/config_toggle_tile.dart';
import '../widgets/config_textfield_tile.dart';
import '../widgets/settings_section_title.dart';

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
      children: [
        const SettingsSectionTitle('Animations'),
        ConfigDropdownTile(
          title: 'Compositor Animations',
          keyPath: 'compositor.animations',
          currentValue: ConfigCache().get('compositor.animations') ?? '',
          options: ['none', 'basic', 'fancy'],
          onChanged: (val) => _updateValue('compositor.animations', val),
        ),
        const SettingsSectionTitle('Wallpaper'),
        ConfigTextFieldTile(
          title: 'Wallpaper Path',
          keyPath: 'appearance.wallpaper',
          currentValue: ConfigCache().get('appearance.wallpaper') ?? '',
          onChanged: (val) => _updateValue('appearance.wallpaper', val),
        ),
      ],
    );
  }
}
