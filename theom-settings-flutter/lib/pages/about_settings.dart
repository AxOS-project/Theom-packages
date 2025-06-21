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


  @override
  Widget build(BuildContext context) {
    if (loading) return const Center(child: CircularProgressIndicator());

    return ListView(
      children: [
        const SettingsSectionTitle('Hardware'),
        SettingsTile(title: 'Device Name: ${info['device']}'),
        const SizedBox(height: 8),
        SettingsTile(title: 'CPU(s): ${info['cpu']}'),
        const SizedBox(height: 8),
        SettingsTile(title: 'GPU(s): ${info['gpu']}'),
        const SizedBox(height: 8),
        SettingsTile(title: 'Memory: ${info['mem']}'),
        const SizedBox(height: 8),
        const SettingsSectionTitle('Software'),
        SettingsTile(title: 'OS: ${info['os']}'),
        const SizedBox(height: 8),
        SettingsTile(title: 'Kernel: ${info['kernel']}'),
        const SizedBox(height: 8),
        SettingsTile(title: 'Theom Version: ${info['theom']}'),
      ],
    );
  }
}
