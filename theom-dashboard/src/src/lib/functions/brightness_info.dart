import 'dart:io';

Future<double> getBrightness() async {
  try {
    final result = await Process.run('brightnessctl', ['get']);
    final current = double.parse(result.stdout.toString().trim());

    final maxResult = await Process.run('brightnessctl', ['max']);
    final max = double.parse(maxResult.stdout.toString().trim());

    return (current / max) * 100;
  } catch (_) {
    return 0;
  }
}

Future<void> setBrightness(double value) async {
  try {
    final percent = value.toStringAsFixed(0) + '%';
    await Process.run('brightnessctl', ['set', percent]);
  } catch (_) {}
}
