import 'dart:async';
import 'package:flutter/material.dart';
import '../functions/time_info.dart';
import '../widgets/card_box.dart';

class TimeBox extends StatefulWidget {
    const TimeBox({super.key});

    @override
    State<TimeBox> createState() => _TimeBoxState();
}

class _TimeBoxState extends State<TimeBox> {
    late String _timeString;
    late Timer _timer;

    @override
    void initState() {
        super.initState();
        _timeString = getCurrentTime();
        _timer = Timer.periodic(const Duration(seconds: 1), (_) {
        setState(() {
            _timeString = getCurrentTime();
        });
        });
    }

    @override
    void dispose() {
        _timer.cancel();
        super.dispose();
    }

    @override
    Widget build(BuildContext context) {
        final parts = _timeString.split('\n');
        final time = parts[0];
        final date = parts.length > 1 ? parts[1] : '';

        return CardBox(
            child: Center(
            child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                Text(
                    time,
                    style: const TextStyle(
                    fontSize: 26,
                    fontWeight: FontWeight.bold,
                    ),
                ),
                const SizedBox(height: 4),
                Text(
                    date,
                    style: const TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.w400,
                    //color: Colors.white70,
                    ),
                ),
                ],
            ),
            ),
        );
    }
}