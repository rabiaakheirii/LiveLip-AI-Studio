class StreamMetrics {
  final int droppedFrames;
  final double queuePressure;
  final double avDriftMs;

  const StreamMetrics({required this.droppedFrames, required this.queuePressure, required this.avDriftMs});
}
