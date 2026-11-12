# Target E: output-orbit order check

Date: 2026-11-12. Status: bounded analytical follow-up to T-426 section 6, not a numbered retained stage.

The supplied language consists of compact homogeneous output sets O_H = H W_R for closed subgroups H <= U(E tensor R). Compare their actual sets by inclusion; equal orbits count as the same premise. Sufficiency means O_H avoids the fixed proper-R blind set. Also consider the sublanguage with H connected.

Question: does this language have a greatest sufficient orbit? The proposed answer is no, including the connected sublanguage. This is stronger in scope than T-426's subgroup-order statement but does not claim absence of maximal orbits, a native impossibility theorem, or a universal statement over premise languages.

Proposed witness: L = U(2) tensor U(2), V_t = diag(1,1,1,zeta_t), zeta_t = (1-t^2+2it)/(1+t^2), 0 <= t < infinity; H_t = V_t L V_t^*. V_t fixes the reference pair |00>, |01>. Every H_t orbit is sufficient with sharp proper-R margin 1/(5 sqrt(1+t^2)). Its Hadamard-pair member converges to a blind pair as t -> infinity. Every closed orbit containing all these sufficient orbits would contain that blind limit.

Before running the checker, freeze this plan and checker in GitHub. The checker is an algebra audit, not the proof of the infinite group or limit claims. Expected checks: unit phase, orthonormal marker pair, exact channel on all 16 matrix units, symbolic marginal formula and sharp squared gap, five exact sequence values, blind endpoint with unchanged channel, and retained p-effect contrast 1/5. Adverse control: orthogonality and compact connected group structure still hold at the blind endpoint; these premises cannot be substituted for proper-R sufficiency.

The proof and all source/action/interface choices are SUPPLIED analytical benchmark content. No native producer, availability, new signal threshold, or fixed binary effect is derived. Native bridge NOT_DERIVED; physical result Not claimed; scientific_breakthrough=false. No claim of literary or scientific novelty.
