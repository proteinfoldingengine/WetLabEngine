from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

STATE_DIR = ROOT / "state"
PROMPTS_DIR = ROOT / "prompts"
RUNS_DIR = ROOT / "runs"
REPORTS_DIR = ROOT / "reports"
CONSTITUTION_DIR = ROOT / "constitution"

OUTPUT_PATH = STATE_DIR / "lab_context.md"


def read(path: Path, limit: int = 12000) -> str:
    if not path.exists():
        return f"[MISSING: {path}]"
    try:
        return path.read_text(encoding="utf-8")[:limit]
    except Exception as e:
        return f"[ERROR READING {path}: {e}]"


def latest_files(pattern: str, limit: int = 3):
    files = sorted(ROOT.glob(pattern))
    return files[-limit:] if files else []


def build_section(title: str, content: str):
    return f"# {title}\n\n{content.strip()}\n\n"


def summarize_validation(validation_path: Path):
    try:
        data = json.loads(validation_path.read_text(encoding="utf-8"))
    except Exception as e:
        return f"Could not parse validation JSON: {e}"

    lines = []

    lines.append(f"- interpretation_allowed: {data.get('interpretation_allowed')}")
    lines.append(f"- overall_status: {data.get('overall_status')}")
    lines.append(f"- valid_row_count: {data.get('valid_row_count')}")
    lines.append(f"- total_row_count: {data.get('total_row_count')}")
    lines.append(
        f"- valid_controller_row_count: {data.get('valid_controller_row_count')}"
    )
    lines.append(
        f"- total_controller_row_count: {data.get('total_controller_row_count')}"
    )

    failures = data.get("failures", [])
    warnings = data.get("warnings", [])

    lines.append("\n## Failures")
    if failures:
        for f in failures:
            lines.append(f"- {f}")
    else:
        lines.append("- none")

    lines.append("\n## Warnings")
    if warnings:
        for w in warnings:
            lines.append(f"- {w}")
    else:
        lines.append("- none")

    return "\n".join(lines)


def main():
    sections = []

    constitution = read(CONSTITUTION_DIR / "agent_constitution.md")
    current_state = read(STATE_DIR / "current_state.md")
    loop_prompt = read(PROMPTS_DIR / "loop_prompt.md")
    next_version = read(PROMPTS_DIR / "next_version.txt")

    sections.append(build_section("Constitution", constitution))
    sections.append(build_section("Current Scientific State", current_state))
    sections.append(build_section("Current Loop Prompt", loop_prompt))
    sections.append(build_section("Next Version Target", next_version))

    latest_reports = latest_files("reports/V*_report.md", limit=3)

    for report in latest_reports:
        sections.append(
            build_section(
                f"Recent Report — {report.name}",
                read(report, limit=10000),
            )
        )

    latest_audits = latest_files("runs/*/*_audit.md", limit=3)

    for audit in latest_audits:
        sections.append(
            build_section(
                f"Recent Audit — {audit.name}",
                read(audit, limit=10000),
            )
        )

    latest_supervisors = latest_files("runs/*/*_supervisor.md", limit=3)

    for sup in latest_supervisors:
        sections.append(
            build_section(
                f"Recent Supervisor — {sup.name}",
                read(sup, limit=10000),
            )
        )

    latest_validations = latest_files("runs/*/*_validation.json", limit=3)

    for val in latest_validations:
        sections.append(
            build_section(
                f"Recent Validation Summary — {val.name}",
                summarize_validation(val),
            )
        )

    summary = """
# Current Lab Summary

The retained-atlas autonomous lab is operating with:
- deterministic validation
- governed reporting
- skeptical audit review
- supervisor/project-manager branch control
- GitHub-based persistent memory

Current strongest validated scientific boundary:
- V307 toy-law diagnostic boundary

Current architecture status:
- governance stack stronger than execution stack
- execution agent remains weakest layer
- validity gating now blocks most invalid interpretations

Current scientific risk:
- repeated degenerate regime generation
- saturated trigger/bad rates
- absent controller separation
- zero horizon metrics in recent runs

Current architectural objective:
- improve scientific critical thinking before execution
- move toward SDK-based project-manager orchestration
"""

    sections.append(summary)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        "\n".join(sections),
        encoding="utf-8",
    )

    print(f"Built lab context: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
