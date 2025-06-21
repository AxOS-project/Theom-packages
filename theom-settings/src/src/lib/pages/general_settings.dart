import 'package:flutter/material.dart';
import 'package:process_run/process_run.dart';
import '../config/cache.dart';
import '../widgets/settings_tile.dart';
import '../widgets/settings_section_title.dart';
import '../widgets/config_dropdown_tile.dart';

class GeneralSettings extends StatefulWidget {
  const GeneralSettings({super.key});

  @override
  State<GeneralSettings> createState() => _GeneralSettingsState();
}

class _GeneralSettingsState extends State<GeneralSettings> {
  final keys = ['appearance.theme'];

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
        const SettingsSectionTitle('General'),
        SettingsTile(
          title: 'Open GTK Theme Manager',
          subtitle: 'Launch lxappearance',
          trailingIcon: Icons.open_in_new,
          onTap: () async {
            await run('lxappearance', []);
          },
        ),
        const SizedBox(height: 8),
        ConfigDropdownTile(
          title: 'Theme',
          keyPath: 'appearance.theme',
          currentValue: ConfigCache().get('appearance.theme') ?? '',
          options: ['light', 'dark'],
          onChanged: (val) => _updateValue('appearance.theme', val),
        ),
      ],
    );
  }
}
