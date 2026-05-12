import argparse
import os
from pathlib import Path
from openai import OpenAI

ROOT = Path(__file__).resolve().parents[1]

CONSTITUTION = ROOT / "constitution" / "agent_constitution.md"
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

    report = read(ROOT / "reports" / f"{version}_report.md")
    audit = read(run_dir / f"{version}_audit.md")
    results = read(run_dir / f"{version}_results.json")
    stdout = read(run_dir / f"{version}_stdout.txt")
    stderr = read(run_dir / f"{version}_stderr.txt")
    current_loop_prompt = read(LOOP_PROMPT)

    prompt = f"""
You are the Retained-Atlas Supervisor Agent.

Your job is to do what a human research lead would do after each loop:
- read the report
- read the audit
- decide whether to continue, branch, stop, or freeze
- select the next version label
- update prompts/loop_prompt.md for the next run

You are not writing code.
You are not interpreting invalid results as law evidence.
You are controlling the research loop.

Required output format:

# {version} — Supervisor Decision

## Supervisor Verdict
continue / branch / stop / freeze

## Reason

## Next Version

## Next Objective

## Required Prompt Update

Provide the exact full replacement text for prompts/loop_prompt.md inside this marker:

BEGIN_LOOP_PROMPT
...full markdown prompt...
END_LOOP_PROMPT

Rules:
- If audit says validity_gate failed, do not freeze.
- If chosen_regime is null, next objective must repair the harness before ablation.
- If the last run was a harness failure, the next run should be a narrower calibration test.
- Do not overclaim.
- Use toy-model language only.
- The updated loop_prompt.md must be specific enough that the next agent run knows exactly what to do.

CURRENT LOOP PROMPT:
{current_loop_prompt}

REPORT:
{report}

AUDIT:
{audit}

RESULTS:
{results}

STDOUT:
{stdout}

STDERR:
{stderr}
"""

    supervisor_output = call_agent(prompt)

    write(run_dir / f"{version}_supervisor.md", supervisor_output)

    start = supervisor_output.find("BEGIN_LOOP_PROMPT")
    end = supervisor_output.find("END_LOOP_PROMPT")

    if start == -1 or end == -1 or end <= start:
        raise ValueError("Supervisor did not provide BEGIN_LOOP_PROMPT / END_LOOP_PROMPT block.")

    new_loop_prompt = supervisor_output[start + len("BEGIN_LOOP_PROMPT"):end].strip()
    write(LOOP_PROMPT, new_loop_prompt)

    print(supervisor_output)
    print(f"\nSaved supervisor decision: {run_dir / f'{version}_supervisor.md'}")
    print(f"Updated loop prompt: {LOOP_PROMPT}")


if __name__ == "__main__":
    main()
