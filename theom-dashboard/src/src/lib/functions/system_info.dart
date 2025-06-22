import 'dart:io';
import 'dart:async';

Future<Map<String, double>> getSystemInfo() async {
  final cpu = await _getCpuUsage();
  final ram = await _getRamUsage();
  final temp = await _getTemperature();

  return {
    'cpu': cpu,
    'ram': ram,
    'temp': temp,
  };
}

Future<double> _getCpuUsage() async {
  final first = await _readProcStat();
  await Future.delayed(const Duration(milliseconds: 100));
  final second = await _readProcStat();

  final totalDelta = (second.total - first.total).toDouble();
  final idleDelta = (second.idle - first.idle).toDouble();

  if (totalDelta == 0) return 0.0;
  return ((totalDelta - idleDelta) / totalDelta) * 100;
}

class _CpuStat {
  final int user, nice, system, idle, iowait, irq, softirq;
  _CpuStat(this.user, this.nice, this.system, this.idle, this.iowait, this.irq, this.softirq);

  int get total => user + nice + system + idle + iowait + irq + softirq;

  static Future<_CpuStat> parseFromLine(String line) async {
    final parts = line.split(RegExp(r'\s+'));
    return _CpuStat(
      int.parse(parts[1]),
      int.parse(parts[2]),
      int.parse(parts[3]),
      int.parse(parts[4]),
      int.parse(parts[5]),
      int.parse(parts[6]),
      int.parse(parts[7]),
    );
  }
}

Future<_CpuStat> _readProcStat() async {
  final file = File('/proc/stat');
  final line = await file.readAsLines().then((lines) => lines.firstWhere((l) => l.startsWith('cpu ')));
  return _CpuStat.parseFromLine(line);
}

Future<double> _getRamUsage() async {
  final file = File('/proc/meminfo');
  final lines = await file.readAsLines();
  double? total, available;

  for (final line in lines) {
    if (line.startsWith('MemTotal')) {
      total = double.parse(line.split(RegExp(r'\s+'))[1]);
    } else if (line.startsWith('MemAvailable')) {
      available = double.parse(line.split(RegExp(r'\s+'))[1]);
    }
    if (total != null && available != null) break;
  }

  if (total == null || available == null) return 0;
  return ((total - available) / total) * 100;
}

Future<double> _getTemperature() async {
  final dir = Directory('/sys/class/thermal');
  if (!await dir.exists()) return 0;

  final entries = await dir.list().toList();

  for (final entry in entries) {
    if (entry is Directory && entry.path.contains('thermal_zone')) {
      final typeFile = File('${entry.path}/type');
      final tempFile = File('${entry.path}/temp');

      try {
        final type = await typeFile.readAsString();
        if (!RegExp(r'(cpu|pkg|core)', caseSensitive: false).hasMatch(type)) {
          continue;
        }

        final tempRaw = await tempFile.readAsString();
        final milliC = int.parse(tempRaw.trim());
        return milliC / 1000.0;
      } catch (_) {
        continue;
      }
    }
  }

  return 0;
}
