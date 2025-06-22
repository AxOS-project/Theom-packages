import 'dart:convert';
import 'dart:io';
import 'dart:math';

class Quote {
  final String quote;
  final String author;

  Quote({required this.quote, required this.author});

  factory Quote.fromJson(Map<String, dynamic> json) {
    return Quote(
      quote: json['quote'] ?? '',
      author: json['author'] ?? '',
    );
  }
}

Future<Quote> getRandomQuote() async {
  try {
    final file = File('lib/quotes.json');
    if (!await file.exists()) {
      return Quote(quote: "No quotes available.", author: "");
    }

    final content = await file.readAsString();
    final List<dynamic> data = jsonDecode(content);

    final quotes = data.map((e) => Quote.fromJson(e)).toList();
    if (quotes.isEmpty) {
      return Quote(quote: "No quotes available.", author: "");
    }

    final random = Random();
    return quotes[random.nextInt(quotes.length)];
  } catch (e) {
    return Quote(quote: "Error reading quotes.", author: "");
  }
}
