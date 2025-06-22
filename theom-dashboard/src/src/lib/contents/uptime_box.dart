import 'package:flutter/material.dart';
import '../functions/uptime_info.dart';
import '../widgets/rounded_box.dart';

class UptimeBox extends StatefulWidget {
  const UptimeBox({super.key});

  @override
  State<UptimeBox> createState() => _UptimeBoxState();
}

class _UptimeBoxState extends State<UptimeBox> {
  String _uptime = 'Uptime: ...';

  @override
  void initState() {
    super.initState();
    _loadUptime();
  }

  void _loadUptime() async {
    final uptime = await getUptime();
    setState(() => _uptime = uptime);
  }

  @override
  Widget build(BuildContext context) {
    return RoundedBox(
      child: const Padding(
        padding: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        child: _UptimeText(),
      ),
    );
  }
}

class _UptimeText extends StatelessWidget {
  const _UptimeText();

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<String>(
      future: getUptime(),
      builder: (context, snapshot) {
        final text = snapshot.hasData ? snapshot.data! : 'Uptime: ...';
        return Text(
          text,
          style: DefaultTextStyle.of(context).style,
        );
      },
    );
  }
}
