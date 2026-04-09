import 'package:flutter_live_lipsync_assistant/models/app_state.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  test('AppState.initial has stream defaults', () {
    final state = AppState.initial();
    expect(state.streamRunning, false);
    expect(state.streamEngine, isNotEmpty);
  });
}
