import 'package:flutter/material.dart';
import 'package:flutter_live_lipsync_assistant/models/performance_metrics.dart';

class PerformanceMetricsPanel extends StatelessWidget {
  const PerformanceMetricsPanel({super.key, required this.metrics});

  final PerformanceMetrics? metrics;

  @override
  Widget build(BuildContext context) {
    if (metrics == null) {
      return const Card(child: ListTile(title: Text('Performance metrics unavailable')));
    }
    final m = metrics!;
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Performance', style: TextStyle(fontWeight: FontWeight.bold)),
            Text('FPS: ${m.fpsActual} | Processed: ${m.framesProcessed} | Dropped: ${m.framesDropped}'),
            Text('Queue pressure: ${(m.queuePressure * 100).toStringAsFixed(1)}% | Adaptive degraded: ${m.adaptiveDegraded}'),
            Text('Stage timing (ms): ${m.stageTiming}'),
          ],
        ),
      ),
    );
  }
}
