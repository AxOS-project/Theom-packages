import 'dart:io';

Future<String> getUptime() async {
  try {
    final file = File('/proc/uptime');
    final contents = await file.readAsString();
    final seconds = double.parse(contents.split(' ').first);
    final duration = Duration(seconds: seconds.toInt());

    final hours = duration.inHours;
    final minutes = duration.inMinutes.remainder(60);

    return 'Uptime: ${hours}h ${minutes}m';
  } catch (e) {
    return 'Uptime: unavailable';
  }
}
