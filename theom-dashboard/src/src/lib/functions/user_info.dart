import 'dart:io';

Future<String> getUsername() async {
  return Platform.environment['USER'] ?? 'Unknown';
}
