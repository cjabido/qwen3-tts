import csv
import sys
from pathlib import Path

import click


def _dquote(s: str) -> str:
    escaped = (
        s.replace("\\", "\\\\")
         .replace('"', '\\"')
         .replace("$", "\\$")
         .replace("`", "\\`")
         .replace("!", "\\!")
    )
    return f'"{escaped}"'


@click.command()
@click.argument("csv_file", type=click.Path(exists=True, dir_okay=False))
@click.option("-o", "--output", default=None, help="Output shell script path. Defaults to stdout.")
def main(csv_file: str, output: str | None):
    """Generate a batch shell script from a CSV of voice cloning jobs.

    CSV format (with header row): voice,speed,temp,transcript,text

    \b
    Example:
        q3batch jobs.csv
        q3batch jobs.csv -o run_jobs.sh
    """
    commands: list[str] = []

    with open(csv_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        missing = {"voice", "speed", "temp", "transcript", "text"} - set(reader.fieldnames or [])
        if missing:
            raise click.UsageError(f"CSV is missing required columns: {', '.join(sorted(missing))}")

        for lineno, row in enumerate(reader, start=2):
            voice = row["voice"].strip()
            speed = row["speed"].strip()
            temp = row["temp"].strip()
            transcript = row["transcript"].strip()
            text = row["text"].strip()

            if not voice or not transcript or not text:
                click.echo(f"Warning: skipping row {lineno} (empty voice, transcript, or text)", err=True)
                continue

            commands.append(
                f"q3clone"
                f" -r {_dquote(voice)}"
                f" -s {speed}"
                f" --temp {temp}"
                f" -t {_dquote(transcript)}"
                f" {_dquote(text)}"
            )

    script = "#!/usr/bin/env bash\nset -euo pipefail\n\n" + "\n".join(commands) + "\n"

    if output:
        out_path = Path(output)
        out_path.write_text(script, encoding="utf-8")
        out_path.chmod(out_path.stat().st_mode | 0o755)
        click.echo(f"Wrote {len(commands)} commands to {out_path}")
    else:
        sys.stdout.write(script)
