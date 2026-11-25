"""Submit the frozen argument and retain the provider's exact disposition."""
import json
from pathlib import Path
import sys

from review_fixed_pair import DEMOS, SCI, accepted, checked, main

DOCS = {
    SCI + "RECEIVER_SHAPE_CALLER.md": "b256924d3176a9fdbb871e07340dc91b65882c58",
    SCI + "RECEIVER_SHAPE_CALLER_PLAN.md": "ea29b235a5c14db96eab1a5dc68baeb729b4064d",
    SCI + "RECEIVER_SHAPE_CONTROLS_PLAN.md": "86af3db99dc6a3830de6fd38e0cccda1310495b1",
    SCI + "receiver_shape_certificate.json": "34dd4a99574185c925eb9be22e63feede6070dbe",
    SCI + "receiver_shape_traces.json.xz": "1ec1acc9d65266a844b3f837b2c6a83ebb23a7d8",
    SCI + "check_receiver_shape.py": "4c2cc20ddc56714ce09d4e247869fb797569996c",
    SCI + "verify_receiver_shape.py": "532fa6d5e21e400a7ba8d688040e80bc68e2b2bc",
    DEMOS + "v16.39-theorem-validation/construct.py": "284b8cc9305c14f3ff6f3693c67a2c61ea00e93e",
    DEMOS + "v16.39-theorem-validation/campaign.py": "a75bfcf8c2e68c021ff0388f5401be9eb39018e8",
    DEMOS + "v16.39-theorem-validation/check.py": "d4acda0e79a35b6c42ef0984ad362ba5e3bfb684",
    DEMOS + "v16.22-response-selection-closure/engine.py": "9b71ce47bbef83132f00270f8a9a19e7721864d6",
    DEMOS + "v16.23-overlap-descent/engine.py": "b18f52109ccff9c7dc77542d3b8f3e5d5989102a",
    DEMOS + "v16.26-consistency-increment-law/engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b",
}
TOPICS = {"live_read", "target_dependence", "fixed_question", "autonomy"}
QUESTION = """Try to falsify this finite rooted-cover construction and its interpretation. Derive the two
minimum covers, which holder the first real recolor reads from the live shrink output, how its route
is materialized, and whether that operation consumes a numeric receiver vector. Reconstruct the target
classification without assuming it; distinguish chart and sibling equivariance, the symmetric prior,
the anchored control, and transient from permanent records. Derive the fixed-test criterion on P1,
the positive-vector obstruction, the two common-address responses, and the no-receiver terminal
continuation. Check what is supplied by the historical campaign. Return a JSON object with verdict
ACCEPTED, REVISE or FAIL, and findings, counterexamples, missing_assumptions and limitations lists.
Only accept a sound scoped argument, with the three substantive objection lists empty. Include
native_bridge_status, and a worked paragraph for each entry of proof_checks keyed live_read,
target_dependence, fixed_question and autonomy. Include exact_checks with keys old_holders (source-a
cut first, then b cut; one-letter chart names), receiver_atoms, common_p_responses (flat, per arm),
all_order_targets (three-letter strings), conditional_order_targets (sorted), numeric_vector_consumed
and source_requires_call (booleans). Counts from the finite replay need not be independently attested."""


def prompt():
    data = {name: checked(name, sha) for name, sha in DOCS.items()}
    chunks = [QUESTION, data[SCI + "RECEIVER_SHAPE_CALLER.md"].decode()]
    sections = (
        ("v16.39-theorem-validation/construct.py", 1, 90),
        ("v16.39-theorem-validation/campaign.py", 31, 46),
        ("v16.26-consistency-increment-law/engine.py", 24, 26),
        ("v16.23-overlap-descent/engine.py", 50, 58),
        ("v16.23-overlap-descent/engine.py", 115, 129),
        ("v16.22-response-selection-closure/engine.py", 137, 146),
    )
    for name, start, end in sections:
        chunks.extend([name, "\n".join(data[DEMOS + name].decode().splitlines()[start-1:end])])
    cert = json.loads(data[SCI + "receiver_shape_certificate.json"])
    chunks.append(json.dumps(dict(per_target=cert["per_target"], named=cert["anchored_fixed_example"]), sort_keys=True))
    return ("\n\n".join(chunks) + "\n").encode()


def verify_reply(doc):
    accepted(doc)
    checks = doc.get("proof_checks", {})
    if doc["native_bridge_status"] != "OPEN" or set(checks) != TOPICS or any(
            not isinstance(v, str) or len(v.split()) < 15 for v in checks.values()):
        raise ValueError("missing proof or scope")
    expected = dict(old_holders=["S", "R"], receiver_atoms=[8, 6], common_p_responses=[8, 8],
                    all_order_targets=["HHS"], conditional_order_targets=["SHH", "SHS"],
                    numeric_vector_consumed=False, source_requires_call=False)
    if json.dumps(doc.get("exact_checks"), sort_keys=True) != json.dumps(expected, sort_keys=True):
        raise ValueError("external reconstruction differs")


if __name__ == "__main__":
    main(sys.argv[1], Path(sys.argv[2]), sources=DOCS, make_prompt=prompt, check_reply=verify_reply)
