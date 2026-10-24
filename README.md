# VidSNAP: images and narration to reels

A local Flask learning project that turns uploaded images and a written narration into a vertical MP4. The text is sent to ElevenLabs for speech; a separate Python worker combines that audio and the images with FFmpeg. The gallery lists generated reels.

[ReelsGenerator](https://github.com/harshgavandit/ReelsGenerator) preserves a substantially overlapping copy. This repository is the preferred place to inspect the application and setup. It does not implement video-content analysis.

## Implemented flow

1. [main.py](main.py) serves the home, create and gallery pages. The create form writes uploaded files, `desc.txt` and an FFmpeg `input.txt` into a job folder under `user_uploads/`.
2. [generate_process.py](generate_process.py) checks folders against `done.txt` every four seconds. New folders are passed to the narration helper and then to FFmpeg.
3. [text_to_audio.py](text_to_audio.py) requests ElevenLabs speech and writes `audio.mp3`. FFmpeg scales/pads images to 1080 × 1920, combines them with the audio, and writes a 30 fps MP4 into `static/reels/`.

The web server and worker are separate processes. Starting Flask alone does not generate a reel.

## Local setup

Prerequisites: Python, FFmpeg available on `PATH`, and your own ElevenLabs account/key for narration. Narration sends the supplied text to that external service and can consume its quota. The repository does not pin a tested Python/SDK environment.

Run from the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install flask elevenlabs
ffmpeg -version
python main.py
```

Open <http://127.0.0.1:5000>. In a second terminal, activate the same environment and start the worker with your own local configuration:

```powershell
.\.venv\Scripts\Activate.ps1
$env:ELEVENLABS_API_KEY = "replace_with_your_own_key"
python generate_process.py
```

On macOS/Linux, activate with `source .venv/bin/activate` and use `export ELEVENLABS_API_KEY="replace_with_your_own_key"` before starting the worker. [config.py](config.py) reads the process environment and rejects a missing or blank key. [.env.example](.env.example) lists the variable name; these scripts do not automatically load `.env` files. Keep credentials out of tracked files.

Create a reel using images and narration text, leave both processes running, then refresh the gallery after processing. The worker scans every unprocessed folder already present in `user_uploads/`, so inspect that folder and `done.txt` before starting it. They contain retained sample/history files.

## Offline checks and limits

```powershell
python -m unittest discover -s tests -v
python -m compileall -q config.py main.py generate_process.py text_to_audio.py
```

The configuration tests use synthetic environment values and make no provider calls. This curation checked the source, configuration boundary and syntax; it did not make a new speech request or render a new reel.

This is a local demonstration: Flask starts in debug mode; jobs use folders and a text completion log rather than a durable queue; the worker has no retry or per-job recovery handling. There is no authentication, upload-size enforcement or verified production deployment. Existing media and processing logs remain in Git history; ignore rules keep new local runtime files out of future additions. A credential literal was removed from the current configuration, but deleting it from source does not revoke historical copies.
