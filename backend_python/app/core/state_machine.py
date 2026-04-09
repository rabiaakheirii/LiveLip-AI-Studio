from __future__ import annotations

from typing import Dict, Set

from app.core.events import PipelineState


class PipelineStateMachine:
    _allowed_transitions: Dict[PipelineState, Set[PipelineState]] = {
        PipelineState.idle: {PipelineState.listening, PipelineState.error},
        PipelineState.listening: {PipelineState.transcribing, PipelineState.idle, PipelineState.error},
        PipelineState.transcribing: {PipelineState.thinking, PipelineState.listening, PipelineState.error},
        PipelineState.thinking: {PipelineState.speaking, PipelineState.error},
        PipelineState.speaking: {PipelineState.lip_syncing, PipelineState.streaming, PipelineState.error},
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
