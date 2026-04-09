class DiagnosticsSummary {
  final bool webcamAvailable;
  final bool ffmpegAvailable;
  final bool ollamaReachable;
  final bool obsReachable;
  final String selectedLipsyncEngine;
  final bool degradedMode;
  final String streamMessage;
  final String workerMode;
  final bool remoteWorkerAvailable;
  final Map<String, dynamic> engineCapabilities;

  const DiagnosticsSummary({
    required this.webcamAvailable,
    required this.ffmpegAvailable,
    required this.ollamaReachable,
    required this.obsReachable,
    required this.selectedLipsyncEngine,
    required this.degradedMode,
    required this.streamMessage,
    required this.workerMode,
    required this.remoteWorkerAvailable,
    required this.engineCapabilities,
  });

  factory DiagnosticsSummary.fromJson(Map<String, dynamic> json) {
    final cap = (json['capability'] as Map?)?.cast<String, dynamic>() ?? {};
    return DiagnosticsSummary(
      webcamAvailable: cap['webcam_available'] as bool? ?? false,
      ffmpegAvailable: cap['ffmpeg_available'] as bool? ?? false,
      ollamaReachable: cap['ollama_reachable'] as bool? ?? false,
      obsReachable: cap['obs_reachable'] as bool? ?? false,
      selectedLipsyncEngine: cap['selected_lipsync_engine'] as String? ?? 'unknown',
      degradedMode: cap['degraded_mode'] as bool? ?? false,
      streamMessage: json['stream_message'] as String? ?? 'idle',
      workerMode: json['worker_mode'] as String? ?? 'local',
      remoteWorkerAvailable: cap['remote_worker_available'] as bool? ?? false,
      engineCapabilities: (cap['engine_capabilities'] as Map?)?.cast<String, dynamic>() ?? {},
    );
  }
}
