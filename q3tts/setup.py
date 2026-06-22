import click


MODELS = [
    "mlx-community/Qwen3-TTS-12Hz-1.7B-Base-bf16",
    "Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign",
]


@click.command()
def main():
    """Download Qwen3-TTS models to the local HuggingFace cache.

    Run once while connected to the internet. After this, q3tts and q3clone
    work fully offline.
    """
    from huggingface_hub import snapshot_download

    for model_id in MODELS:
        click.echo(f"Downloading {model_id}...")
        path = snapshot_download(model_id)
        click.echo(f"  Cached at: {path}\n")
    click.echo("Setup complete. q3tts and q3clone can now run offline.")
