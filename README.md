## ASR audio-to-text test

This project includes a simple script that sends a local audio file to
Deepgram and saves the transcription response as JSON in the `output` folder.

### Setup

Create a Deepgram API key, then set it in your shell:

```powershell
$env:DEEPGRAM_API_KEY="your_deepgram_api_key_here"
```

No extra Python packages are required; the script uses Python's standard
library.

### Run transcription

From the project folder:

```powershell
python asr_transcribe.py C:\My_Projects\WebPT\audio_sample.mp3
```

For example, if your audio file is `sample.mp3`, the script creates
`output/sample.json`.

The script calls Deepgram's pre-recorded audio endpoint:

```text
POST https://api.deepgram.com/v1/listen
```

## Whisper audio-to-text test

This project also includes a separate script for OpenAI Whisper transcription.

Add your OpenAI API key to `.env`:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

Run it from the project folder:

```powershell
python whisper_transcribe.py "C:\path\to\audio.mp3"
```

For example, if your audio file is `sample.mp3`, the script creates
`output/sample_whisper.json` and prints the transcript in the terminal.
