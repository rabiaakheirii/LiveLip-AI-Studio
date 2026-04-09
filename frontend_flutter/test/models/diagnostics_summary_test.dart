import 'package:flutter_live_lipsync_assistant/models/diagnostics_summary.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  test('DiagnosticsSummary.fromJson parses capability', () {
    final model = DiagnosticsSummary.fromJson({
      'stream_message': 'ok',
      'capability': {
        'webcam_available': true,
        'ffmpeg_available': true,
        'ollama_reachable': false,
        'obs_reachable': true,
        'selected_lipsync_engine': 'ffmpeg',
        'degraded_mode': false,
      }
    });

    expect(model.webcamAvailable, true);
    expect(model.selectedLipsyncEngine, 'ffmpeg');
  });
}
