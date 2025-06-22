import 'dart:io';

Future<double> getVolume() async {
  try {
    final result = await Process.run('pamixer', ['--get-volume']);
    final value = double.tryParse(result.stdout.toString().trim());
    return value ?? 0;
  } catch (_) {
    return 0;
  }
}

Future<void> setVolume(double value) async {
  try {
    await Process.run('pamixer', ['--set-volume', value.toStringAsFixed(0)]);
  } catch (_) {}
}
