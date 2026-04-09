import 'package:flutter/material.dart';
import 'package:flutter_live_lipsync_assistant/models/preview_chunk.dart';
import 'package:flutter_live_lipsync_assistant/widgets/preview_panel.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('PreviewPanel renders latest URL', (tester) async {
    await tester.pumpWidget(MaterialApp(
      home: PreviewPanel(
        latest: const PreviewChunk(chunkId: '1', fileName: 'a.mp4', previewUrl: '/preview/a.mp4', source: 'webcam'),
        history: const [],
        backendBaseUrl: 'http://127.0.0.1:8000',
      ),
    ));

    expect(find.textContaining('Latest preview URL'), findsOneWidget);
  });
}
