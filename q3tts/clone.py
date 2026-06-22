import os
os.environ["HF_HUB_OFFLINE"] = "1"

import sys
from pathlib import Path

import click

from q3tts._utils import CustomHelpCommand, get_unique_filename


class _HelpCmd(CustomHelpCommand):
    examples = [
        '{prog} -r voice.wav -t "transcript of the sample" "Text to speak"',
        '{prog} -r voice.wav -t "transcript" -o cloned.wav "Hello world"',
        'echo "piped text" | {prog} -r voice.wav -t "transcript"',
    ]


@click.command(cls=_HelpCmd)
@click.argument("text", required=False)
@click.option("-r", "--ref-audio", required=True, type=click.Path(exists=True, dir_okay=False), help="Path to reference audio file (the voice to clone).")
@click.option("-t", "--ref-text", required=True, help="Transcript of the reference audio.")
@click.option("-o", "--output", default="output.wav", help="Output filename (default: output.wav)")
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose output")
@click.option("-s", "--speed", default=1.0, type=float, help="Speech rate (default: 1.0)")
@click.option("--temp", default=0.9, type=float, help="Sampling temperature (default: 0.9)")
def main(text: str | None, ref_audio: str, ref_text: str, output: str, verbose: bool, speed: float, temp: float):
    """Clone a voice from a reference audio sample using Qwen3-TTS."""
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
    model = load_model("mlx-community/Qwen3-TTS-12Hz-1.7B-Base-bf16")

    if verbose:
        click.echo(f"Reference audio: {ref_audio}")
        click.echo(f"Reference text:  {ref_text}")
        click.echo(f"Generating audio for: {text[:50]}{'...' if len(text) > 50 else ''}")

    results = list(model.generate(
        text=text,
        ref_audio=ref_audio,
        ref_text=ref_text,
        speed=speed,
        temperature=temp,
        verbose=verbose,
    ))

    sf.write(str(output_path), np.array(results[0].audio), model.sample_rate)
    if verbose:
        click.echo(f"Audio saved to: {output_path}")
