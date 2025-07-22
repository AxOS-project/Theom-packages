import 'package:flutter/material.dart';
import 'dart:io';
import 'package:file_picker/file_picker.dart';

class WallpaperSelectorTile extends StatelessWidget {
  final String wallpaperPath;
  final ValueChanged<String> onChange;

  const WallpaperSelectorTile({
    required this.wallpaperPath,
    required this.onChange,
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () async {
            final result = await FilePicker.platform.pickFiles(type: FileType.image);
            if (result != null && result.files.single.path != null) {
                onChange(result.files.single.path!);
            }
        },

      child: Container(
        height: 120,
        margin: EdgeInsets.all(8),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(16),
          image: wallpaperPath.isNotEmpty
              ? DecorationImage(
                  image: FileImage(File(wallpaperPath)),
                  fit: BoxFit.cover,
                )
              : null,
          color: Colors.grey[300],
          border: Border.all(
            color: Theme.of(context).colorScheme.primary,
            width: 2,
          ),
        ),
        child: Stack(
          children: [
            if (wallpaperPath.isEmpty)
              Center(
                child: Text(
                  "No Wallpaper Selected",
                  style: TextStyle(
                    color: Colors.grey[700],
                    fontWeight: FontWeight.w500,
                  ),
                ),
              ),
            Positioned(
              bottom: 8,
              right: 8,
              child: Container(
                padding: EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                decoration: BoxDecoration(
                  color: Colors.black.withOpacity(0.5),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Text(
                  "Change",
                  style: TextStyle(
                    color: Colors.white,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            )
          ],
        ),
      ),
    );
  }
}
