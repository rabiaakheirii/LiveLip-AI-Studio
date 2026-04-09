import 'dart:async';

import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_live_lipsync_assistant/models/app_state.dart';
import 'package:flutter_live_lipsync_assistant/models/camera_device.dart';
import 'package:flutter_live_lipsync_assistant/models/pipeline_status.dart';
import 'package:flutter_live_lipsync_assistant/models/preview_chunk.dart';
import 'package:flutter_live_lipsync_assistant/services/api_service.dart';
import 'package:flutter_live_lipsync_assistant/services/websocket_service.dart';

final apiServiceProvider = Provider((ref) => ApiService());
final wsServiceProvider = Provider((ref) => WebSocketService());

final appControllerProvider = StateNotifierProvider<AppController, AppState>((ref) {
  return AppController(
    apiService: ref.read(apiServiceProvider),
    wsService: ref.read(wsServiceProvider),
  );
});

class AppController extends StateNotifier<AppState> {
  AppController({required ApiService apiService, required WebSocketService wsService})
      : _apiService = apiService,
        _wsService = wsService,
        super(AppState.initial());

  final ApiService _apiService;
  final WebSocketService _wsService;
  StreamSubscription<Map<String, dynamic>>? _subscription;

  void initialize() {
    _wsService.connect();
    _subscription ??= _wsService.events.listen(_handleEvent);
    unawaited(refreshCameras());
  }

  Future<void> start() async {
    await _apiService.startPipeline();
  }

  Future<void> stop() async {
    await _apiService.stopPipeline();
  }

  Future<void> refreshCameras() async {
    try {
      final payload = await _apiService.getCameraDevices();
      final items = ((payload['items'] as List?) ?? [])
          .map((e) => CameraDevice.fromJson((e as Map).cast<String, dynamic>()))
          .toList();
      state = state.copyWith(cameras: items, selectedCameraIndex: payload['selected_index'] as int? ?? 0);
    } catch (e) {
      state = state.copyWith(logs: [...state.logs, 'refreshCameras failed: $e']);
    }
  }

  Future<void> selectCamera(int index) async {
    await _apiService.selectCamera(index);
    state = state.copyWith(selectedCameraIndex: index);
  }

  void _handleEvent(Map<String, dynamic> event) {
    final type = event['event_type'] as String? ?? '';
    final data = (event['data'] as Map?)?.cast<String, dynamic>() ?? <String, dynamic>{};

    switch (type) {
      case 'pipeline_state':
        state = state.copyWith(status: pipelineStatusFromString(data['state'] as String? ?? 'error'));
        break;
      case 'transcript_partial':
        state = state.copyWith(partialTranscript: data['text'] as String? ?? '');
        break;
      case 'transcript_final':
        state = state.copyWith(finalTranscript: data['text'] as String? ?? '', partialTranscript: '');
        break;
      case 'ai_response_partial':
        state = state.copyWith(partialResponse: data['text'] as String? ?? '');
        break;
      case 'ai_response_final':
        state = state.copyWith(finalResponse: data['text'] as String? ?? '', partialResponse: '');
        break;
      case 'obs_status':
        state = state.copyWith(
          obsConnected: data['connected'] as bool? ?? false,
          obsScenes: ((data['scenes'] as List?) ?? []).map((e) => e.toString()).toList(),
        );
        break;
      case 'pipeline_timing':
        state = state.copyWith(timings: data);
        break;
      case 'camera_list':
        final cameras = ((data['cameras'] as List?) ?? [])
            .map((e) => CameraDevice.fromJson((e as Map).cast<String, dynamic>()))
            .toList();
        state = state.copyWith(cameras: cameras, selectedCameraIndex: data['selected_index'] as int? ?? 0);
        break;
      case 'camera_selected':
        state = state.copyWith(selectedCameraIndex: data['index'] as int? ?? state.selectedCameraIndex);
        break;
      case 'preview_chunk_ready':
        final chunk = PreviewChunk.fromJson(data);
        final history = [chunk, ...state.previewHistory].take(10).toList();
        state = state.copyWith(latestPreview: chunk, previewHistory: history, previewStatus: 'ready');
        break;
      case 'preview_status':
        state = state.copyWith(previewStatus: (data['ready'] == true) ? 'ready' : 'pending');
        break;
      case 'render_progress':
        state = state.copyWith(renderProgress: data['progress'] as int? ?? 0, previewStatus: data['stage'] as String? ?? 'rendering');
        break;
      case 'render_error':
        state = state.copyWith(previewStatus: 'error', errorMessage: data['message'] as String? ?? 'render error');
        break;
      case 'error':
        state = state.copyWith(errorMessage: data['message'] as String? ?? 'Unknown error', status: PipelineStatus.error);
        break;
      default:
        final nextLogs = [...state.logs, '$type: $data'];
        state = state.copyWith(logs: nextLogs.take(200).toList());
    }
  }

  @override
  void dispose() {
    _subscription?.cancel();
    _wsService.dispose();
    super.dispose();
  }
}
