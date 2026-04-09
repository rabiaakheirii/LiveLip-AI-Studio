enum PipelineStatus {
  idle,
  listening,
  transcribing,
  thinking,
  speaking,
  lipSyncing,
  streaming,
  cameraReady,
  capturingVideo,
  renderingPreview,
  previewReady,
  error,
}

PipelineStatus pipelineStatusFromString(String value) {
  switch (value) {
    case 'idle':
      return PipelineStatus.idle;
    case 'listening':
      return PipelineStatus.listening;
    case 'transcribing':
      return PipelineStatus.transcribing;
    case 'thinking':
      return PipelineStatus.thinking;
    case 'speaking':
      return PipelineStatus.speaking;
    case 'lip_syncing':
      return PipelineStatus.lipSyncing;
    case 'streaming':
      return PipelineStatus.streaming;
    case 'camera_ready':
      return PipelineStatus.cameraReady;
    case 'capturing_video':
      return PipelineStatus.capturingVideo;
    case 'rendering_preview':
      return PipelineStatus.renderingPreview;
    case 'preview_ready':
      return PipelineStatus.previewReady;
    default:
      return PipelineStatus.error;
  }
}
