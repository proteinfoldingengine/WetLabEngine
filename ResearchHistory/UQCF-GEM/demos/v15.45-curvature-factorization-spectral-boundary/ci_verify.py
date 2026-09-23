"""Fail-closed exact-head certification helpers for UQCF-GEM v15.45."""
from __future__ import annotations
import json
import subprocess
import sys
from hashlib import sha1
from pathlib import Path

from gate import verify_result

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
PARENT="9085e4fa0bec3dbd700f759a8a9629b230d226ff"
SPEC=ROOT/"docs/superpowers/specs/2026-09-23-v1545-curvature-factorization-spectral-boundary-design.md"
PLAN=ROOT/"docs/superpowers/plans/2026-09-23-v1545-curvature-factorization-spectral-boundary-implementation.md"
LEDGER=HERE/"docs/RESULTS.json"
SPEC_BLOB="dc3f87ecf25d64e410e72c52e6a6a604349f5a92"
PLAN_BLOB="991dba75caa477dbd0a28df5e693dd01c70d5e4e"


def _blob(path):
    raw=path.read_bytes()
    return sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()


def _git(*args):
    return subprocess.run(("git",)+args,cwd=ROOT,text=True,capture_output=True,
                          check=True).stdout.strip()


def verify_runtime(version=None):
    value=sys.version_info[:3] if version is None else tuple(version)
    if value != (3,13,5):
        raise ValueError("python_runtime")
    return value


def verify_head(expected, actual=None):
    value=_git("rev-parse","HEAD") if actual is None else actual
    if value != expected:
        raise ValueError("head_mismatch")
    return value


def load_ledger():
    return json.loads(LEDGER.read_text("ascii"))


def verify_ledger(value=None):
    ledger=load_ledger() if value is None else value
    verify_result(ledger)
    if LEDGER.read_bytes() != __import__("gate").canonical_bytes(ledger) and value is None:
        raise ValueError("noncanonical_ledger")
    return ledger


def verify_test_summary(*,tests_run,failures,errors,skipped):
    if skipped:
        raise ValueError("skipped_tests")
    if failures or errors or tests_run <= 0:
        raise ValueError("test_failure")
    return True


def verify_static_contract():
    if _blob(SPEC)!=SPEC_BLOB:
        raise ValueError("spec_drift")
    if _blob(PLAN)!=PLAN_BLOB:
        raise ValueError("plan_drift")
    changed=_git("diff","--name-status",PARENT+"..HEAD").splitlines()
    if not changed:
        raise ValueError("empty_scope")
    if any(not line.startswith("A\t") for line in changed):
        raise ValueError("nonadditive_scope")
    return {"parent":PARENT,"spec_blob":SPEC_BLOB,"plan_blob":PLAN_BLOB,
            "additive_scope":True,"changed_files":len(changed)}
