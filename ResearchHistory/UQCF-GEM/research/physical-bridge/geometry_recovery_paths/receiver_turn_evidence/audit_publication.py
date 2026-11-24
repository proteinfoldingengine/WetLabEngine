"""Verify both scientific outputs and the original receiver-turn review disposition."""
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from fixed_pair_evidence.audit_publication import main


if __name__ == "__main__":
    print(json.dumps(main(HERE, receiver=True), indent=2, sort_keys=True))
