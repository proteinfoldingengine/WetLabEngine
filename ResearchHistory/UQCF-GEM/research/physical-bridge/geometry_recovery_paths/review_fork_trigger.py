"""Challenge the frozen free-pruning and historical-caller results in one bounded review."""
import json
import lzma
from pathlib import Path
import sys

from review_fixed_pair import DEMOS, SCI, accepted, checked, main

DOCS = {
    SCI+"FORK_TRIGGER.md": "623011d53629341d7c93c24011fadba3a709d890",
    SCI+"FORK_TRIGGER_PLAN.md": "fa0fa4d9ef0c4dff8eda794f0a47ef55f47029fe",
    SCI+"FORK_TRIGGER_CALLER_PLAN.md": "9e3e497c5f4f9a3c5399dea682fc760fde0154bf",
    SCI+"fork_trigger_certificate.json": "2d57bb550244c61ac3915283f6c13a89362fdf70",
    SCI+"fork_trigger_caller.json.xz": "277466539a3e3148e087f8ea728bf6f2ab26ad52",
    DEMOS+"v16.23-overlap-descent/engine.py": "b18f52109ccff9c7dc77542d3b8f3e5d5989102a",
    DEMOS+"v16.26-consistency-increment-law/engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b",
    DEMOS+"v16.28-diamond-attribution-closure/producer.py": "36c894db328c0865007df3ca273ddb059475fe4a",
    DEMOS+"v16.39-theorem-validation/construct.py": "284b8cc9305c14f3ff6f3693c67a2c61ea00e93e",
}
TOPICS = {"terminals", "trigger", "history_measure", "historical_caller", "limitations"}
QUESTION = """Independently try to falsify the attached UQCF finite-tree results. Derive both terminal outcomes and
the prefix P1 reading at their common fork; verify the bi-implication for complete histories, the lead/lag on
incomplete histories and the difference between local and global cover. Derive the explicit bijection of active
words and the spectator interleaving and uniform-enabled results. Check the archived v16.39 code directly for
the mixed-depth, role-reversal and deep/deep cases, plus endpoint-dependent versus endpoint-independent phases.
Challenge any claim of autonomous selection, causal triggering or physical probability. Treat the enumeration
as bounded evidence. Return one JSON object with verdict ACCEPTED, REVISE or FAIL; findings, missing_assumptions,
counterexamples and limitations lists; native_bridge_status OPEN unless you can establish otherwise; proof_checks
with a worked paragraph each under terminals, trigger, history_measure, historical_caller and limitations.
Include exact_checks with named_changed_roots, no_write_root, spectator_two_counts_after_5 (write, unchanged),
split_under_uniform_enabled (rational string), mixed_depth_roots_source_first, deep_six_roots_source_first,
histories_with_trigger and actor_schedule_derived. Accept only if the whole scoped argument is sound and
the three substantive objections lists are empty. Keep limitations explicit."""


def prompt():
    data={k:checked(k,v) for k,v in DOCS.items()}
    chunks=[QUESTION,data[SCI+"FORK_TRIGGER.md"].decode()]
    for file,first,last in (("v16.23-overlap-descent/engine.py",50,58),
        ("v16.26-consistency-increment-law/engine.py",9,35),("v16.28-diamond-attribution-closure/producer.py",45,74),
        ("v16.39-theorem-validation/construct.py",1,110)):
        contents=data[DEMOS+file].decode().splitlines()
        chunks.extend([f"Original {file}, lines {first} through {min(last,len(contents))}","\n".join(contents[first-1:last])])
    cert=json.loads(data[SCI+"fork_trigger_certificate.json"])
    caller=json.loads(lzma.decompress(data[SCI+"fork_trigger_caller.json.xz"]))
    chunks.append(json.dumps(dict(complete=cert["bare"],named=cert["examples"],builder=caller["bare"],
                                  builder_examples=caller["examples"]),sort_keys=True))
    return ("\n\n".join(chunks)+"\n").encode()


def verify_reply(doc):
    accepted(doc)
    checks=doc.get("proof_checks",{})
    if doc["native_bridge_status"]!="OPEN" or set(checks)!=TOPICS or any(
            not isinstance(x,str) or len(x.split())<15 for x in checks.values()):
        raise ValueError("incomplete independent proof checks")
    expected=dict(named_changed_roots=[10,9],no_write_root=3,spectator_two_counts_after_5=[60,84],
                  split_under_uniform_enabled="1/2",mixed_depth_roots_source_first=[3,11],
                  deep_six_roots_source_first=[16,16],histories_with_trigger=456,actor_schedule_derived=False)
    if json.dumps(doc.get("exact_checks"),sort_keys=True)!=json.dumps(expected,sort_keys=True):
        raise ValueError("external quantitative/scope reconstruction differs")


if __name__=="__main__":
    main(sys.argv[1],Path(sys.argv[2]),sources=DOCS,make_prompt=prompt,check_reply=verify_reply)
