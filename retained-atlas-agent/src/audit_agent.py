import argparse
import os
from pathlib import Path
from openai import OpenAI

ROOT = Path(__file__).resolve().parents[1]
CONSTITUTION = ROOT / "constitution" / "agent_constitution.md"
MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def read(path: Path, limit: int = 20000) -> str:
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
    results = read(run_dir / f"{version}_results.json")
    stdout = read(run_dir / f"{version}_stdout.txt")
    stderr = read(run_dir / f"{version}_stderr.txt")
    plan = read(run_dir / f"{version}_agent_plan.md")

    code_files = list(run_dir.glob("*.py"))
    code_text = "\n\n".join(
        f"--- CODE FILE: {p.name} ---\n{read(p, limit=30000)}"
        for p in code_files
    )

    prompt = f"""
You are the Retained-Atlas Auditor Agent.

Your job is to audit the latest retained-atlas loop like a skeptical reviewer.

You are NOT the generator.
You are NOT trying to rescue the result.
You are checking whether the report, code, results, and decision obey the constitution.

Audit version:
{version}

You must answer in this exact format:

# {version} — Audit Report

## Audit Verdict
pass / warning / fail

## Decision Check
Was the reported decision justified?
Expected decision if different:

## Validity Gate Check
Did validity_gate exist?
Did valid_for_interpretation pass?
If it failed, did the report avoid interpretation?

## Numerical Integrity Check
Were numbers grounded in stdout/results?
Any invented or unsupported numbers?

## Code/Method Check
Was the code runnable?
Any obvious harness flaws?
Any degenerate regime problems?

## Claim Boundary Check
Any overclaiming?
Any forbidden GR/physics language?

## Required Correction
What must be fixed before next loop?

## Recommended Next Version
Example: V309E

## Recommended Next Test
Smallest useful next test.

Important rules:
- If validity_gate.valid_for_interpretation is false, audit should reject freeze.
- If chosen_regime is null, audit should reject component interpretation.
- If code failed, audit should reject all result interpretation.
- If report says branch because harness failed, that is usually correct.
- Keep toy-model language only.
- Do not invent results.

REPORT:
{report}

RESULTS JSON:
{results}

STDOUT:
{stdout}

STDERR:
{stderr}

PLAN:
{plan}

CODE:
{code_text}
"""

    audit = call_agent(prompt)
    audit_path = run_dir / f"{version}_audit.md"
    write(audit_path, audit)

    print(audit)
    print(f"\nSaved audit: {audit_path}")


if __name__ == "__main__":
    main()
