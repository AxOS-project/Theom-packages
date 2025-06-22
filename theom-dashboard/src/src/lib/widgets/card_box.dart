import 'package:flutter/material.dart';
import '../app_theme_extension.dart';

class CardBox extends StatelessWidget {
  final Widget child;
  final Color? color;

  const CardBox({super.key, required this.child, this.color});

  @override
  Widget build(BuildContext context) {
    final themeExtras = Theme.of(context).extension<ExtraColors>()!;
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: color ?? themeExtras.cardBackground,
        borderRadius: BorderRadius.circular(16),
        boxShadow: const [BoxShadow(color: Colors.black45, blurRadius: 6)],
      ),
      child: child,
    );
  }
}
