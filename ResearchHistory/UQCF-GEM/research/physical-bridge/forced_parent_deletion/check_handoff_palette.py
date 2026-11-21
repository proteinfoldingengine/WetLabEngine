"""Post-freeze diagnostics on three archived handoffs; run beside check_source_handoff.py."""
import gzip
import itertools
import json
import sys
from collections import Counter

import check_fixed_donor as fixed
import check_routed_chain as chain
from check_source_handoff import edits

def main():
    fixed.pins()
    raw = (chain.DEMOS / chain.ARCHIVE).read_bytes()
    assert fixed.blob(raw) == chain.PINS[chain.ARCHIVE]
    corpus = json.loads(gzip.decompress(raw))["corpus"]
    sys.path.insert(0, str(chain.DEMOS / chain.OLD))
    import producer
    import verifier
    results = []
    for case in (178,184,190):
        row = corpus[case]
        path = row["path"]
        degrees, k = row["spec"]["degrees"], row["spec"]["k"]
        lengths = []
        for index in (3,4):
            q = verifier.raw_profile(path[index],degrees,k)
            assert q[:len(degrees)] == row["spec"]["q"]
            suffix = producer.normalize(path[index],degrees,k,q)
            assert suffix == path[index:]
            lengths.append(len(suffix))
        outcomes = Counter()
        first_gains = Counter()
        for permutation in itertools.permutations(range(k)):
            state = [path[4][j] for j in permutation]
            q = verifier.raw_profile(state,degrees,k)
            renamed = producer.normalize(state,degrees,k,q)
            actor,site,add = next(edits(renamed[:2]))
            name = ("+" if add else "-") + "ABCD"[permutation[actor]] + str(site)
            outcomes[name] += 1
            if permutation == (0,1,3,2):
                assert name == "+D9"
            protected = True
            first_gain = "no gain"
            for (next_actor, vertex, gained), old in zip(edits(renamed), renamed):
                protected = protected and any(j != next_actor and mask & 512 for j,mask in enumerate(old))
                if vertex == 9 and gained:
                    first_gain = ("protected " if protected else "unprotected ") + "ABCD"[permutation[next_actor]]
                    break
            first_gains[first_gain] += 1
            if permutation == (1,0,2,3):
                assert first_gain == "no gain"
        assert sum(outcomes.values()) == 24 and outcomes["+C9"] == 6
        assert first_gains == {"protected C":8,"protected D":8,"protected A":2,"no gain":6}
        results.append({"case":case, "restart_suffix_state_counts":lengths,"next_edit_in_original_names":dict(outcomes),
                        "first_later_gain_in_original_names":dict(first_gains)})
    print(json.dumps(results,indent=2,sort_keys=True))

if __name__ == "__main__":
    main()
