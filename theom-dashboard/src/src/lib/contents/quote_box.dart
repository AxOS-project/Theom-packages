import 'package:flutter/material.dart';
import '../functions/quote_info.dart';
import '../widgets/card_box.dart';

class QuoteBox extends StatefulWidget {
  const QuoteBox({super.key});

  @override
  State<QuoteBox> createState() => _QuoteBoxState();
}

class _QuoteBoxState extends State<QuoteBox> {
  String quote = '...';

  @override
  void initState() {
    super.initState();
    _loadQuote();
  }

  void _loadQuote() async {
    final q = await getRandomQuote();
    setState(() {
      quote = '"${q.quote}"\n${q.author}';
    });
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return CardBox(
      color: theme.colorScheme.surface, // theme-driven background
      child: Center(
        child: Text(
          quote,
          textAlign: TextAlign.center,
          style: theme.textTheme.bodyMedium?.copyWith(
            fontStyle: FontStyle.italic,
            fontWeight: FontWeight.w400,
          ),
        ),
      ),
    );
  }
}
