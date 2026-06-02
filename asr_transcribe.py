import json
import mimetypes
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path


DEEPGRAM_API_URL = "https://api.deepgram.com/v1/listen"
OUTPUT_FOLDER = Path("output")


def load_env_file(env_file: Path = Path(".env")) -> None:
    if not env_file.exists():
        return

    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        if key and key not in os.environ:
            os.environ[key] = value


def transcribe_audio(audio_file: Path) -> dict:
    api_key = os.getenv("DEEPGRAM_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Please add DEEPGRAM_API_KEY to .env or set it in PowerShell."
        )

    if not audio_file.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_file}")

    content_type, _ = mimetypes.guess_type(audio_file)
    content_type = content_type or "application/octet-stream"

    query = urllib.parse.urlencode(
        {
            "model": "nova-3",
            "smart_format": "true",
            "punctuate": "true",
        }
    )

    request = urllib.request.Request(
        url=f"{DEEPGRAM_API_URL}?{query}",
        data=audio_file.read_bytes(),
        headers={
            "Authorization": f"Token {api_key}",
            "Content-Type": content_type,
        },
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=120) as response:
        return json.loads(response.read().decode("utf-8"))


def save_json(data: dict, audio_file: Path) -> Path:
    OUTPUT_FOLDER.mkdir(exist_ok=True)
    output_file = OUTPUT_FOLDER / f"{audio_file.stem}.json"
    output_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return output_file


def get_transcript(data: dict) -> str:
    channels = data.get("results", {}).get("channels", [])
    if not channels:
        return ""

    alternatives = channels[0].get("alternatives", [])
    if not alternatives:
        return ""

    return alternatives[0].get("transcript", "")


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python asr_transcribe.py path/to/audio_file.wav")
        raise SystemExit(1)

    load_env_file()

    audio_file = Path(sys.argv[1])
    result = transcribe_audio(audio_file)
    output_file = save_json(result, audio_file)
    transcript = get_transcript(result)

    print(f"Transcription JSON saved to: {output_file}")
    print("\nTranscript:")
    print(transcript or "No transcript found in the response.")


if __name__ == "__main__":
    main()
