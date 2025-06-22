import 'package:flutter/material.dart';

void confirmAction(BuildContext context, String title, Future<void> Function() action) {
  showDialog(
    context: context,
    builder: (context) => AlertDialog(
      title: Text(title),
      content: const Text("Are you sure you want to continue?"),
      actions: [
        TextButton(
          onPressed: () => Navigator.pop(context),
          child: const Text("Cancel"),
        ),
        ElevatedButton(
          onPressed: () {
            Navigator.pop(context);
            action();
          },
          child: const Text("Yes"),
        ),
      ],
    ),
  );
}
