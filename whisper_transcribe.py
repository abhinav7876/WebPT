import json
import os
import sys
from pathlib import Path

from openai import OpenAI


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
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("Please add OPENAI_API_KEY to .env or set it in PowerShell.")

    if not audio_file.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_file}")

    client = OpenAI()

    with audio_file.open("rb") as file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=file,
            response_format="verbose_json",
        )

    return transcription.model_dump()


def save_json(data: dict, audio_file: Path) -> Path:
    OUTPUT_FOLDER.mkdir(exist_ok=True)
    output_file = OUTPUT_FOLDER / f"{audio_file.stem}_whisper.json"
    output_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return output_file


def get_transcript(data: dict) -> str:
    return data.get("text", "")


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python whisper_transcribe.py path/to/audio_file.mp3")
        raise SystemExit(1)

    load_env_file()

    audio_file = Path(sys.argv[1])
    result = transcribe_audio(audio_file)
    output_file = save_json(result, audio_file)
    transcript = get_transcript(result)

    print(f"Whisper JSON saved to: {output_file}")
    print("\nTranscript:")
    print(transcript or "No transcript found in the response.")


if __name__ == "__main__":
    main()
