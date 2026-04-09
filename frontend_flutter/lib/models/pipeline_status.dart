enum PipelineStatus {
  idle,
  listening,
  transcribing,
  thinking,
  speaking,
  lipSyncing,
  streaming,
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
    default:
      return PipelineStatus.error;
  }
}
