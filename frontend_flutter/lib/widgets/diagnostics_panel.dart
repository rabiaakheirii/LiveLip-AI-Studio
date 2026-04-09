import 'package:flutter/material.dart';
import 'package:flutter_live_lipsync_assistant/models/diagnostics_summary.dart';

class DiagnosticsPanel extends StatelessWidget {
  const DiagnosticsPanel({super.key, required this.summary});

  final DiagnosticsSummary? summary;

  @override
  Widget build(BuildContext context) {
    final s = summary;
    if (s == null) {
      return const Card(child: ListTile(title: Text('Diagnostics unavailable')));
    }
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Diagnostics', style: TextStyle(fontWeight: FontWeight.bold)),
            Text('Worker mode: ${s.workerMode} | Remote worker: ${s.remoteWorkerAvailable}'),
            Text('Webcam: ${s.webcamAvailable} | FFmpeg: ${s.ffmpegAvailable}'),
            Text('Ollama: ${s.ollamaReachable} | OBS: ${s.obsReachable}'),
            Text('Engine: ${s.selectedLipsyncEngine} | Degraded: ${s.degradedMode}'),
            Text('Engine capabilities: ${s.engineCapabilities}'),
            Text('Stream message: ${s.streamMessage}'),
          ],
        ),
      ),
    );
  }
}
