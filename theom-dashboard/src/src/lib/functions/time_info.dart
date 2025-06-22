import 'package:intl/intl.dart';

String getCurrentTime() {
    final now = DateTime.now();
    final time = DateFormat('hh:mm a').format(now);
    final date = DateFormat('d MMM, yyyy').format(now);
    return "$time\n$date";
}
