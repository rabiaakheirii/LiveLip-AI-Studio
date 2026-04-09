import 'package:flutter/material.dart';

class StreamStatusCard extends StatelessWidget {
  const StreamStatusCard({
    super.key,
    required this.running,
    required this.engine,
    required this.degraded,
    required this.message,
  });

  final bool running;
  final String engine;
  final bool degraded;
  final String message;

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        title: Text('Stream: ${running ? "Running" : "Stopped"}'),
        subtitle: Text('Engine: $engine | Mode: ${degraded ? "Degraded" : "Normal"} | $message'),
      ),
    );
  }
}
