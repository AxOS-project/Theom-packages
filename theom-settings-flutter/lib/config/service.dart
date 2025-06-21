import 'package:process_run/process_run.dart';

class ConfigService {
  static Future<Map<String, String>> load(List<String> keys) async {
    final Map<String, String> result = {};
    for (final key in keys) {
      try {
        final res = await run('theom-config', [key]);
        result[key] = res.stdout.toString().trim();
      } catch (_) {
        result[key] = '';
      }
    }
    return result;
  }

  static Future<void> set(String key, String value) async {
    await run('theom-config', ['set', key, value]);
  }
}
