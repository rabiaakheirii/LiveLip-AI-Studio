import 'package:flutter/material.dart';
import 'package:flutter_live_lipsync_assistant/widgets/obs_live_status_card.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('OBSLiveStatusCard renders mode', (tester) async {
    await tester.pumpWidget(const MaterialApp(home: OBSLiveStatusCard(ready: true, mode: 'media_source_refresh')));
    expect(find.textContaining('media_source_refresh'), findsOneWidget);
  });
}
