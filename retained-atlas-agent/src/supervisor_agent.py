import argparse
import os
import re
from pathlib import Path
from openai import OpenAI

ROOT = Path(__file__).resolve().parents[1]

CONSTITUTION = ROOT / "constitution" / "agent_constitution.md"
CURRENT_STATE = ROOT / "state" / "current_state.md"
LOOP_PROMPT = ROOT / "prompts" / "loop_prompt.md"
NEXT_VERSION_FILE = ROOT / "prompts" / "next_version.txt"

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


def extract_loop_prompt(supervisor_output: str) -> str:
    start = supervisor_output.find("BEGIN_LOOP_PROMPT")
    end = supervisor_output.find("END_LOOP_PROMPT")

    if start == -1 or end == -1 or end <= start:
        raise ValueError(
            "Supervisor did not provide BEGIN_LOOP_PROMPT / END_LOOP_PROMPT block."
        )

    return supervisor_output[start + len("BEGIN_LOOP_PROMPT"):end].strip()


def extract_next_version(supervisor_output: str) -> str:
    match = re.search(r"## Next Version\s*\n\s*(V[0-9A-Za-z._-]+)", supervisor_output)
    if match:
        return match.group(1).strip()

    match = re.search(r"Next Version\s*:?\s*(V[0-9A-Za-z._-]+)", supervisor_output)
    if match:
        return match.group(1).strip()

    return ""


def harden_bad_freeze(supervisor_output: str) -> str:
    lower = supervisor_output.lower()

    has_freeze = "## supervisor verdict" in lower and re.search(
        r"## supervisor verdict\s*\n\s*freeze", lower
    )

    failure_signals = [
        "validity_gate failed",
        "valid_for_interpretation is false",
        "valid_for_interpretation failed",
        "chosen_regime is null",
        "chosen_regime stayed null",
        "harness failure",
        "repair the harness",
        "not interpretable",
        "do not interpret",
    ]

    if has_freeze and any(s in lower for s in failure_signals):
        supervisor_output = re.sub(
            r"(## Supervisor Verdict\s*\n)\s*freeze",
            r"\1branch",
            supervisor_output,
            flags=re.IGNORECASE,
        )
        supervisor_output += (
            "\n\n## Supervisor Safety Override\n"
            "Original verdict was `freeze`, but the text described a harness/regime "
            "failure or failed validity gate. Per constitution hardening, this was "
            "overridden to `branch`.\n"
        )

    return supervisor_output


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

Scientific current state:
{read(CURRENT_STATE)}

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

Hard supervisor rules:
- If validity_gate failed, chosen_regime is null, or the audit says harness failure, the Supervisor Verdict must be branch or stop, never freeze.
- Use freeze only when a law/result is stable enough to preserve and no immediate repair is needed.
- If audit says validity_gate failed, do not freeze.
- If chosen_regime is null, next objective must repair the harness before ablation.
- If the last run was a harness failure, the next run should be a narrower calibration test.
- Preserve current_state.md as the scientific lineage source.
- Do not overwrite the V307 law boundary unless new valid evidence justifies it.
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
    supervisor_output = harden_bad_freeze(supervisor_output)

    write(run_dir / f"{version}_supervisor.md", supervisor_output)

    new_loop_prompt = extract_loop_prompt(supervisor_output)
    write(LOOP_PROMPT, new_loop_prompt)

    next_version = extract_next_version(supervisor_output)
    if next_version:
        write(NEXT_VERSION_FILE, next_version + "\n")

    print(supervisor_output)
    print(f"\nSaved supervisor decision: {run_dir / f'{version}_supervisor.md'}")
    print(f"Updated loop prompt: {LOOP_PROMPT}")
    if next_version:
        print(f"Next version: {next_version}")
        print(f"Saved next version: {NEXT_VERSION_FILE}")


if __name__ == "__main__":
    main()
