import 'dart:io';
import 'package:process_run/process_run.dart';

Future<String> readThemeFromConfig() async {
  try {
    final result = await run('theom-config', ['appearance.theme']);
    return result.stdout.toString();
  } catch (e) {
    return 'light';
  }
}
