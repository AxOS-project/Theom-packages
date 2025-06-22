import 'package:flutter/material.dart';

class RoundedBox extends StatelessWidget {
  final Widget child;
  const RoundedBox({super.key, required this.child});

  @override
  Widget build(BuildContext context) {
    return ClipRRect(
      borderRadius: BorderRadius.circular(30),
      child: Container(
        padding: const EdgeInsets.all(12),
        color: Theme.of(context).colorScheme.surface,
        child: child,
      ),
    );
  }
}
