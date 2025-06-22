import 'package:flutter/material.dart';
import '../functions/user_info.dart';
import 'dart:io';

class UserBox extends StatefulWidget {
  const UserBox({super.key});

  @override
  State<UserBox> createState() => _UserBoxState();
}

class _UserBoxState extends State<UserBox> {
  String username = '...';
  ImageProvider? _userImage;

  @override
  void initState() {
    super.initState();
    _loadUsername();
    _loadUserImage();
  }

  void _loadUsername() async {
    final name = await getUsername();
    setState(() => username = name);
  }

  void _loadUserImage() {
    final home = Platform.environment['HOME'];
    if (home != null) {
      final file = File('$home/.config/theom/desktop/user/user.png');
      if (file.existsSync()) {
        setState(() {
          _userImage = FileImage(file);
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        CircleAvatar(
          radius: 40,
          backgroundColor: Colors.grey.shade800,
          backgroundImage: _userImage,
          child: _userImage == null
              ? const Icon(Icons.account_circle, size: 40, color: Colors.white70)
              : null,
        ),
        const SizedBox(height: 10),
        const Text(
          "Welcome",
          style: TextStyle(
            fontSize: 22,
            fontWeight: FontWeight.w600,
          ),
        ),
        Text(
          "$username!",
          style: const TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.w500,
            //color: Colors.white70,
          ),
        ),
      ],
    );
  }
}
