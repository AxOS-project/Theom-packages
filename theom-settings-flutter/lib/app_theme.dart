import 'package:flutter/material.dart';

class AppThemes {
  static ThemeData get dark {
    return ThemeData(
      brightness: Brightness.dark,
      fontFamily: 'Segoe UI',
      scaffoldBackgroundColor: const Color.fromRGBO(30, 30, 30, 0.85),
      colorScheme: const ColorScheme.dark(
        primary: Color(0xFFD35D6E),
        secondary: Color(0xFF4B5A66),
        surface: Color(0xFF282C34),
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: const Color(0xFF282C34),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(6),
          borderSide: const BorderSide(color: Color(0xFF4B5A66)),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(6),
          borderSide: const BorderSide(color: Color(0xFFD35D6E)),
        ),
      ),
      textTheme: const TextTheme(
        bodyMedium: TextStyle(fontSize: 14, color: Color(0xFFB0B4BC)),
        labelLarge: TextStyle(fontSize: 16, color: Color(0xFFB0B4BC)),
      ),
      listTileTheme: const ListTileThemeData(
        tileColor: Color(0xFF282C34),
        textColor: Color(0xFFB0B4BC),
        iconColor: Color(0xFFB0B4BC),
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: const Color(0xFF282C34),
          foregroundColor: const Color(0xFFB0B4BC),
          padding: const EdgeInsets.symmetric(vertical: 10, horizontal: 16),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(6),
            side: const BorderSide(color: Color(0xFF4B5A66)),
          ),
        ),
      ),
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
        ),
      ),
    );
  }
}
