import argparse
import json
import os
import re
import subprocess
from pathlib import Path
from openai import OpenAI

ROOT = Path(__file__).resolve().parents[1]

CONSTITUTION = ROOT / "constitution" / "agent_constitution.md"
LOOP_PROMPT = ROOT / "prompts" / "loop_prompt.md"

MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def read(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def load_prior_memory(limit: int = 5) -> str:
    reports_dir = ROOT / "reports"
    runs_dir = ROOT / "runs"

    memory = []

    if reports_dir.exists():
        reports = sorted(reports_dir.glob("V*_report.md"))[-limit:]
        for path in reports:
            memory.append(f"\n--- PRIOR REPORT: {path.name} ---\n")
            memory.append(path.read_text(encoding="utf-8")[:8000])

    if runs_dir.exists():
        results = sorted(runs_dir.glob("V*/V*_results.json"))[-limit:]
        for path in results:
            memory.append(f"\n--- PRIOR RESULTS: {path} ---\n")
            memory.append(path.read_text(encoding="utf-8")[:4000])

    return "\n".join(memory) if memory else "No prior run memory found."


def call_agent(prompt: str) -> str:
    response = client.responses.create(
        model=MODEL,
        input=[
            {"role": "system", "content": read(CONSTITUTION)},
            {"role": "user", "content": prompt},
        ],
    )
    return response.output_text


def extract_json(text: str) -> dict:
    text = text.strip()

    fenced = re.search(r"```json\s*(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if fenced:
        text = fenced.group(1).strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Could not parse JSON from agent response.\n"
            f"Error: {e}\n\nRaw response:\n{text}"
        )


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
    parser.add_argument("--version", default="V309B")
    parser.add_argument("--memory-limit", type=int, default=5)
    args = parser.parse_args()

    version = args.version
    run_dir = ROOT / "runs" / version
    report_path = ROOT / "reports" / f"{version}_report.md"

    run_dir.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    prior_memory = load_prior_memory(limit=args.memory_limit)

    experiment_prompt = f"""
You are executing retained-atlas loop {version}.

Read and obey the constitution.

Loop prompt:
{read(LOOP_PROMPT)}

Prior run memory:
{prior_memory}

Use this memory to avoid repeating tests unless repetition is explicitly needed.
Continue from the latest decision and smallest useful next test.

Important current correction:
If the prior run failed because metrics were degenerate, treat that as a harness/regime failure, not as a law failure.
For example:
- bad_rate too low
- trigger_rate = 0
- score variance = 0
- AUC = 0.5 for all variants
- mean_bad and mean_safe identical

Return ONLY valid JSON.

Required JSON schema:

{{
  "version": "{version}",
  "title": "short title",
  "plan_markdown": "markdown plan using the required loop format",
  "python_filename": "{version.lower()}_experiment.py",
  "python_code": "complete runnable Python code as a string"
}}

Rules for python_code:
- Must be complete runnable Python.
- Must save outputs under runs/{version}/.
- Must save a JSON result file under runs/{version}/{version}_results.json.
- Must print the JSON results to stdout.
- Must not require external files unless it creates them.
- Must not use secrets.
- Must not call OpenAI.
- Must use fixed seeds.
- Must include numerical metrics.
- Must include a validity_gate object in the JSON results.
- validity_gate must report:
  - nondegenerate_bad_rate: true/false
  - nonzero_score_variance: true/false
  - nonzero_trigger_rate: true/false
  - enough_positive_cases: true/false
  - valid_for_interpretation: true/false
- If valid_for_interpretation is false, the report decision must be branch, not freeze.
- For ablation/intervention tests, target bad_rate should be between 0.20 and 0.40 unless the test explicitly studies rare failure.
- For ablation tests, first verify the full score is non-degenerate before interpreting component drops.
- Must be compact and robust.
"""

    print(f"Calling agent for {version}...")
    agent_raw = call_agent(experiment_prompt)

    write(run_dir / f"{version}_agent_raw.txt", agent_raw)

    try:
        payload = extract_json(agent_raw)
    except Exception as e:
        write(run_dir / f"{version}_parse_error.txt", str(e))
        raise

    plan_md = payload.get("plan_markdown", "")
    python_filename = payload.get("python_filename", f"{version.lower()}_experiment.py")
    python_code = payload.get("python_code", "")

    if not python_code.strip():
        raise ValueError("Agent JSON did not include python_code.")

    write(run_dir / f"{version}_agent_plan.md", plan_md)

    script_path = run_dir / python_filename
    write(script_path, python_code)

    print(f"Running experiment: {script_path}")
    code_status, stdout, stderr = run_python(script_path)

    write(run_dir / f"{version}_stdout.txt", stdout)
    write(run_dir / f"{version}_stderr.txt", stderr)

    report_prompt = f"""
Write the final retained-atlas report for {version}.

Use the constitution-required loop format exactly:

# V### — Title

## Question
## Hypothesis
## Method
## Controls
## Results
## Interpretation
## Failure / Caveat
## Decision
## Next

Use only the execution output below.
Do not invent numbers.
Do not overclaim.
Use toy-model language only.

Decision must be one of:
continue / stop / branch / freeze

Validity rule:
If validity_gate.valid_for_interpretation is false, classify the result as a harness/regime failure.
Do not freeze.
Decision should be branch unless there is a stronger reason to stop.

Prior run memory:
{prior_memory}

Agent plan:
{plan_md}

Execution return code:
{code_status}

STDOUT:
{stdout}

STDERR:
{stderr}
"""

    print(f"Writing report for {version}...")
    report = call_agent(report_prompt)
    write(report_path, report)

    print("\nDONE")
    print(f"Raw:    {run_dir / f'{version}_agent_raw.txt'}")
    print(f"Plan:   {run_dir / f'{version}_agent_plan.md'}")
    print(f"Script: {script_path}")
    print(f"Report: {report_path}")
    print(f"Stdout: {run_dir / f'{version}_stdout.txt'}")
    print(f"Stderr: {run_dir / f'{version}_stderr.txt'}")


if __name__ == "__main__":
    main()
