class StreamStatus {
  final bool running;
  final bool degradedMode;
  final String lipsyncEngine;
  final int targetFps;
  final int captureQueueSize;
  final int droppedFrames;
  final double queuePressure;
  final double avDriftMs;
  final bool obsLiveReady;
  final String message;

  const StreamStatus({
    required this.running,
    required this.degradedMode,
    required this.lipsyncEngine,
    required this.targetFps,
    required this.captureQueueSize,
    required this.droppedFrames,
    required this.queuePressure,
    required this.avDriftMs,
    required this.obsLiveReady,
    required this.message,
  });

  factory StreamStatus.fromJson(Map<String, dynamic> json) => StreamStatus(
        running: json['running'] as bool? ?? false,
        degradedMode: json['degraded_mode'] as bool? ?? false,
        lipsyncEngine: json['lipsync_engine'] as String? ?? 'unknown',
        targetFps: json['target_fps'] as int? ?? 0,
        captureQueueSize: json['capture_queue_size'] as int? ?? 0,
        droppedFrames: json['dropped_frames'] as int? ?? 0,
        queuePressure: (json['queue_pressure'] as num?)?.toDouble() ?? 0.0,
        avDriftMs: (json['av_drift_ms'] as num?)?.toDouble() ?? 0.0,
        obsLiveReady: json['obs_live_ready'] as bool? ?? false,
        message: json['message'] as String? ?? 'idle',
      );
}
