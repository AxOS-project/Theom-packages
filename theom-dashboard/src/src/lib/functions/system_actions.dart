import 'dart:io';

Future<void> shutdownSystem() async {
  await Process.run('systemctl', ['poweroff']);
}

Future<void> rebootSystem() async {
  await Process.run('systemctl', ['reboot']);
}

Future<void> logoutUser() async {
  // This depends on session manager. Here's a common fallback:
  await Process.run('loginctl', ['terminate-user', Platform.environment['USER'] ?? '']);
}
