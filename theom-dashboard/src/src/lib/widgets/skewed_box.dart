import 'package:flutter/material.dart';

class SkewedBox extends StatelessWidget {
  final Widget child;
  const SkewedBox({super.key, required this.child});

  @override
  Widget build(BuildContext context) {
    return Transform(
      transform: Matrix4.skewX(-0.2),
      child: Container(
        padding: const EdgeInsets.all(16),
        color: Colors.deepPurpleAccent,
        child: child,
      ),
    );
  }
}
