import 'package:flutter/material.dart';
import 'widgets/card_box.dart';
import 'widgets/rounded_box.dart';
import 'widgets/skewed_box.dart';
import 'widgets/compact_slider.dart';
import 'widgets/confirm_action.dart';
import 'contents/user_box.dart';
import 'contents/time_box.dart';
import 'contents/uptime_box.dart';
import 'contents/volume_box.dart';
import 'contents/brightness_box.dart';
import 'contents/system_info_box.dart';
import 'contents/weather_box.dart';
import 'contents/quote_box.dart';

import 'functions/system_actions.dart';

class DashboardPage extends StatelessWidget {
  const DashboardPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Column(
          children: [
            // ───── Row 1: Uptime + Actions ─────
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
              child: Row(
                children: [
                  Expanded(
                      child: Padding(
                        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                        child: UptimeBox(),
                      ),
                    ),
                  const SizedBox(width: 12),
                  Row(
                    children: [
                      IconButton(
                        icon: const Icon(Icons.power_settings_new),
                        onPressed: () => confirmAction(context, "Shut Down", shutdownSystem),
                      ),
                      IconButton(
                        icon: const Icon(Icons.restart_alt),
                        onPressed: () => confirmAction(context, "Reboot", rebootSystem),
                      ),
                      IconButton(
                        icon: const Icon(Icons.logout),
                        onPressed: () => confirmAction(context, "Log Out", logoutUser),
                      ),
                    ],
                  ),
                ],
              ),
            ),

            const SizedBox(height: 4),

            // ───── Row 2: User | Time | Weather | Quote ─────
            Expanded(
              flex: 3,
              child: Row(
                children: [
                  // User
                  Expanded(
                    flex: 2,
                    child: Padding(
                      padding: const EdgeInsets.all(8),
                      child: RoundedBox(
                        child: const UserBox(),
                      ),

                    ),
                  ),

                  // Time
                  Expanded(
                    flex: 2,
                    child: Padding(
                      padding: const EdgeInsets.all(8),
                      child: TimeBox(),
                    ),
                  ),

                  // Weather
                  Expanded(
                    flex: 2,
                    child: Padding(
                      padding: const EdgeInsets.all(8),
                      child: SizedBox(
                        height: double.infinity,
                        child: const WeatherBox(),
                      ),
                    ),
                  ),


                  // Quote
                  Expanded(
                    flex: 4,
                    child: Padding(
                      padding: const EdgeInsets.all(8),
                      child: CardBox(
                        child: const QuoteBox(),
                      ),
                    ),
                  ),
                ],
              ),
            ),

            // ───── Row 3: Sys Info + Sliders ─────
            Expanded(
              flex: 3,
              child: Row(
                children: [
                  // System Info
                  Expanded(
                    flex: 6,
                    child: Padding(
                      padding: const EdgeInsets.all(8),
                      child: const SystemInfoBox(),
                    ),
                  ),


                  // Sliders (stacked vertically)
                  Expanded(
                    flex: 4,
                    child: Padding(
                      padding: const EdgeInsets.all(8),
                      child: Column(
                        children: const [
                          Expanded(child: VolumeSlider()),
                          SizedBox(height: 12),
                          Expanded(child: BrightnessBox()),
                        ],
                      ),
                    ),
                  ),

                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
