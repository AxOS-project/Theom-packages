import 'package:flutter/material.dart';

@immutable
class ExtraColors extends ThemeExtension<ExtraColors> {
  final Color cardBackground;

  const ExtraColors({required this.cardBackground});

  @override
  ExtraColors copyWith({Color? cardBackground}) {
    return ExtraColors(
      cardBackground: cardBackground ?? this.cardBackground,
    );
  }

  @override
  ExtraColors lerp(ThemeExtension<ExtraColors>? other, double t) {
    if (other is! ExtraColors) return this;
    return ExtraColors(
      cardBackground: Color.lerp(cardBackground, other.cardBackground, t)!,
    );
  }
}
