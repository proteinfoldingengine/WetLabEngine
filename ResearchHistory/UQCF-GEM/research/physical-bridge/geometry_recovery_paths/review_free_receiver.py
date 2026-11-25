"""Challenge four connected claims against frozen source, proof and deterministic outputs."""
import json
from pathlib import Path
import sys
from review_fixed_pair import DEMOS, SCI, accepted, checked, main

DOCS={
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/FREE_RECEIVER.md": "2de93ef6bed08b06e8c77be9674d1b9a40788a1d",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/FREE_RECEIVER_PLAN.md": "a4992a07c1f4a9b544bff66ac308ca182d543d8c",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/FREE_RECEIVER_WORD_LENGTH_PLAN.md": "2e6ca1701f51c7245e9b0090f1f6182dd8355da2",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/check_free_receiver_caller.py": "d8b4cc9577d30492a2518d261359f35fa367c5f3",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/check_free_receiver_chart12.py": "bb21d7b33b6e950d1de5d764ad2573248b5cbc9f",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/check_free_receiver_threshold.py": "55672d8abd305fe31b9455bf011893304e6a6312",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/check_free_receiver_words.py": "b7ab46a21b774d3e5d754640f952b6b51348a7f5",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/free_receiver_call_check.json": "407f4161a57e9ab5d60c2f805c88d9420094b2af",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/free_receiver_caller.json.xz": "44ec33c7fe988cc3e8afde00c6e0fdad1051e426",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/free_receiver_chart12.json.xz": "d1981af91c30e2de640b19b131f9e6653db02490",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/free_receiver_io.py": "e2f37fdca9951c82b294f1e82ff991881c8c866d",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/free_receiver_language.json": "6989aff40fef713104eeb096ff3b1f4d1c205979",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/free_receiver_lengths.json": "1d9dc1639d939f3b1c34e9c1f7988dc828e84fc4",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/free_receiver_spectra.json": "8449e5d0e5ee730c817aacf3136b5f74439f1ed8",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/free_receiver_threshold.json.xz": "7030a4b406a527b9daf4d3618c054af5a2cfe6b8",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/free_receiver_words.json.xz": "4000dfb2e2d861a0fc4882d75399674ea2327c93",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/verify_free_receiver_caller.py": "0f3f7a222296ce753a9527d9ad2f6f096c06cd97",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/verify_free_receiver_chart12.py": "2c91de1f00ce696cf3b6899b8e568d583efd5a15",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/verify_free_receiver_threshold.py": "e2c0b96511797686d0bb11ae4d5ae311d440f441",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/verify_free_receiver_words.py": "4811c459310fea46aba39330605818c344be0594",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.27-increment-attribution-closure/engine.py": "48f132d141167d9cd85ff79ec41720b5dca4f8bb",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.44-two-branch-unit-barrier/producer.py": "2a61afbeeb4f9ca1c9554a2a7c1d2d43bb4800a1",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.44-two-branch-unit-barrier/star_normalize.py": "d58cc9d1168d219b2869affd2d4ede889ebe579b",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.23-overlap-descent/engine.py": "b18f52109ccff9c7dc77542d3b8f3e5d5989102a",
    "review_sources/ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_geometry_repair.py": "3324c0b46e09120ae526338444a19070b692d049",
}
QUESTION="""Independently try to refute this mathematical argument and its scientific interpretation.
Prove or disprove the full characterization of terminal charts, visible owner options, visible words,
and the common-word construction for arbitrary external-only histories. Handle root-only views, internal
stubs and outside steps. On the actual chart 12 fixture reconstruct why one source forces an additional
unit-grade tip, why the root ranges and event-exclusive value differ, why 931 is optimal for sequences
and address-erased states, and why 1173 alone is ambiguous. Explain the role of a failed command versus
an actual successful record. Check the historical normalization path and how the campaign selects
representatives; distinguish supplied call, supplied destination and global versus local data.
Return verdict ACCEPTED, REVISE or FAIL with findings, missing_assumptions, counterexamples and limitations
arrays. The findings array is only for unresolved adverse findings, not affirmative checks. For ACCEPTED,
findings, missing_assumptions and counterexamples must each be exactly []; put affirmative reconstructions
only in worked.proof_checks. Return native_bridge_status as the literal string OPEN. Return worked.proof_checks
keyed terminals, local_words, chart12, threshold, caller, with each value a prose reconstruction of at least
15 words rather than a boolean. Return exact_checks with balanced_maxima (662 then 718), original_maxima,
shared_record_exponent, shortest_address_erased_word, root_after_shortest, source_exclusive_scalar,
actual_selected_arms, event_forces_distinction (boolean). Here event_forces_distinction means that the source
event alone makes the actual receiver record differ under every legal later history. A changed set of possible
records is not enough; a common complete receiver history makes this value false. Do not treat supplied
enumeration counts as independently run."""
TOPICS={"terminals","local_words","chart12","threshold","caller"}


def prompt():
    data={k:checked(k,v) for k,v in DOCS.items()}
    chunks=[QUESTION,data[SCI+"FREE_RECEIVER.md"].decode()]
    for name,start,end in (("v16.26-consistency-increment-law/engine.py",24,36),
                           ("v16.27-increment-attribution-closure/engine.py",4,20),
                           ("v16.44-two-branch-unit-barrier/producer.py",7,48),
                           ("v16.44-two-branch-unit-barrier/star_normalize.py",5,30),
                           ("v16.23-overlap-descent/engine.py",50,58)):
        chunks+=[name,"\n".join(data[DEMOS+name].decode().splitlines()[start-1:end])]
    for name in ("free_receiver_spectra.json","free_receiver_lengths.json","free_receiver_call_check.json",
                 "free_receiver_language.json"):
        chunks.extend([name,data[SCI+name].decode()])
    return ("\n\n".join(chunks)+"\n").encode()


def verify_reply(doc):
    accepted(doc)
    checks=doc.get("proof_checks",{})
    if doc["native_bridge_status"]!="OPEN" or set(checks)!=TOPICS or any(
            not isinstance(v,str) or len(v.split())<15 for v in checks.values()):
        raise ValueError("incomplete argument or unsupported scope")
    expected=dict(balanced_maxima=[3176,3175],original_maxima=[3176,3176],shared_record_exponent=1304,
                  shortest_address_erased_word=931,root_after_shortest=1173,source_exclusive_scalar=3176,
                  actual_selected_arms=0,event_forces_distinction=False)
    if json.dumps(doc.get("exact_checks"),sort_keys=True)!=json.dumps(expected,sort_keys=True):
        raise ValueError("external worked reconstruction differs")


if __name__=="__main__":
    main(sys.argv[1],Path(sys.argv[2]),sources=DOCS,make_prompt=prompt,check_reply=verify_reply)
