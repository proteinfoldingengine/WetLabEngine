# v16.14F — Obstruction carrier closure

The ordered pruning filtration itself forces canonical quotient carriers but not a transport between them.

## Verdicts

- **ASSOCIATED_GRADED_CARRIER_CANONICAL**
- **INTERGRADE_TRANSPORT_NOT_CANONICAL**
- **OBSTRUCTION_DESCENT_REQUIRES_ADDITIONAL_INVARIANCE**

For the canonical nested kernels K_0⊂K_1⊂...⊂K_m, each associated graded object

G_j = K_j / K_{j-1}

is canonical. The inclusion K_{j-1}→K_j and quotient projection K_j→G_j are forced by the filtration. The abstract external family/direct sum of the quotient objects is therefore legitimate bookkeeping of when distinctions become unrecoverable.

But the filtration alone does not give a canonical nonzero map G_j→G_{j+1}. Inclusion of representatives from K_j into K_{j+1} becomes zero after quotienting by K_j. A reverse/lift map requires choosing a splitting or other additional structure. Likewise, the graded pieces do not canonically reconstruct K_m as embedded representatives without splitting the extension sequences.

For an intrinsic response obstruction T defined on K_j to descend to G_j, the quotient universal property requires

T(K_{j-1})=0.

That condition is not supplied by the filtration alone. Therefore the next first-principles gate is exact and narrow: test whether the already-earned intrinsic obstruction at each pruning stage annihilates the previously lost kernel. If yes, graded obstruction classes are earned. If no, the obstruction contains history across grades and cannot be localized to the newly lost information without extra structure.

No splitting, coarse response map A, geometry, quantum primitive, or external alignment was used.

RED run **36511115866** failed because the implementation was absent. GREEN run **36511159223** passed at commit **74206c3fb1aca45e83ce1aa11ce8e8379eeced3f**.

Time remains pruning / ordered recoverability update.
