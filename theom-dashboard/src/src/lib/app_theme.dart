import 'package:flutter/material.dart';
import 'app_theme_extension.dart';

class AppThemes {
  static const darkCard = Color(0xFF1E1E1E);
  static const lightCard = Color(0xFFE9E3D8);

  static ThemeData get dark {
    const background = Color(0xFF181818);
    const surface = Color(0xFF455A64); // Blue-grey dark
    const border = Color(0xFF2D2D2D);
    const text = Color(0xFFA0A4AC);
    const accent = Color(0xFFC9505F);

    return ThemeData(
      brightness: Brightness.dark,
      fontFamily: 'Segoe UI',
      scaffoldBackgroundColor: background,
      colorScheme: const ColorScheme.dark(
        primary: accent,
        secondary: Color(0xFF404D58),
        surface: surface,
      ),
      extensions: [
        const ExtraColors(cardBackground: darkCard),
      ],

      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: surface,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(6),
          borderSide: const BorderSide(color: border),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(6),
          borderSide: const BorderSide(color: accent),
        ),
      ),

      textTheme: const TextTheme(
        bodyMedium: TextStyle(fontSize: 14, color: text),
        labelLarge: TextStyle(fontSize: 16, color: text),
      ),

      listTileTheme: const ListTileThemeData(
        tileColor: surface,
        textColor: text,
        iconColor: text,
      ),

      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: surface,
          foregroundColor: text,
          padding: const EdgeInsets.symmetric(vertical: 10, horizontal: 16),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(6),
            side: const BorderSide(color: border),
          ),
          animationDuration: Duration(milliseconds: 100),
        ),
      ),

      splashFactory: NoSplash.splashFactory,
      highlightColor: Colors.transparent,
      splashColor: Colors.transparent,
      hoverColor: Colors.transparent,
    );
  }

  static ThemeData get light {
    return ThemeData(
      brightness: Brightness.light,
      fontFamily: 'Segoe UI',
      scaffoldBackgroundColor: const Color(0xFFEFE1CA),
      colorScheme: const ColorScheme.light(
        primary: Color(0xFF0986D3),
        secondary: Color(0xFFA70B06),
        surface: Color(0xFFF5EFE4),
      ),
      extensions: [
        const ExtraColors(cardBackground: lightCard),
      ],

      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: const Color(0xFFF5EFE4),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(6),
          borderSide: const BorderSide(color: Color(0xFFA70B06)),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(6),
          borderSide: const BorderSide(color: Color(0xFF0986D3)),
        ),
      ),

      textTheme: const TextTheme(
        bodyMedium: TextStyle(fontSize: 14, color: Color(0xFF4B5A66)),
        labelLarge: TextStyle(fontSize: 16, color: Color(0xFF4B5A66)),
      ),

      listTileTheme: const ListTileThemeData(
        tileColor: Color(0xFFF5EFE4),
        textColor: Color(0xFF4B5A66),
        iconColor: Color(0xFF4B5A66),
      ),

      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: const Color(0xFFD8C4AC),
          foregroundColor: const Color(0xFF4B5A66),
          padding: const EdgeInsets.symmetric(vertical: 10, horizontal: 16),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(6),
            side: const BorderSide(color: Color(0xFFA70B06)),
          ),
          animationDuration: Duration(milliseconds: 100),
        ),
      ),

      splashFactory: NoSplash.splashFactory,
      highlightColor: Colors.transparent,
      splashColor: Colors.transparent,
      hoverColor: Colors.transparent,
    );
  }
}
