import 'service.dart';

class ConfigCache {
  static final ConfigCache _instance = ConfigCache._internal();
  factory ConfigCache() => _instance;

  ConfigCache._internal();

  final Map<String, String> _data = {};
  bool _initialized = false;

  Future<void> loadOnce(List<String> keys) async {
    if (_initialized) return;
    final result = await ConfigService.load(keys);
    _data.addAll(result);
    _initialized = true;
  }

  String? get(String key) => _data[key];

  void set(String key, String value) {
    _data[key] = value;
    ConfigService.set(key, value);
  }

  void reset() {
    _data.clear();
    _initialized = false;
  }
}
