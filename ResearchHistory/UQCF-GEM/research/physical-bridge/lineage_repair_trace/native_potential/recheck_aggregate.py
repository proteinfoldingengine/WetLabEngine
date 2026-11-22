"""Resolve the review's P1 wording against the existing exact fiber-sum entry point."""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import sys


native = Path(__file__).resolve().parents[4] / "foundational-closure-verification"
data = (native / "lineage.py").read_bytes()
blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
if blob != "e95e3e978779164dd91f09b80e3389247e6320c2":
    raise ValueError("Native P1 implementation changed")
sys.path.insert(0, str(native))
from lineage import Carrier, Pruning

fine = Carrier("shared", ((), (0,), (1,)))
coarse = Carrier("shared", ((), (1,)))
prune = Pruning(fine, coarse)
cases = {"a": (1, 0, 0), "b": (0, 1, 0), "b_minus_a": (-1, 1, 0),
         "a_centered": (F(2,3), F(-1,3), F(-1,3)),
         "b_centered": (F(-1,3), F(2,3), F(-1,3))}
rows = {k: tuple(prune.aggregate(v)) for k, v in cases.items()}
if not (rows["a"] == rows["b"] == (1, 0) and rows["b_minus_a"] == (0, 0)
        and rows["a_centered"] == rows["b_centered"] == (F(1,3), F(-1,3))):
    raise ValueError("Direct exact P1 readback differs")
print(json.dumps({"source_blob": blob, "entry": "Pruning.aggregate",
                  "fine_order": ["parent","leaf","sibling"], "coarse_order": ["parent","sibling"],
                  "coarse_outputs": {k: [str(x) for x in v] for k, v in rows.items()}},
                 indent=2, sort_keys=True))
