from __future__ import annotations

from typing import Dict, Set

from app.core.events import PipelineState


class PipelineStateMachine:
    _allowed_transitions: Dict[PipelineState, Set[PipelineState]] = {
        PipelineState.idle: {PipelineState.listening, PipelineState.camera_ready, PipelineState.stream_initializing, PipelineState.error},
        PipelineState.listening: {PipelineState.transcribing, PipelineState.idle, PipelineState.error},
        PipelineState.transcribing: {PipelineState.thinking, PipelineState.listening, PipelineState.error},
        PipelineState.thinking: {PipelineState.speaking, PipelineState.error},
        PipelineState.speaking: {PipelineState.lip_syncing, PipelineState.streaming, PipelineState.camera_ready, PipelineState.error},
        PipelineState.camera_ready: {PipelineState.capturing_video, PipelineState.rendering_preview, PipelineState.error},
        PipelineState.capturing_video: {PipelineState.rendering_preview, PipelineState.error},
        PipelineState.rendering_preview: {PipelineState.preview_ready, PipelineState.error},
        PipelineState.preview_ready: {PipelineState.streaming, PipelineState.idle, PipelineState.error},
        PipelineState.stream_initializing: {PipelineState.streaming_live, PipelineState.degraded_mode, PipelineState.error},
        PipelineState.streaming_live: {PipelineState.syncing_av, PipelineState.obs_output_ready, PipelineState.idle, PipelineState.error},
        PipelineState.syncing_av: {PipelineState.obs_output_ready, PipelineState.streaming_live, PipelineState.degraded_mode, PipelineState.error},
        PipelineState.obs_output_ready: {PipelineState.streaming_live, PipelineState.degraded_mode, PipelineState.idle, PipelineState.error},
        PipelineState.degraded_mode: {PipelineState.streaming_live, PipelineState.idle, PipelineState.error},
        PipelineState.lip_syncing: {PipelineState.streaming, PipelineState.error},
        PipelineState.streaming: {PipelineState.listening, PipelineState.idle, PipelineState.error},
        PipelineState.error: {PipelineState.idle},
    }

    def __init__(self) -> None:
        self._state = PipelineState.idle

    @property
    def state(self) -> PipelineState:
        return self._state

    def can_transition(self, next_state: PipelineState) -> bool:
        return next_state in self._allowed_transitions[self._state]

    def transition(self, next_state: PipelineState) -> PipelineState:
        if not self.can_transition(next_state):
            raise ValueError(f"Invalid state transition: {self._state} -> {next_state}")
        self._state = next_state
        return self._state

    def force_error(self) -> PipelineState:
        self._state = PipelineState.error
        return self._state
