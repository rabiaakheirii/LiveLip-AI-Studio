import 'package:flutter/material.dart';
import 'package:flutter_live_lipsync_assistant/widgets/stream_status_card.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('StreamStatusCard renders running text', (tester) async {
    await tester.pumpWidget(const MaterialApp(
      home: StreamStatusCard(running: true, engine: 'ffmpeg', degraded: false, message: 'ok'),
    ));

    expect(find.textContaining('Running'), findsOneWidget);
  });
}
