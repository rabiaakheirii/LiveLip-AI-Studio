import 'package:flutter_live_lipsync_assistant/models/camera_device.dart';
import 'package:flutter_live_lipsync_assistant/models/pipeline_status.dart';
import 'package:flutter_live_lipsync_assistant/models/preview_chunk.dart';

class AppState {
  final PipelineStatus status;
  final String partialTranscript;
  final String finalTranscript;
  final String partialResponse;
  final String finalResponse;
  final List<String> logs;
  final bool obsConnected;
  final List<String> obsScenes;
  final Map<String, dynamic> timings;
  final String? errorMessage;

  final List<CameraDevice> cameras;
  final int selectedCameraIndex;
  final PreviewChunk? latestPreview;
  final List<PreviewChunk> previewHistory;
  final int renderProgress;
  final String previewStatus;

  const AppState({
    required this.status,
    required this.partialTranscript,
    required this.finalTranscript,
    required this.partialResponse,
    required this.finalResponse,
    required this.logs,
    required this.obsConnected,
    required this.obsScenes,
    required this.timings,
    required this.cameras,
    required this.selectedCameraIndex,
    required this.latestPreview,
    required this.previewHistory,
    required this.renderProgress,
    required this.previewStatus,
    this.errorMessage,
  });

  factory AppState.initial() => const AppState(
        status: PipelineStatus.idle,
        partialTranscript: '',
        finalTranscript: '',
        partialResponse: '',
        finalResponse: '',
        logs: [],
        obsConnected: false,
        obsScenes: [],
        timings: {},
        cameras: [],
        selectedCameraIndex: 0,
        latestPreview: null,
        previewHistory: [],
        renderProgress: 0,
        previewStatus: 'idle',
      );

  AppState copyWith({
    PipelineStatus? status,
    String? partialTranscript,
    String? finalTranscript,
    String? partialResponse,
    String? finalResponse,
    List<String>? logs,
    bool? obsConnected,
    List<String>? obsScenes,
    Map<String, dynamic>? timings,
    List<CameraDevice>? cameras,
    int? selectedCameraIndex,
    PreviewChunk? latestPreview,
    List<PreviewChunk>? previewHistory,
    int? renderProgress,
    String? previewStatus,
    String? errorMessage,
  }) {
    return AppState(
      status: status ?? this.status,
      partialTranscript: partialTranscript ?? this.partialTranscript,
      finalTranscript: finalTranscript ?? this.finalTranscript,
      partialResponse: partialResponse ?? this.partialResponse,
      finalResponse: finalResponse ?? this.finalResponse,
      logs: logs ?? this.logs,
      obsConnected: obsConnected ?? this.obsConnected,
      obsScenes: obsScenes ?? this.obsScenes,
      timings: timings ?? this.timings,
      cameras: cameras ?? this.cameras,
      selectedCameraIndex: selectedCameraIndex ?? this.selectedCameraIndex,
      latestPreview: latestPreview ?? this.latestPreview,
      previewHistory: previewHistory ?? this.previewHistory,
      renderProgress: renderProgress ?? this.renderProgress,
      previewStatus: previewStatus ?? this.previewStatus,
      errorMessage: errorMessage,
    );
  }
}
