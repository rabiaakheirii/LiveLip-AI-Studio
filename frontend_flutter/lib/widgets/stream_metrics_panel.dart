import 'package:flutter/material.dart';

class StreamMetricsPanel extends StatelessWidget {
  const StreamMetricsPanel({
    super.key,
    required this.queuePressure,
    required this.droppedFrames,
    required this.avDriftMs,
  });

  final double queuePressure;
  final int droppedFrames;
  final double avDriftMs;

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Stream Metrics', style: TextStyle(fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            Text('Queue Pressure: ${(queuePressure * 100).toStringAsFixed(1)}%'),
            Text('Dropped Frames: $droppedFrames'),
            Text('AV Drift: ${avDriftMs.toStringAsFixed(2)} ms'),
          ],
        ),
      ),
    );
  }
}
