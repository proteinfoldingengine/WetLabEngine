# Existing visible pool labels can make a handoff guard-independent

Status: proposed conditional theorem; verification/review pending.

## Objects and exact scope
There are finitely many labelled nonhost roots and host h. Distinct active labels occupy known nonempty patterns W_i covering all nonhost roots; D,E occur only at h. Fixed hidden backgrounds Q are disjoint from pool. The source has tau=4 and arbitrary positive floors not exceeding original sizes. Select A on W, m=|W|>=1. At most two stable other role labels K cover all nonhost roots outside W; P is W covered by K, R=W\P, r=|R|. Orders on P/R are supplied static parameters.

Current observation O is the labelled projection onto the ENTIRE existing pool, excluding Q. No fresh marker or other changing hidden field exists. Static source/template/address/certificate data and the initial tau4/floor promises remain supplied; neither tau nor floors nor Q are controller inputs. Exclusive atomic toggle-or-NOOP outcomes exclude other writers, delayed duplicates, compensations and incomplete observation. No fairness is assumed.

The guarded relation checks syntax, floors and3<=tau<=4 before permitting a toggle, and always permits NOOP. The syntax-only relation permits NOOP and a syntactically valid toggle without any floor/band test. We prove equality of these relations RESTRICTED to the issued policy on every reachable promised world. No claim that all requests in the universe are safe, or that a universal native guard has been implemented, follows.

## Sharp cost of an existing-label host addition
For any source whose host lacks A, let F be the nonhost supports not containing A and rho=tau(F), taking tau(empty family)=0. Then

tau(source with +A(h))=min(tau(source),1+rho).

Proof: any old source hitting set remains a hitting set after addition. A together with a minimum hitting set of F hits all nonhost roots and the new host, giving the other upper bound. Conversely, a hitting set after addition either already hits the old host, hence is a source cover, or uses A to cover the host and must additionally cover F. Since A occurs in none of F, that second case needs at least1+rho labels. This exact formula is mathematical, not an observer algorithm for hidden F.

Also tau(source)<=2+rho: A, a cover of F, and E cover the source. Thus a tau4 source has rho>=2 and the prepared source has tau>=3. The four-root triangle {a,b},{b,c},{a,c},{d,e} instead has tau3 and rho_a=1; adding a at the host gives tau2. Under the retained K certificate, rho<=2 as well, so every tau4 source in this class has rho=2 and the first prepared slice has EXACT tau3. This stronger consequence was identified analytically before implementation or enumeration. The initial upper-edge promise cannot be dropped from the general sufficient theorem. Some tau3 sources are safe, but their exact additional residual condition is not provided by this core-only controller.

## Script and uniform safety before issue
Use only existing labels:
1. +A(h), then -D(h).
2. For each p in P, +D(p),-A(p).
3. Add D at every R root; then remove A at every R root.

The end is exactly the swap: D on W, A with E at h, other pool roles and Q unchanged. There is no final host addition, marker cleanup or hidden temporary object. Every syntactic condition follows from the script.

Floors: host preparation adds one incidence before deleting D, leaving the original host size. All nonhost exchanges add before delete; at every slice sizes are at least original. Every command is therefore floor-safe for every permitted floor assignment without reading its values.

Lower band: for any current hitting set H, map D to A once D appears on nonhost roots; otherwise keep D fixed. Fix all other labels, including Q. Images hit every ORIGINAL nonhost root: current D occurs only on original A roots, and A remains confined there apart from the host. Add original D to the image set to cover the ORIGINAL host if needed. This gives a source hitting set of size at most |H|+1, so tau(current)>=tau(source)-1=3. Before any nonhost D addition, the same extension argument applies. Adding the single ORIGINAL host label is a cover argument, not an introduced physical incidence or extra resource.

Upper band: K union {E,A} hits every slice until all deficit roots have received D; K protects P and outside roots even as their A incidences disappear. Thereafter K union {E,D} hits every slice. Each has at most4 labels. Empty deficits are harmless. Thus every prescribed toggle remains in3..4 across EVERY compatible initial Q/floor world, and every issued command is uniformly safe before issue. There is no reliance on an inadmissible request being rejected.

At the endpoint, exchanging the names A,D in the source while fixing Q is a palette permutation, so exact endpoint tau=4. Transient tau3 is allowed, and occurs in the disjoint six-root fixture. This is a different guarantee from the higher-budget exact-tau handoff.

Peak excess is beta=max(1,r): preparation costs1, covered-root duplication costs1, deficit batching costs r. There are exactly2m+2 actual changes in a complete script and no new labels. This is not global path optimality.

## A deterministic current-core request policy
Let c_0,...,c_(2m+2) be the pool-core slices of that static script. They are all distinct. Host incidences distinguish source (D present,A absent), prepared state (both present), and subsequent slices (D absent,A present). Along nonhost edits, n_D+(m-n_A) increases once per toggle and identifies the prefix; the full labelled template identifies its addressed next request. Counts alone are not an off-template validator.

At c_t for t<2m+2 issue the unique next toggle; at c_(2m+2) issue nothing. Outside the promised templates the policy is empty. The policy is a deterministic SINGLE-request map of current core plus static parameters, with no stored phase/counter/transcript or success acknowledgment. It also consumes no syntax/floor/tau query beyond the already observed core template.

Under syntax-only outcomes, induction gives exactly these slices, with arbitrary NOOP loops at each nonterminal slice. Every offered toggle is syntactically valid and uniformly safe by the proof. Consequently the floor/band filter never excludes it: guarded and syntax-only execution have identical complete restricted graphs. This establishes guard redundancy for this protocol, not universal enforcement.

Rank t increases by one on every actual change; the exact endpoint is the sole committed sink and has no offered requests. Every maximal path of actual changes reaches it. Attempts may NOOP forever; no actual selection or progress law is derived.

Unlike the hidden-marker policy, exact completion is constant on every reachable O-fiber. All changing incidences are in the pool, Q is fixed, and there is no marker. For each initial world, core=c_(2m+2) holds if and only if the full carrier equals that world's exact prescribed endpoint. Thus a current-core stopping rule is valid without hidden cleanup certification. This does not assert injectivity across arbitrary Q worlds or derive physical access to O.

## Scientific meaning and remaining origin gap
This reduces a concrete enforcement dependency: native edits in the restricted protocol need no runtime full-state admission calculation. It also removes fresh-marker availability, the set-valued source request choice and unobservable cleanup, at the cost of the stronger tau4 initial promise and transient tau3 allowance.

It does NOT derive initialization/accessibility of the core record, the source admission promise, addressing/certificates or closed-world atomic execution. It does not select realized outcomes or guarantee progress. Native observer origin and universal guard enforcement remain open. Earlier A11 native committed-path theorems remain valid; the new operational conclusion is their C3-style uniform-before-issue/guard-redundancy/observable-endpoint interface for this specified host-role construction, not a new universal connectivity or minimum-repair theorem. No physical force, fundamental time, inserted geometry, dark matter or GR derivation is asserted.
