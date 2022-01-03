# -*- coding: utf-8 -*-

"""Console script for knitchart."""
import contextlib
import json
import os
import sys

import click
from dotenv import load_dotenv

# if dotenv file, load it
dotenv_path = os.environ.get("KNITCHART_DOTENV_PATH", None)
if dotenv_path:
    # BEWARE that dotenv overrides what's already in env
    load_dotenv(dotenv_path, override=True)

patterns = {}


@click.group()
def cli():
    pass


@click.command()
@click.option(
    "--pattern-name",
    help="name of pattern, given in chart-filename, to be printed",
)
@click.option(
    "--width",
    default=5,
    help="number of pattern repetitions for width",
)
@click.option(
    "--height",
    default=3,
    help="number of pattern repetitions for height",
)
def print_pattern(pattern_name, width, height):
    chart_filename = os.environ.get("KNITCHART_DB", None)
    if chart_filename is None:
        # get local pattern file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        chart_filename = os.path.join(current_dir, "pattern_db.json")

    if os.path.exists(chart_filename) and os.path.isfile(chart_filename):
        # read chart_filename into patterns
        with click.open_file(chart_filename, "r") as handle:
            result = json.load(handle)
    else:
        click.echo("missing chart db filename")
        exit(1)

    if isinstance(result, dict):
        patterns.update(result)

    if pattern_name not in patterns:
        click.echo(
            "pattern_name({}) not in db({})".format(pattern_name, chart_filename)
        )
        exit(2)

    y = 0
    while y < height:
        for line in patterns[pattern_name]:
            print(width * line)
        y += 1


# add commands to group
cli.add_command(print_pattern)


if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover
