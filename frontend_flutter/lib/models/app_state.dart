import 'package:flutter_live_lipsync_assistant/models/pipeline_status.dart';

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
      errorMessage: errorMessage,
    );
  }
}
