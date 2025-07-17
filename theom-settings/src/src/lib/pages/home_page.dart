import 'package:flutter/material.dart';
import 'general_settings.dart';
import 'system_settings.dart';
import 'about_settings.dart';
import 'looks_settings.dart';

class SettingsHomePage extends StatefulWidget {
  const SettingsHomePage({super.key});

  @override
  State<SettingsHomePage> createState() => _SettingsHomePageState();
}

class _SettingsHomePageState extends State<SettingsHomePage> {
  int selectedIndex = 0;
  final List<String> sections = ['General', 'Looks', 'System', 'About'];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('System Settings')),
      body: Row(
        children: [
          NavigationRail(
            selectedIndex: selectedIndex,
            onDestinationSelected: (index) {
              setState(() {
                selectedIndex = index;
              });
            },
            labelType: NavigationRailLabelType.all,
            destinations: const [
              NavigationRailDestination(
                icon: Icon(Icons.settings),
                label: Text('General'),
              ),
              NavigationRailDestination(
                icon: Icon(Icons.brush),
                label: Text('Looks'),
              ),
              NavigationRailDestination(
                icon: Icon(Icons.computer),
                label: Text('System'),
              ),
              NavigationRailDestination(
                icon: Icon(Icons.info_outline),
                label: Text('About'),
              ),
            ],
          ),
          const VerticalDivider(width: 1),
          Expanded(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: _buildPage(sections[selectedIndex]),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildPage(String section) {
    switch (section) {
      case 'General':
        return const GeneralSettings();
      case 'Looks':
        return const LooksSettings();
      case 'System':
        return const SystemSettings();
      case 'About':
        return const AboutSettings();
      default:
        return const Center(child: Text('Unknown Section'));
    }
  }
}
