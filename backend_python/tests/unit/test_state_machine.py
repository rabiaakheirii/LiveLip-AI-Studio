import pytest

from app.core.events import PipelineState
from app.core.state_machine import PipelineStateMachine


def test_state_machine_stream_transition_chain():
    sm = PipelineStateMachine()
    sm.transition(PipelineState.stream_initializing)
    sm.transition(PipelineState.streaming_live)
    sm.transition(PipelineState.syncing_av)
    sm.transition(PipelineState.obs_output_ready)
    sm.transition(PipelineState.idle)
    assert sm.state == PipelineState.idle


def test_state_machine_invalid_transition_raises():
    sm = PipelineStateMachine()
    with pytest.raises(ValueError):
        sm.transition(PipelineState.thinking)
