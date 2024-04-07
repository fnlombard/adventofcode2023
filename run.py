"""Run function to check all source code and run requested solution."""

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


def setup_venv(project_config: Config) -> None:

    if not project_config.venv.exists():
        print("Creating virtual environment.")
        subprocess.run(["python", "-m", "venv", project_config.venv], check=True)
    else:
        print("Reusing virtual environment.")

    print("Installing required packages.")
    install_output = subprocess.run(
        args=[str(project_config.pip), "install", "mypy", "pylint", "black", "numpy"],
        capture_output=True,
        check=False,
    )

    if install_output.stderr:
        print(f"    Error installing requirements:\n{install_output.stderr!r}\n")
    else:
        print("    Successfully installed packages.\n")


def run_checks(project_config: Config) -> None:
    def run_check(library: str) -> subprocess.CompletedProcess:
        print(f"Running: {library}")
        return subprocess.run([project_config.venv / "Scripts" / library, "."], check=False)

    _black_result = run_check("black")
    _mypy_result = run_check("mypy")
    _pylint_result = run_check("pylint")


def run_solution(project_config: Config) -> None:
    _solution_result = subprocess.run(
        [project_config.python, project_config.solution],
        cwd=project_config.solution.parent,
        check=False,
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

    setup_venv(project_config=config)
    run_checks(config)
    run_solution(config)
