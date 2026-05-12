import argparse
import os
from pathlib import Path
from openai import OpenAI

ROOT = Path(__file__).resolve().parents[1]

CONSTITUTION = ROOT / "constitution" / "agent_constitution.md"
CURRENT_STATE = ROOT / "state" / "current_state.md"
LOOP_PROMPT = ROOT / "prompts" / "loop_prompt.md"

MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def read(path: Path, limit: int = 30000) -> str:
    if not path.exists():
        return f"[MISSING: {path}]"
    return path.read_text(encoding="utf-8")[:limit]


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def call_agent(prompt: str) -> str:
    response = client.responses.create(
        model=MODEL,
        input=[
            {"role": "system", "content": read(CONSTITUTION)},
            {"role": "user", "content": prompt},
        ],
    )
    return response.output_text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", required=True)
    args = parser.parse_args()

    version = args.version
    run_dir = ROOT / "runs" / version
    report_path = ROOT / "reports" / f"{version}_report.md"

    plan = read(run_dir / f"{version}_agent_plan.md")
    results = read(run_dir / f"{version}_results.json")
    stdout = read(run_dir / f"{version}_stdout.txt")
    stderr = read(run_dir / f"{version}_stderr.txt")
    returncode = read(run_dir / f"{version}_returncode.txt")
    validation_md = read(run_dir / f"{version}_validation.md")
    validation_json = read(run_dir / f"{version}_validation.json")

    prompt = f"""
You are the Retained-Atlas Report Agent.

Your job is to write the final report for {version} using:
- execution output
- saved JSON results
- deterministic execution validation

You must obey the constitution and current_state.md.

Scientific current state:
{read(CURRENT_STATE)}

Operational loop prompt:
{read(LOOP_PROMPT)}

Important reporting rule:
The deterministic execution validator is authoritative for interpretation permission.

If validation says interpretation_allowed = false:
- do NOT interpret scientific meaning
- classify as harness/regime/execution failure
- decision should be branch or stop, not continue/freeze as success

If validation says interpretation_allowed = true:
- you may interpret only the rows/claims supported by validation and results
- do not generalize from one valid row to broad robustness

Use this required format exactly:

# {version} — Title

## Question

## Hypothesis

## Method

## Controls

## Results

## Interpretation

## Failure / Caveat

## Decision
continue / stop / branch / freeze

## Next

Rules:
- Use only numbers from stdout/results/validation.
- Do not invent numbers.
- Do not overclaim.
- Use toy-model language only.
- Do not claim GR recovery, spacetime, black holes, quantum gravity, or universality.
- If code failed, reject interpretation.
- If validation failed, reject scientific interpretation.
- If only one narrow valid regime exists, say so clearly.

AGENT PLAN:
{plan}

EXECUTION RETURN CODE:
{returncode}

EXECUTION VALIDATION MD:
{validation_md}

EXECUTION VALIDATION JSON:
{validation_json}

RESULTS JSON:
{results}

STDOUT:
{stdout}

STDERR:
{stderr}
"""

    report = call_agent(prompt)
    write(report_path, report)

    print(report)
    print(f"\nSaved report: {report_path}")


if __name__ == "__main__":
    main()
