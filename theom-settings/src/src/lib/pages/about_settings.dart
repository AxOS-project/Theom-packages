import 'package:flutter/material.dart';
import 'package:process_run/process_run.dart';
import '../widgets/settings_tile.dart';
import '../widgets/settings_section_title.dart';

class AboutSettings extends StatefulWidget {
  const AboutSettings({super.key});

  @override
  State<AboutSettings> createState() => _AboutSettingsState();
}

class _AboutSettingsState extends State<AboutSettings> {
  Map<String, String> info = {};
  bool loading = true;

  @override
  void initState() {
    super.initState();
    _loadInfo();
  }

  Future<void> _loadInfo() async {
    final data = <String, String>{};

    Future<String> runCmd(String cmd) async {
      try {
        final result = await run('bash', ['-c', cmd]);
        return result.stdout.toString().trim();
      } catch (_) {
        return 'Unknown';
      }
    }

    data['device'] = await runCmd('hostname');
    data['cpu'] = await runCmd('lscpu | grep "Model name" | cut -d ":" -f2');
    data['gpu'] = await runCmd('lspci | grep VGA | cut -d ":" -f3');
    data['mem'] = await runCmd("free -h | awk '/Mem:/ {print \$2}'");
    data['os'] = await runCmd('bash -c "source /etc/os-release && echo \\\$PRETTY_NAME"');
    data['kernel'] = await runCmd('uname -r');
    data['theom'] = await runCmd('pacman -Q theom');

    setState(() {
      info = data.map((k, v) => MapEntry(k, v.trim()));
      loading = false;
    });
  }

  Widget buildCard(String title) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      child: Material(
        elevation: 2,
        borderRadius: BorderRadius.circular(12),
        color: Theme.of(context).colorScheme.surface,
        child: Padding(
          padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 16),
          child: Text(
            title,
            style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                  color: Theme.of(context).colorScheme.onSurface,
                ),
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    if (loading) return const Center(child: CircularProgressIndicator());

    return ListView(
      padding: const EdgeInsets.only(bottom: 24),
      children: [
        const SettingsSectionTitle('Hardware'),
        buildCard('Device Name: ${info['device']}'),
        buildCard('CPU(s): ${info['cpu']}'),
        buildCard('GPU(s): ${info['gpu']}'),
        buildCard('Memory: ${info['mem']}'),
        const SettingsSectionTitle('Software'),
        buildCard('OS: ${info['os']}'),
        buildCard('Kernel: ${info['kernel']}'),
        buildCard('Theom Version: ${info['theom']}'),
      ],
    );
  }
}
