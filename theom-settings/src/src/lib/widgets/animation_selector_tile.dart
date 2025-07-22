import 'package:flutter/material.dart';

class AnimationSelectorTile extends StatelessWidget {
  final String currentAnimation;
  final ValueChanged<String> onChanged;

  const AnimationSelectorTile({
    required this.currentAnimation,
    required this.onChanged,
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    final options = ['none', 'basic', 'fancy'];

    Widget buildPreview(String type) {
      final isSelected = currentAnimation == type;

      Duration animationDuration;
      List<double> barHeights;

      switch (type) {
        case 'none':
          animationDuration = Duration.zero;
          barHeights = [8, 8, 8];
          break;
        case 'basic':
          animationDuration = Duration(milliseconds: 300);
          barHeights = [10, 14, 10];
          break;
        case 'fancy':
        default:
          animationDuration = Duration(milliseconds: 500);
          barHeights = [12, 16, 20];
      }

      return Expanded(
        child: GestureDetector(
          onTap: () => onChanged(type),
          child: AnimatedContainer(
            duration: const Duration(milliseconds: 200),
            margin: const EdgeInsets.all(8),
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: Theme.of(context).colorScheme.surface,
              borderRadius: BorderRadius.circular(12),
              border: Border.all(
                color: isSelected
                    ? Theme.of(context).colorScheme.primary
                    : Colors.grey.shade400,
                width: isSelected ? 2 : 1,
              ),
              boxShadow: isSelected
                  ? [
                      BoxShadow(
                        color: Theme.of(context).colorScheme.primary.withOpacity(0.3),
                        blurRadius: 6,
                        offset: const Offset(0, 4),
                      ),
                    ]
                  : [],
            ),
            child: Column(
              children: [
                Text(
                  type.toUpperCase(),
                  style: TextStyle(
                    fontWeight: FontWeight.bold,
                    color: Theme.of(context).colorScheme.onSurface,
                  ),
                ),
                const SizedBox(height: 12),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: List.generate(3, (index) {
                    return AnimatedContainer(
                      duration: animationDuration,
                      margin: const EdgeInsets.symmetric(horizontal: 4),
                      height: barHeights[index],
                      width: 12,
                      decoration: BoxDecoration(
                        color: Theme.of(context).colorScheme.primary,
                        borderRadius: BorderRadius.circular(3),
                      ),
                    );
                  }),
                ),
              ],
            ),
          ),
        ),
      );
    }

    return Row(
      children: options.map(buildPreview).toList(),
    );
  }
}
