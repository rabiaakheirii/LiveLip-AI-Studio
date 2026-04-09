class PerformanceMetrics {
  final double fpsActual;
  final int framesProcessed;
  final int framesDropped;
  final double queuePressure;
  final bool adaptiveDegraded;
  final Map<String, dynamic> stageTiming;

  const PerformanceMetrics({
    required this.fpsActual,
    required this.framesProcessed,
    required this.framesDropped,
    required this.queuePressure,
    required this.adaptiveDegraded,
    required this.stageTiming,
  });

  factory PerformanceMetrics.fromJson(Map<String, dynamic> json) {
    return PerformanceMetrics(
      fpsActual: (json['fps_actual'] as num?)?.toDouble() ?? 0,
      framesProcessed: json['frames_processed'] as int? ?? 0,
      framesDropped: json['frames_dropped'] as int? ?? 0,
      queuePressure: (json['queue_pressure'] as num?)?.toDouble() ?? 0,
      adaptiveDegraded: json['adaptive_degraded'] as bool? ?? false,
      stageTiming: (json['stage_timing'] as Map?)?.cast<String, dynamic>() ?? {},
    );
  }
}
