import 'package:flutter/material.dart';
import 'package:flutter_live_lipsync_assistant/models/preview_chunk.dart';

class PreviewPanel extends StatelessWidget {
  const PreviewPanel({
    super.key,
    required this.latest,
    required this.history,
    required this.backendBaseUrl,
  });

  final PreviewChunk? latest;
  final List<PreviewChunk> history;
  final String backendBaseUrl;

  @override
  Widget build(BuildContext context) {
    final latestUrl = latest == null ? null : '$backendBaseUrl${latest!.previewUrl}';

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Preview Output', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            Text(latestUrl == null ? 'No preview chunk yet' : 'Latest preview URL: $latestUrl'),
            const SizedBox(height: 8),
            const Text('Recent Chunks:'),
            for (final chunk in history.take(5))
              Text('- ${chunk.fileName} (${chunk.source})', style: const TextStyle(color: Colors.white70)),
          ],
        ),
      ),
    );
  }
}
