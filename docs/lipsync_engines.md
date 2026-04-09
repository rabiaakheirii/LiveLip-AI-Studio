# LipSync Engines

## Available adapters
- mock (always available)
- ffmpeg (fallback/compositor path)
- wav2lip (experimental; dependency-gated)
- musetalk (experimental; dependency-gated)
- liveportrait (experimental; dependency-gated)

## Setup notes
- `LIPSYNC_ENGINE` selects preferred engine.
- `ENABLE_EXPERIMENTAL_ENGINES=true` required for experimental adapters.
- `LIPSYNC_MODEL_ASSETS_DIR` should contain model files when integrating real engines.

## Current status
- Real runtime inference for experimental adapters remains TODO and dependency-gated.
