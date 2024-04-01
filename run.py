#!/usr/bin/env python

from contextlib import contextmanager
from dataclasses import dataclass
import os
from pathlib import Path
import sys
import subprocess


@dataclass
class Config:
    day: Path
    venv: Path

    @property
    def python(self) -> Path:
        return self.venv / "Scripts" / "python.exe"

    @property
    def pip(self) -> Path:
        return self.venv / "Scripts" / "pip.exe"

    @property
    def solution(self) -> Path:
        return self.day / "solution.py"


def setup_venv(config: Config) -> None:

    if not config.venv.exists():
        print("Creating virtual environment...")
        subprocess.run(["python", "-m", "venv", config.venv])

    print("Installing required packages...")
    print([str(config.pip), "install", "mypy", "pylint", "black"])
    subprocess.run([str(config.pip), "install", "mypy", "pylint", "black"])


def run_checks(config: Config) -> None:
    def run_check(library: str) -> subprocess.CompletedProcess:
        print(f"testing: {[config.python, library, "."]}")
        subprocess.run([config.venv / "Scripts" / library, "."])

    _mypy_result = run_check("mypy")
    _pylint_result = run_check("pylint")
    _black_result = run_check("black")


def run_solution(config: Config) -> None:
    _solution_result = subprocess.run(
        [config.python, config.solution], cwd=config.solution.parent
    )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./run.py DayXX")
        sys.exit(1)

    day_arg = Path(sys.argv[1])
    current_dir = Path(os.getcwd())

    config = Config(
        day=current_dir / day_arg,
        venv=current_dir / ".venv",
    )

    if not (solution_path := config.day).exists():
        print(f"Directory {solution_path} does not exist.")
        sys.exit(1)

    setup_venv(config=config)
    run_checks(config)
    run_solution(config)