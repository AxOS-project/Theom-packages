import 'package:flutter/material.dart';
import 'package:process_run/process_run.dart';
import '../config/cache.dart';
import '../widgets/settings_tile.dart';
import '../widgets/settings_section_title.dart';

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
      setState(() => loading = false);
    });
  }

  void _updateValue(String key, String value) {
    ConfigCache().set(key, value);
    setState(() {});
  }

  Widget buildCard({
    required String title,
    String? subtitle,
    IconData? icon,
    VoidCallback? onTap,
  }) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      child: Material(
        elevation: 2,
        borderRadius: BorderRadius.circular(12),
        color: Theme.of(context).colorScheme.surface,
        child: InkWell(
          borderRadius: BorderRadius.circular(12),
          onTap: onTap,
          child: Padding(
            padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 16),
            child: Row(
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        title,
                        style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                              color: Theme.of(context).colorScheme.onSurface,
                            ),
                      ),
                      if (subtitle != null) ...[
                        const SizedBox(height: 4),
                        Text(
                          subtitle,
                          style: Theme.of(context).textTheme.bodySmall?.copyWith(
                                color: Theme.of(context).colorScheme.onSurface.withOpacity(0.7),
                              ),
                        ),
                      ]
                    ],
                  ),
                ),
                if (icon != null)
                  Icon(
                    icon,
                    color: Theme.of(context).colorScheme.primary,
                  ),
              ],
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
        const SettingsSectionTitle('General'),
        buildCard(
          title: 'Open GTK Theme Manager',
          subtitle: 'Launch lxappearance',
          icon: Icons.open_in_new,
          onTap: () => run('lxappearance', []),
        ),
      ],
    );
  }
}
