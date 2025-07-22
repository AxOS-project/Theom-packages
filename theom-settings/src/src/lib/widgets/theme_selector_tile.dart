import 'package:flutter/material.dart';


class ThemeSelectorTile extends StatelessWidget {
  final String currentTheme;
  final ValueChanged<String> onChanged;

  const ThemeSelectorTile({
    required this.currentTheme,
    required this.onChanged,
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    final isLight = currentTheme == 'light';

    Widget buildPreview(String theme) {
      final isSelected = currentTheme == theme;
      final isLight = theme == 'light';

      return Expanded(
        child: GestureDetector(
          onTap: () => onChanged(theme),
          child: AnimatedContainer(
            duration: Duration(milliseconds: 200),
            margin: EdgeInsets.all(8),
            padding: EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: isLight ? Colors.white : Colors.black,
              borderRadius: BorderRadius.circular(12),
              border: Border.all(
                color: isSelected ? Theme.of(context).colorScheme.primary : Colors.grey,
                width: isSelected ? 2 : 1,
              ),
              boxShadow: [
                if (isSelected)
                  BoxShadow(
                    color: Theme.of(context).colorScheme.primary.withOpacity(0.3),
                    blurRadius: 8,
                    offset: Offset(0, 4),
                  ),
              ],
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  theme.toUpperCase(),
                  style: TextStyle(
                    color: isLight ? Colors.black : Colors.white,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 8),
                Container(
                  height: 24,
                  decoration: BoxDecoration(
                    color: isLight ? Colors.grey[300] : Colors.grey[800],
                    borderRadius: BorderRadius.circular(4),
                  ),
                ),
                const SizedBox(height: 4),
                Container(
                  height: 16,
                  width: 100,
                  color: isLight ? Colors.grey[200] : Colors.grey[700],
                ),
              ],
            ),
          ),
        ),
      );
    }

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            buildPreview('light'),
            buildPreview('dark'),
          ],
        ),
      ],
    );
  }
}
