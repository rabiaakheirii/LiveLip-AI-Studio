import 'package:flutter/material.dart';
import 'package:flutter_live_lipsync_assistant/models/camera_device.dart';
import 'package:flutter_live_lipsync_assistant/widgets/camera_selector.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('CameraSelector renders camera names', (tester) async {
    await tester.pumpWidget(MaterialApp(
      home: CameraSelector(
        cameras: const [CameraDevice(id: 'c0', index: 0, name: 'Cam 0', available: true)],
        selectedIndex: 0,
        onSelected: (_) {},
      ),
    ));

    expect(find.textContaining('Cam 0'), findsOneWidget);
  });
}
