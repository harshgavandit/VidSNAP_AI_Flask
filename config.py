"""Local narration configuration; credentials are never stored in source."""
import os

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "").strip()
if not ELEVENLABS_API_KEY:
    raise RuntimeError("Set ELEVENLABS_API_KEY in your local environment before starting narration.")
