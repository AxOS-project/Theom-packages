import 'package:flutter/material.dart';
import 'package:process_run/process_run.dart';
import 'app_theme.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  String output = await runShellCommand();

  final themeMode = output.trim().toLowerCase() == 'dark'
      ? ThemeMode.dark
      : ThemeMode.light;

  runApp(SettingsApp(themeMode: themeMode));
}

Future<String> runShellCommand() async {
  try {
    final result = await run('theom-config', ['appearance.theme']);
    return result.stdout.toString();
  } catch (e) {
    return 'light';
  }
}

class SettingsApp extends StatelessWidget {
  final ThemeMode themeMode;
  const SettingsApp({required this.themeMode, super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Settings App',
      debugShowCheckedModeBanner: false,
      theme: AppThemes.light,
      darkTheme: AppThemes.dark,
      themeMode: themeMode,
      home: const SettingsHomePage(),
    );
  }
}


class SettingsHomePage extends StatefulWidget {
  const SettingsHomePage({super.key});

  @override
  State<SettingsHomePage> createState() => _SettingsHomePageState();
}

class _SettingsHomePageState extends State<SettingsHomePage> {
  int selectedIndex = 0;

  final List<String> sections = ['General', 'System', 'About'];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('System Settings')),
      body: Row(
        children: [
          // Sidebar
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
          // Content area
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
      case 'System':
        return const SystemSettings();
      case 'About':
        return const AboutSettings();
      default:
        return const Center(child: Text('Unknown Section'));
    }
  }
}

class GeneralSettings extends StatelessWidget {
  const GeneralSettings({super.key});

  @override
  Widget build(BuildContext context) {
    return ListView(
      children: [
        SettingsSectionTitle('General'),
        SettingsTile(
          title: 'Open GTK Theme Manager',
          subtitle: 'Launch lxappearance',
          onTap: () async {
            await run('lxappearance', []);
          },
        ),
        const SizedBox(height: 8),
        SettingsTile(title: 'Theme', subtitle: 'Light'),
      ],
    );
  }
}

class SystemSettings extends StatelessWidget {
  const SystemSettings({super.key});

  @override
  Widget build(BuildContext context) {
    return ListView(
      children: const [
        SettingsSectionTitle('System'),
        SettingsTile(title: 'Enable OSD', subtitle: 'true'),
        const SizedBox(height: 8),
        SettingsTile(title: 'Enable Compositing', subtitle: 'true'),
        const SizedBox(height: 8),
        SettingsTile(title: 'Compositing Mode', subtitle: 'performance'),
        SettingsSectionTitle('Status Bar'),
        SettingsTile(title: 'Polybar Layout', subtitle: 'floating'),
        const SizedBox(height: 8),
        SettingsTile(title: 'Use Eww Bar', subtitle: 'true'),
      ],
    );
  }
}

class AboutSettings extends StatelessWidget {
  const AboutSettings({super.key});

  @override
  Widget build(BuildContext context) {
    return ListView(
      children: const [
        SettingsSectionTitle('About'),
        SettingsTile(title: 'Version', subtitle: '1.0.0'),
        const SizedBox(height: 8),
        SettingsTile(title: 'Licenses'),
      ],
    );
  }
}

class SettingsSectionTitle extends StatelessWidget {
  final String title;
  const SettingsSectionTitle(this.title, {super.key});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(top: 16, bottom: 8),
      child: Text(
        title,
        style: Theme.of(context).textTheme.titleMedium?.copyWith(
              fontWeight: FontWeight.bold,
              color: Colors.blueGrey[700],
            ),
      ),
    );
  }
}

class SettingsTile extends StatelessWidget {
  final String title;
  final String? subtitle;
  final Future<void> Function()? onTap;

  const SettingsTile({
    required this.title,
    this.subtitle,
    this.onTap,
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return ListTile(
      title: Text(title),
      subtitle: subtitle != null ? Text(subtitle!) : null,
      onTap: () {
        if (onTap != null) {
          onTap!();
        }
      },
    );
  }
}
