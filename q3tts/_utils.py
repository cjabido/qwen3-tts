from pathlib import Path

import click


def get_unique_filename(base_path: Path) -> Path:
    if not base_path.exists():
        return base_path
    stem = base_path.stem
    suffix = base_path.suffix
    parent = base_path.parent
    counter = 2
    while True:
        new_path = parent / f"{stem}-{counter}{suffix}"
        if not new_path.exists():
            return new_path
        counter += 1


class CustomHelpCommand(click.Command):
    """click.Command subclass that appends an Examples section to --help.

    Subclass and set the `examples` class attribute as a list of strings;
    use `{prog}` as a placeholder for the command name.
    """

    examples: list[str] = []

    def format_help(self, ctx, formatter):
        super().format_help(ctx, formatter)
        if self.examples:
            prog = ctx.info_name
            with formatter.section("Examples"):
                formatter.write_paragraph()
                for ex in self.examples:
                    formatter.write_text(ex.replace("{prog}", prog))
