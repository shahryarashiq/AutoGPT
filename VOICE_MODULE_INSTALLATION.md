# Voice Module Installation Guide

## Overview

The voice module for AutoGPT Classic provides Text-to-Speech (TTS) functionality, allowing the agent to speak responses aloud. This guide explains how to install and use the voice module.

## Installation

The voice module has been successfully installed! The following packages are now available:

- **gTTS** (Google Text-to-Speech) v2.5.1 - Default TTS provider
- **playsound** v1.2.2 - Audio playback library

### Installation Steps

To install the voice module dependencies:

```bash
cd classic/forge
poetry install
```

This will install all required packages including the voice module dependencies.

## Available TTS Providers

The voice module supports multiple Text-to-Speech providers:

### 1. Google Text-to-Speech (gTTS) - Default
- **Provider ID**: `gtts`
- **Requirements**: Internet connection
- **Cost**: Free
- **Setup**: No additional configuration needed

### 2. ElevenLabs
- **Provider ID**: `elevenlabs`
- **Requirements**: ElevenLabs API key
- **Cost**: Paid service (free tier available)
- **Setup**: Configure environment variables:
  - `ELEVENLABS_API_KEY`: Your API key
  - `ELEVENLABS_VOICE_ID`: Voice ID (e.g., "Rachel", "Adam")

### 3. macOS TTS
- **Provider ID**: `macos`
- **Requirements**: macOS operating system
- **Cost**: Free
- **Setup**: No additional configuration needed

### 4. StreamElements
- **Provider ID**: `streamelements`
- **Requirements**: Internet connection
- **Cost**: Free
- **Setup**: No additional configuration needed

## Usage

### Command Line

To enable Text-to-Speech when running AutoGPT:

```bash
./autogpt.sh --speak
```

### Configuration

You can configure the TTS provider in your `.env` file:

```bash
# Enable speak mode
SPEAK_MODE=true

# Choose TTS provider (gtts, elevenlabs, macos, streamelements)
TEXT_TO_SPEECH_PROVIDER=gtts

# For ElevenLabs (optional)
ELEVENLABS_API_KEY=your_api_key_here
ELEVENLABS_VOICE_ID=Rachel
```

### Programmatic Usage

```python
from forge.speech.say import TextToSpeechProvider, TTSConfig

# Create configuration
config = TTSConfig(
    speak_mode=True,
    provider="gtts"  # or "elevenlabs", "macos", "streamelements"
)

# Initialize provider
tts = TextToSpeechProvider(config)

# Say something (when speak_mode is True)
tts.say("Hello, I am AutoGPT!")
```

## Verification

To verify the voice module is installed correctly:

```bash
cd classic/forge
poetry run python -c "from forge.speech.say import TextToSpeechProvider, TTSConfig; print('✅ Voice module installed successfully!')"
```

## Troubleshooting

### Audio Playback Issues

If you encounter issues with audio playback:

1. **Linux**: Ensure you have a sound system installed (ALSA, PulseAudio, etc.)
2. **macOS**: Audio should work out of the box
3. **Windows**: Windows Sound System should be enabled

### Import Errors

If you see import errors, ensure dependencies are installed:

```bash
cd classic/forge
poetry install
```

### ElevenLabs Authentication

If using ElevenLabs, verify your API key is valid:
1. Visit [ElevenLabs](https://beta.elevenlabs.io/)
2. Check your API key in Profile settings
3. Ensure the key is correctly set in `.env`

## Available Voices (ElevenLabs)

| Name   | Voice ID                  |
|--------|---------------------------|
| Rachel | `21m00Tcm4TlvDq8ikWAM`    |
| Domi   | `AZnzlk1XvdvUeBnXmlld`    |
| Bella  | `EXAVITQu4vr4xnSDxMaL`    |
| Antoni | `ErXwobaYiN019PkySvjV`    |
| Elli   | `MF3mGyEYCl7XYWbV9V6O`    |
| Josh   | `TxGEqnHWrfWFTfGW9XjX`    |
| Arnold | `VR6AewLTigWG4xSOukaG`    |
| Adam   | `pNInz6obpgDQGcFmaJgB`    |
| Sam    | `yoZ06aMxZJJ28mfd3POQ`    |

## Additional Resources

- [Voice Configuration Documentation](docs/content/classic/configuration/voice.md)
- [AutoGPT Classic Documentation](docs/)
- [ElevenLabs API Documentation](https://docs.elevenlabs.io/)

## Notes

- The voice module is part of AutoGPT Classic, which is no longer actively maintained
- For production use, consider using the [AutoGPT Platform](/autogpt_platform)
- Audio files are temporarily created and deleted after playback
- Network connectivity is required for online TTS providers (gTTS, ElevenLabs, StreamElements)
