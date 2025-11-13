"""Unified launcher for the weather application."""

from __future__ import annotations

import argparse
import sys

import cli
import gui


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Weather Application")
    parser.add_argument(
        "--mode",
        choices=("cli", "gui"),
        default="cli",
        help="Launch mode: command-line interface or Tkinter GUI (default: cli).",
    )
    parser.add_argument(
        "rest",
        nargs=argparse.REMAINDER,
        help="Arguments forwarded to the selected mode.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])

    if args.mode == "gui":
        gui.main()
        return 0

    return cli.main(args.rest)


if __name__ == "__main__":
    raise SystemExit(main())

