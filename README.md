# qwen3-tts

Local text-to-speech and voice cloning on Apple Silicon using [Qwen3-TTS](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign) and [MLX Audio](https://github.com/Blaizzy/mlx-audio). No cloud APIs — everything runs on your Mac's Neural Engine.

## Requirements

- macOS with Apple Silicon (M1/M2/M3/M4)
- Python 3.12+

## Install

```sh
git clone <repo-url>
cd qwen3-tts
pip install -e .
```

Or with uv:

```sh
uv pip install -e .
```

## First-time setup

Download both models to your local HuggingFace cache (~4–8 GB, requires internet):

```sh
q3setup
```

After this, `q3tts` and `q3clone` work fully offline.

## Commands

### `q3tts` — Voice design TTS

```sh
q3tts "Hello, world!"
q3tts -i "warm female narrator" "Once upon a time..."
q3tts -l Chinese "你好世界"
q3tts --temp 0.5 "Steady delivery."
q3tts -o greeting.wav "Hi there"
echo "piped text" | q3tts
```

| Option | Description |
|---|---|
| `-o FILE` | Output filename (default: `output.wav`, auto-increments to `output-2.wav` etc.) |
| `-l LANG` | Language (default: `English`) |
| `-i TEXT` | Voice style instruction (e.g., `"deep low voice"`, `"warm female narrator"`) |
| `--temp FLOAT` | Sampling temperature — lower is flatter, higher is more expressive (default: `0.9`) |
| `-v` | Verbose output |

### `q3clone` — Voice cloning

```sh
q3clone -r sample.wav -t "What was said in the sample" "New text to speak"
q3clone -r sample.wav -t "transcript" -s 0.9 --temp 0.6 "Careful delivery"
q3clone -r sample.wav -t "transcript" -o cloned.wav "Hello world"
echo "long text" | q3clone -r sample.wav -t "transcript"
```

| Option | Description |
|---|---|
| `-r FILE` | **(required)** Reference audio file (voice to clone) |
| `-t TEXT` | **(required)** Transcript of the reference audio |
| `-o FILE` | Output filename (default: `output.wav`, auto-increments) |
| `-s FLOAT` | Speech rate (default: `1.0`) |
| `--temp FLOAT` | Sampling temperature (default: `0.9`) |
| `-v` | Verbose output |

Tips for best results:
- Use a clean 5–15 second reference clip with minimal background noise
- The transcript must match the reference audio exactly
- WAV format works best for reference audio

### `q3setup` — Download models

```sh
q3setup
```

Downloads both models to `~/.cache/huggingface/`. Run once; required before using `q3tts` or `q3clone`.

### `q3batch` — Batch voice cloning from CSV

```sh
q3batch jobs.csv            # print shell script to stdout
q3batch jobs.csv -o run.sh  # save executable shell script
```

CSV format (with header row): `voice,speed,temp,transcript,text`

See `example_jobs.csv` for a sample.

## Models

| Model | Used by | Size |
|---|---|---|
| `Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign` | `q3tts` | ~3 GB |
| `mlx-community/Qwen3-TTS-12Hz-1.7B-Base-bf16` | `q3clone` | ~3 GB |

## Offline use on another Mac

1. On a machine **with** internet: `q3setup`
2. Copy `~/.cache/huggingface/` to the target Mac
3. Install the package: `pip install -e .`
4. Commands work offline immediately
