import argparse
import os
import re
import subprocess
from pathlib import Path
from openai import OpenAI

ROOT = Path(__file__).resolve().parents[1]
CONSTITUTION = ROOT / "constitution" / "agent_constitution.md"
LOOP_PROMPT = ROOT / "prompts" / "loop_prompt.md"

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def read(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(path)
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def extract_python_block(text: str) -> str:
    match = re.search(r"```python\n(.*?)```", text, re.DOTALL)
    if not match:
        raise ValueError("No Python code block found in agent response.")
    return match.group(1).strip()


def call_agent(prompt: str) -> str:
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {"role": "system", "content": read(CONSTITUTION)},
            {"role": "user", "content": prompt},
        ],
    )
    return response.output_text


def run_python(script_path: Path):
    result = subprocess.run(
        ["python", str(script_path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout, result.stderr


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", default="V308")
    args = parser.parse_args()

    version = args.version
    run_dir = ROOT / "runs" / version
    report_path = ROOT / "reports" / f"{version}_report.md"

    prompt = f"""
{read(LOOP_PROMPT)}

You are now executing {version}.

Return:
1. the required loop report draft
2. one runnable Python code block only

The Python script must:
- save outputs under runs/{version}/
- save a JSON result file
- print results
"""

    print(f"Calling agent for {version}...")
    agent_output = call_agent(prompt)

    write(run_dir / f"{version}_agent_plan.md", agent_output)

    code = extract_python_block(agent_output)
    script_path = run_dir / f"{version.lower()}_experiment.py"
    write(script_path, code)

    print(f"Running experiment: {script_path}")
    code_status, stdout, stderr = run_python(script_path)

    write(run_dir / f"{version}_stdout.txt", stdout)
    write(run_dir / f"{version}_stderr.txt", stderr)

    report_prompt = f"""
Using the constitution and loop format, write the final report for {version}.

Agent plan:
{agent_output}

Execution return code:
{code_status}

STDOUT:
{stdout}

STDERR:
{stderr}

Rules:
- do not invent numbers
- use only execution output
- decision must be continue / stop / branch / freeze
- if code failed, decision should not be freeze unless justified
"""

    print(f"Writing report for {version}...")
    report = call_agent(report_prompt)
    write(report_path, report)

    print("\nDONE")
    print(f"Plan:   {run_dir / f'{version}_agent_plan.md'}")
    print(f"Script: {script_path}")
    print(f"Report: {report_path}")
    print(f"Stdout: {run_dir / f'{version}_stdout.txt'}")
    print(f"Stderr: {run_dir / f'{version}_stderr.txt'}")


if __name__ == "__main__":
    main()
