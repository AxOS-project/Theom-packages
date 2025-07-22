import 'package:flutter/material.dart';
import '../config/cache.dart';
import '../widgets/config_dropdown_tile.dart';
import '../widgets/config_toggle_tile.dart';
import '../widgets/settings_section_title.dart';

class SystemSettings extends StatefulWidget {
  const SystemSettings({super.key});

  @override
  State<SystemSettings> createState() => _SystemSettingsState();
}

class _SystemSettingsState extends State<SystemSettings> {
  final keys = [
    'osd.osd',
    'compositor.compositing',
    'compositor.compositing_mode',
    'bar.polybar_layout',
    'bar.use_eww',
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

  Widget buildCard(Widget child) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      child: Material(
        elevation: 2,
        borderRadius: BorderRadius.circular(12),
        color: Theme.of(context).colorScheme.surface,
        child: Padding(
          padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 16),
          child: child,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    if (loading) {
      return const Center(child: CircularProgressIndicator());
    }

    return ListView(
      padding: const EdgeInsets.only(bottom: 24),
      children: [
        const SettingsSectionTitle('System'),
        buildCard(
          ConfigToggleTile(
            title: 'Enable OSD',
            keyPath: 'osd.osd',
            value: ConfigCache().get('osd.osd') == 'true',
            onChanged: (val) => _updateValue('osd.osd', val.toString()),
          ),
        ),
        buildCard(
          ConfigToggleTile(
            title: 'Enable Compositing',
            keyPath: 'compositor.compositing',
            value: ConfigCache().get('compositor.compositing') == 'true',
            onChanged: (val) => _updateValue('compositor.compositing', val.toString()),
          ),
        ),
        buildCard(
          ConfigDropdownTile(
            title: 'Compositing Mode',
            keyPath: 'compositor.compositing_mode',
            currentValue: ConfigCache().get('compositor.compositing_mode') ?? '',
            options: ['performance', 'compatibility'],
            onChanged: (val) => _updateValue('compositor.compositing_mode', val),
          ),
        ),
        const SettingsSectionTitle('Status Bar'),
        buildCard(
          ConfigDropdownTile(
            title: 'Polybar Layout',
            keyPath: 'bar.polybar_layout',
            currentValue: ConfigCache().get('bar.polybar_layout') ?? '',
            options: ['stuck', 'float'],
            onChanged: (val) => _updateValue('bar.polybar_layout', val),
          ),
        ),
        buildCard(
          ConfigToggleTile(
            title: 'Use Eww Bar (recommended)',
            keyPath: 'bar.use_eww',
            value: ConfigCache().get('bar.use_eww') == 'true',
            onChanged: (val) => _updateValue('bar.use_eww', val.toString()),
          ),
        ),
      ],
    );
  }
}
