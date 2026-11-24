# A retained state that certifies one of the two source events

After the common geometry-preserving preparation, **an actual later absence of leaf 718 from view 12 certifies that view 0 deleted leaf 662**, within the two stated alternatives. It can never occur after view 0 deleted leaf 718. This witness uses a successful receiver deletion and its returned membership. Observing an error or choosing a recovered endpoint plays no role. The corresponding successful receiver event is possible and is not forced.

This is an analytical consequence drawn after the [native veto replay](NATIVE_RECEIVER_VETO.md). The separate [readback plan](RECEIVER_RETAINED_STATE_PLAN.md) records this timing. It applies only to the original deletion-only atom, the two named source alternatives, and the receiver's indexed membership. Reading that membership as a physical observation remains an additional premise.

## The exact set of possible future memberships

Fix a valid family immediately after a source event. Suppose the receiver chart $B$ consists of its root and children of that root, with no retained grandchildren. Let $Y$ be this chart and let $F$ contain the nonroot members of $Y$ that have at least one holder outside $B$. The possible future $B$ memberships over all legal deletion histories, including the empty history, are exactly
\[
 \{Y\setminus K:K\subseteq F\}.
\]

For necessity, a vertex whose only holder is $B$ can never be deleted in $B$ while the union is fixed. Deletions cannot add a holder elsewhere. The root is also fixed. These facts hold for arbitrary interleaved edits in other charts. For sufficiency, choose any subset $K$ of $F$ and leave all other charts fixed. Each member of $K$ is a local leaf, has a surviving outside holder, and can be removed in any order. Every member in the displayed family thus has a valid witness history. This accounts for existentially reachable states and introduces no scheduler, probability measure or terminal-state rule. [Original atomic rule](https://github.com/proteinfoldingengine/WetLabEngine/blob/e61d5b0e827f7b412824ad46021e2ad6cc6f7875/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py#L24)

## Apply the classification to the two source arms

At the 42-edit common preparation $A=0$ and $B=12$ are the last holders of $q=718$. The receiver has 1,307 retained vertices including the root. It has no retained grandchildren. Compare source $p$, deletion of 662 at $A$, with source $q$, deletion of 718 at $A$.

| Source event | Fixed receiver addresses | Independently removable receiver leaves | Number of reachable receiver memberships |
|---|---|---:|---:|
| Source $p$ | 0 and 5 | 1,305 | $2^{1305}$ |
| Source $q$ | 0, 5 and 718 | 1,304 | $2^{1304}$ |

The removable sets differ only at 718. The entire $q$-source family is therefore precisely the $q$-present part of the $p$-source family. There is no receiver membership unique to source $q$. Every $p$-source membership missing $q$ is exclusive to source $p$. The cardinalities count distinct states and have no frequency interpretation.

There is an actual successful witness. After source $p$ the original `atomic` call removes 718 at $B$, and its verified output has 718 absent. It stays absent under every legal continuation, because this operation can only delete. After source $q$ no chart other than $B$ can ever acquire 718, and the fixed union forces $B$ to retain it forever. To see why the root grade alone is insufficient, deleting the unrelated unit leaf 8 at $B$ succeeds after either source and produces the same local chart in both cases with 718 still present. That unit deletion, like the successful deletion of 718 after $p$, raises the root grade from 242 to 243. It is the leaf's retained identity that resolves the source in the witness.

At the unreduced original cover the same source alternatives give identical removable sets at $B$. Other holders of 718 remain, and histories with a later absence of 718 exist in both arms. The admitted common preparation is consequential even though its starting work table exactly equals the unreduced table.

The immediate event-generated result is a restriction on the receiver's future choices. A later successful local deletion can leave a persistent, one-sided record in the receiver chart. Actual occurrence of that local event and physical access to the resulting state remain open.

[Reachability readback](verify_reachable_states.py) · [Machine-readable witness](reachable_receiver_certificate.json)
