"""Audit the ledger input in the pinned V1173 winner-selection caller."""
import ast
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import List, Tuple

PATH = "Tmp/TOE/Einstein 6/v1173_cinematic_provenance_collapse_package/v1173_cinematic_provenance_collapse_engine.py"
BLOB = "c3fbc4fc1356f52e823678b694ba7ed86d73fff3"


def main():
    root = Path(__file__).resolve().parents[5]
    raw = (root / PATH).read_bytes()
    assert hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest() == BLOB
    tree = ast.parse(raw)
    required_globals = {"QUORUM", "PINNED_GENESIS_ROOT", "PINNED_GENESIS_REGISTRY"}
    ledger_functions = {
        "short_hash", "chain_transition", "registry_matches", "root_matches", "quorum_valid",
        "circular_bootstrap_detected", "build_chain", "append_chain_valid_partial",
        "genesis_pin_passes_partial", "HistoryLedger", "make_ledger",
    }
    definitions = [
        node for node in tree.body
        if (isinstance(node, (ast.FunctionDef, ast.ClassDef)) and node.name in ledger_functions)
        or (isinstance(node, ast.Assign)
            and any(isinstance(target, ast.Name) and target.id in required_globals for target in node.targets))
    ]
    env = {"dataclass": dataclass, "hashlib": hashlib, "List": List, "Tuple": Tuple,
           "__name__": "__main__"}
    # Only the pinned, standard-library ledger fragment is executed.
    exec(compile(ast.Module(body=definitions, type_ignores=[]), PATH, "exec", dont_inherit=True), env)
    run = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "run_pruning_for_mode")
    access = sorted((n.lineno, type(n.ctx).__name__) for n in ast.walk(run) if isinstance(n, ast.Name) and n.id == "ledger")
    assert access == [(356, "Store"), (428, "Load")]
    assert ast.unparse(run.body[4]) == "ledger = make_ledger(mode)"
    final_check = next(n for n in run.body if n.lineno == 428)
    assert ast.unparse(final_check) == "cert = certify_field(mode, winner, genesis, ledger, thresholds)"
    transform = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "apply_mode_transform")
    assert any(ast.unparse(n) == "f = torch.flip(f, dims=[3])" for n in ast.walk(transform))

    ledgers = []
    actual = []
    for mode in ("valid_label_transported", "retained_order_shuffle", "genesis_valid_source_shuffled"):
        ledger = env["make_ledger"](mode)
        verify = env["genesis_pin_passes_partial"]
        accepted = all(verify(ledger.registry, ledger.root, ledger.events, ledger.witnesses, ledger.roots, k)
                       for k in range(1, len(ledger.events) + 1))
        broken = ledger.roots[:-1] + ["mismatch"]
        rejects = not verify(ledger.registry, ledger.root, ledger.events, ledger.witnesses, broken, len(ledger.events))
        assert accepted and rejects
        ledgers.append({"mode": mode, "head": ledger.roots[-1], "events": ledger.events,
                        "every_prefix_passed": accepted, "changed_head_rejected": rejects})
        actual.append(ledger)
    assert actual[0].events == list(reversed(actual[1].events))
    assert actual[0].roots == actual[2].roots and actual[0].roots != actual[1].roots
    print(json.dumps({"source_blob": BLOB, "ledger_accesses_in_selection_caller": access,
                      "old_mode_control_has_independent_tensor_transform": True,
                      "ledgers": ledgers, "run_scope": "ledger verification and caller syntax"}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
