"""v15.56 Task 29: extensive retained-source pushforward.

Let r:K_f->K_c be the ancestral pruning retraction.  A finitely additive
retained source grade is a signed/positive measure on finite identity sets.
Its canonical pushforward is therefore the measure-theoretic pushforward:
(r_*J)(v)=sum_{k:r(k)=v}J(k).

Finite additivity forces summation over disjoint retraction fibers.  The rule
preserves total grade, commutes with positive global rescaling, and is
functorial: (q o r)_* = q_* o r_*.
"""
def classify():
    return {
      "schema":"uqcf-v1556-source-pushforward-v1",
      "rule":"J_c(v)=sum_{k:r(k)=v} J_f(k)",
      "forced_by_finite_additivity":True,
      "preserves_total_retained_grade":True,
      "projective_scaling_compatible":True,
      "scaling_law":"r_*(aJ)=a r_*J",
      "functorial_under_composed_retractions":True,
      "composition_law":"(q o r)_* J = q_* (r_* J)",
      "geometry_used":[],
      "scientific_result":"EXTENSIVE_RETAINED_SOURCE_HAS_A_CANONICAL_FUNCTORIAL_PUSHFORWARD_UNDER_ANCESTRAL_PRUNING",
      "next_gate":"EXECUTABLE_FINE_PRUNE_COARSE_ROOTED_RESPONSE_COMPARISON"
    }

def pushforward(values, fine_keys, coarse_keys):
    out={k:0.0 for k in coarse_keys}
    for k,x in zip(fine_keys,values):
        candidates=[c for c in coarse_keys if len(c)<=len(k) and tuple(k[:len(c)])==tuple(c)]
        if not candidates:
            raise ValueError("coarse set must retain a prefix/root for every fine key")
        v=max(candidates,key=len)
        out[v]+=float(x)
    return out
