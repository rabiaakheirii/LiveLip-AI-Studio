import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_live_lipsync_assistant/models/preview_chunk.dart';
import 'package:flutter_live_lipsync_assistant/state/app_controller.dart';

final latestPreviewProvider = Provider<PreviewChunk?>((ref) {
  return ref.watch(appControllerProvider).latestPreview;
});
