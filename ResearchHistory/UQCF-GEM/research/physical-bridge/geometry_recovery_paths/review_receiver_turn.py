"""Submit the distinct receiver-turn claim to the pinned reviewer on its frozen inputs."""
import json
from pathlib import Path
import sys

from review_fixed_pair import DEMOS, SCI, accepted, checked, main

DOCS = {
    SCI + "RECEIVER_TURN.md": "94efb2d63eb0c6e84b864c71ffbae596dd0c45b7",
    SCI + "RECEIVER_TURN_PLAN.md": "6ab11b9a18176eff9b894974057cfea6da4c0490",
    SCI + "receiver_turn_certificate.json": "481cefbcc2f6d748469efdacba5863e71aa15c8b",
    SCI + "check_receiver_turn.py": "e1a36464dd6c6e432e7c2428c27e0a0f15adf5c5",
    SCI + "verify_receiver_turn.py": "a91e74a27f0c1ae9dd6187fb5071272dd4b62ef5",
    DEMOS + "v16.23-overlap-descent/engine.py": "b18f52109ccff9c7dc77542d3b8f3e5d5989102a",
    DEMOS + "v16.26-consistency-increment-law/engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b",
}
TOPICS = {"two_successes", "local_readout", "cover_controls", "schedule"}
QUESTION = """Independently challenge the complete attached receiver-turn proof. Focus on whether
a successful native deletion occurs in both arms, whether the single terminal measurement is truly
receiver-local, whether the global admissibility oracle is indispensable, and whether an autonomous
receiver turn is established. Reconstruct the six-node example, both coverage laws, sibling case,
extra chart, and counter-schedule. Seek a counterexample to the quantified result and to any stronger
statement. Return a JSON object with verdict ACCEPTED, REVISE or FAIL; findings, counterexamples,
missing_assumptions and limitations arrays; native_bridge_status OPEN unless justified otherwise;
proof_checks with substantiated worked paragraphs keyed two_successes, local_readout, cover_controls
and schedule. Return exact_checks with keys receiver_deleted, receiver_node_one, total, distinct_parent_pairs,
sibling_pairs, autonomous_receiver_turn. Keep substantive objection arrays empty only for valid scoped
acceptance. Attached enumeration is bounded evidence; do not assert that you ran it yourself."""


def prompt():
    docs = {name: checked(name, blob).decode() for name, blob in DOCS.items()}
    chunks = [QUESTION, docs[SCI + "RECEIVER_TURN.md"], docs[SCI + "check_receiver_turn.py"],
              docs[SCI + "verify_receiver_turn.py"]]
    for file, lo, hi in ((DEMOS + "v16.23-overlap-descent/engine.py", 50, 58),
                         (DEMOS + "v16.26-consistency-increment-law/engine.py", 9, 25)):
        chunks.extend([f"Verbatim {file}, lines {lo}-{hi}", "\n".join(docs[file].splitlines()[lo-1:hi])])
    c = json.loads(docs[SCI + "receiver_turn_certificate.json"])
    chunks.append(json.dumps({"counts": c["counts"], "witness": c["witness"]}, sort_keys=True))
    return ("\n\n".join(chunks) + "\n").encode()


def verify_reply(doc):
    accepted(doc)
    checks = doc.get("proof_checks", {})
    if doc["native_bridge_status"] != "OPEN" or set(checks) != TOPICS or any(
            not isinstance(x, str) or len(x.split()) < 15 for x in checks.values()):
        raise ValueError("missing reconstruction")
    expected = dict(receiver_deleted=[5, 4], receiver_node_one=[4, 6], total=16, distinct_parent_pairs=76,
                    sibling_pairs=8, autonomous_receiver_turn=False)
    if json.dumps(doc.get("exact_checks"), sort_keys=True) != json.dumps(expected, sort_keys=True):
        raise ValueError("external numerical/scope adjudication differs")


if __name__ == "__main__":
    main(sys.argv[1], Path(sys.argv[2]), sources=DOCS, make_prompt=prompt, check_reply=verify_reply)
