import os
os.environ["HF_HUB_OFFLINE"] = "1"

import sys
from pathlib import Path

import click

from q3tts._utils import CustomHelpCommand, get_unique_filename


class _HelpCmd(CustomHelpCommand):
    examples = [
        '{prog} "say this text out loud"',
        '{prog} -o saved.wav "hello world"',
        '{prog} -l Chinese "你好世界"',
        '{prog} -i "deep low voice" "hello"',
        'echo "piped text" | {prog}',
    ]


@click.command(cls=_HelpCmd)
@click.argument("text", required=False)
@click.option("-o", "--output", default="output.wav", help="Output filename (default: output.wav)")
@click.option("-l", "--language", default="English", help="Language for TTS (default: English)")
@click.option("-i", "--instruct", default=None, help="Voice instruction (e.g., 'deep low voice')")
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose output")
@click.option("--temp", default=0.9, type=float, help="Sampling temperature (default: 0.9)")
def main(text: str | None, output: str, language: str, instruct: str | None, verbose: bool, temp: float):
    """Generate speech using Qwen3-TTS voice design on Apple Silicon."""
    if text is None:
        if not sys.stdin.isatty():
            text = sys.stdin.read().strip()
        else:
            raise click.UsageError("No text provided. Pass text as an argument or pipe it via stdin.")

    if not text:
        raise click.UsageError("Text cannot be empty.")

    output_path = Path(output)
    if output == "output.wav":
        output_path = get_unique_filename(output_path)

    import numpy as np
    import soundfile as sf
    from mlx_audio.tts.utils import load_model

    if verbose:
        click.echo("Loading model...")
    model = load_model("Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign")

    if verbose:
        click.echo(f"Generating audio for: {text[:50]}{'...' if len(text) > 50 else ''}")

    results = list(model.generate_voice_design(
        text=text,
        language=language,
        verbose=verbose,
        instruct=instruct or "",
        temperature=temp,
    ))

    sf.write(str(output_path), np.array(results[0].audio), model.sample_rate)
    if verbose:
        click.echo(f"Audio saved to: {output_path}")
