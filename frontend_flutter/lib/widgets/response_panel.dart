import 'package:flutter/material.dart';

class ResponsePanel extends StatelessWidget {
  const ResponsePanel({
    super.key,
    required this.partialText,
    required this.finalText,
  });

  final String partialText;
  final String finalText;

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('AI Response', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            Text('Final: $finalText'),
            const SizedBox(height: 8),
            Text('Partial: $partialText', style: const TextStyle(color: Colors.white70)),
          ],
        ),
      ),
    );
  }
}
