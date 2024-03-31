#!/usr/bin/env python

from contextlib import contextmanager
import os
import sys
import subprocess


@contextmanager
def setup_venv(day_path):
    venv_path = os.path.join(day_path, "venv")
    if not os.path.exists(venv_path):
        print("Creating virtual environment...")
        subprocess.run(["python", "-m", "venv", "venv"], cwd=day_path)

    scripts_path = os.path.join(venv_path, "Scripts")
    os.environ["PATH"] = f"{scripts_path}:{os.environ['PATH']}"

    print("Installing required packages...")
    subprocess.run(
        [os.path.join(scripts_path, "pip"), "install", "mypy", "pylint", "black"],
        cwd=day_path,
    )

    # Returns context manager for local environment
    activate_script = os.path.join(scripts_path, "activate.bat")
    subprocess.run(activate_script)


def run_checks(day_path):
    subprocess.run(["mypy", "."], cwd=day_path)
    subprocess.run(["pylint", "."], cwd=day_path)
    subprocess.run(["black", "."], cwd=day_path)


def run_solution(day_path):
    solution_file = os.path.join(day_path, "solution.py")
    subprocess.run(["python", solution_file], cwd=day_path)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./run.py DayXX")
        sys.exit(1)

    project_dir = os.path.dirname(os.path.abspath(__file__))

    day_dir = sys.argv[1]
    day_path = os.path.join(project_dir, day_dir)

    if not os.path.exists(day_path):
        print(f"Directory {day_path} does not exist.")
        sys.exit(1)

    setup_venv(day_path)
    run_checks(day_path)
    run_solution(day_path)
