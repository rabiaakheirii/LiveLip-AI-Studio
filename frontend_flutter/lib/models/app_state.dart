import 'package:flutter_live_lipsync_assistant/models/camera_device.dart';
import 'package:flutter_live_lipsync_assistant/models/diagnostics_summary.dart';
import 'package:flutter_live_lipsync_assistant/models/performance_metrics.dart';
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

  final bool streamRunning;
  final bool degradedMode;
  final String streamEngine;
  final double queuePressure;
  final int droppedFrames;
  final double avDriftMs;
  final bool obsLiveReady;
  final String obsLiveMode;
  final String streamMessage;
  final DiagnosticsSummary? diagnostics;
  final PerformanceMetrics? performanceMetrics;

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
    required this.streamRunning,
    required this.degradedMode,
    required this.streamEngine,
    required this.queuePressure,
    required this.droppedFrames,
    required this.avDriftMs,
    required this.obsLiveReady,
    required this.obsLiveMode,
    required this.streamMessage,
    required this.diagnostics,
    required this.performanceMetrics,
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
        streamRunning: false,
        degradedMode: false,
        streamEngine: 'ffmpeg',
        queuePressure: 0,
        droppedFrames: 0,
        avDriftMs: 0,
        obsLiveReady: false,
        obsLiveMode: 'media_source_refresh',
        streamMessage: 'idle',
        diagnostics: null,
        performanceMetrics: null,
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
    bool? streamRunning,
    bool? degradedMode,
    String? streamEngine,
    double? queuePressure,
    int? droppedFrames,
    double? avDriftMs,
    bool? obsLiveReady,
    String? obsLiveMode,
    String? streamMessage,
    DiagnosticsSummary? diagnostics,
    PerformanceMetrics? performanceMetrics,
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
      streamRunning: streamRunning ?? this.streamRunning,
      degradedMode: degradedMode ?? this.degradedMode,
      streamEngine: streamEngine ?? this.streamEngine,
      queuePressure: queuePressure ?? this.queuePressure,
      droppedFrames: droppedFrames ?? this.droppedFrames,
      avDriftMs: avDriftMs ?? this.avDriftMs,
      obsLiveReady: obsLiveReady ?? this.obsLiveReady,
      obsLiveMode: obsLiveMode ?? this.obsLiveMode,
      streamMessage: streamMessage ?? this.streamMessage,
      diagnostics: diagnostics ?? this.diagnostics,
      performanceMetrics: performanceMetrics ?? this.performanceMetrics,
      errorMessage: errorMessage,
    );
  }
}
