from pathlib import Path
from openai import OpenAI
import os

ROOT = Path(__file__).resolve().parents[1]

CONSTITUTION_PATH = ROOT / "constitution" / "agent_constitution.md"
LOOP_PROMPT_PATH = ROOT / "prompts" / "loop_prompt.md"

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def load_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    return path.read_text(encoding="utf-8")

def main():
    constitution = load_text(CONSTITUTION_PATH)
    loop_prompt = load_text(LOOP_PROMPT_PATH)

    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {
                "role": "system",
                "content": constitution,
            },
            {
                "role": "user",
                "content": loop_prompt,
            },
        ],
    )

    print(response.output_text)

if __name__ == "__main__":
    main()
