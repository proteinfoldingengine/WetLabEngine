# Charge selection and the native-grade admission boundary

Status: **NEW-assumption analytical candidate; native bridge NOT_DERIVED.** This is a bounded test of an explicitly added physical law, under the user's delegated exploration of new assumptions. It is not a native derivation, numerical campaign, numbered research stage, certification, or claim of a new conservation theorem. All results and countermodels below were derived before the independent review freeze.

## 1. Question, unchanged source/receiver, and premise ledger

Can global additive conservation prevent the unread environment from absorbing the removed distinction, thereby forcing the same nominated receiver's fixed effect to respond? Does the conserved native extensive grade supply the needed source charge?

Keep the already supplied source and receiver benchmark, with an explicitly supplied generalization of the bath. The source basis is `(o,p,u,v)`, its retained projection is `Q=I_S-pi_u`, and its exact channel is

\[
 C(\rho)=Q\rho Q+\rho_{uu}\pi_p,\qquad \pi_j=|j\rangle\langle j|.
\]

The original location example had a blank qubit E. Here E is explicitly allowed finite dimension `d>=1` and an arbitrary fixed density matrix `tau`; set `k=rank(tau)>=1`. The receiver R remains the **same qubit**, initially `|0_R>`, with the **same effect** `F_R=|1_R><1_R|`. A single source-independent unitary U acts on S tensor E tensor R. The initial state is `rho tensor tau tensor |0_R><0_R|`; tracing out E,R must give C(rho) for **every source density matrix**, equivalently all source matrix units. Initial correlations are not admitted.

Keep the two source inputs fixed:

\[
 \rho^{(0)}=\operatorname{diag}(1,1,2,1)/5,\quad
 \rho^{(1)}=\operatorname{diag}(1,1,1,2)/5.
\]

Write `q(rho)=Tr[(I_SE tensor F_R) U(rho tensor tau tensor pi_0,R)U†]` and signed contrast `Delta=q(rho^(0))-q(rho^(1))`.

| Premise | Status and scope |
|---|---|
| Native retained map `P x=(x_o,x_p+x_u,x_v)` and total-grade preservation | INHERITED source mathematics within its typed scope |
| Actual event occurrence | ACCEPTED INPUT; no physical-time coordinate is introduced |
| Hilbert factorization S,E,R; normalized source encoding; exact all-input C; independent product preparation; initially blank qubit; same owned accessible F_R | SUPPLIED benchmark/correspondence, not native-derived |
| Physical source charge `Q_S=pi_u` | NEW; it is not the native preserved total grade |
| Environment Hermitian charge Q_E, receiver charge F_R, additive total `K=Q_S+Q_E+F_R`, and `[U,K]=0` on the **whole** joint space | NEW physical law and charge/effect identification; tensor identities implicit |
| `spec(Q_E) intersect (spec(Q_E)+1)=empty` | NEW exclusion of bath charge differences equal to one |

The unit is the proposed source charge difference `q_u-q_p=1`, also the fixed receiver charge gap. Q_E is a charge observable, not an identification of native grade with physical energy. No stationarity, thermality, diagonality, full rank, or invariance of the support of tau under Q_E is assumed for the positive theorem.

## 2. Conditional selection theorem

**Theorem A.** Under the supplied benchmark and all NEW charge assumptions above,

\[
 q(\rho)=\rho_{uu}\quad\hbox{for every }\rho,\qquad \Delta=1/5.
\]

In particular the receiver stays blank on every input supported on the retained subspace, and is `|1_R><1_R|` on the erased basis input `pi_u`. This derives the quiet-reference condition within the added class. It does not derive that class from native P1.

**Proof.** Let `q_u=1` and `q_o=q_p=q_v=0`. For source labels s,t and receiver bits r,r', define the bath operator block

\[
 B_{sr;tr'}=\langle s,r|U|t,r'\rangle.
\]

Global commutation gives

\[
 (Q_E+q_s+r)B_{sr;tr'}=B_{sr;tr'}(Q_E+q_t+r').
\]

In an eigenbasis of Q_E, a matrix element can be nonzero only when the output bath eigenvalue minus the input bath eigenvalue is `q_t+r'-q_s-r`. The spectral exclusion therefore sets to zero every block requiring bath shift +1 or -1. This is an identity on the **entire bath space**, before restricting to the occupied support of tau. Coherent tau and non-invariant support consequently cause no loophole.

For each retained a in `{o,p,v}`, exact C maps `pi_a` to the pure system state `pi_a`. For every vector in supp(tau), positivity therefore confines the joint output to system a. The block `B_(a,1);(a,0)` needs bath shift -1 and is zero; the receiver is 0. For input u, exact C confines the output to system p. The block `B_(p,0);(u,0)` needs bath shift +1 and is zero; the receiver is 1. Purity of the reduced system justifies these support statements even when tau is mixed: diagonalize tau on its support and use positivity of every occupied summand.

The map rho -> q(rho) has a POVM effect M on S with `0<=M<=I`. Its diagonal entries are `M_aa=0` on retained labels and `M_uu=1`. Positivity gives `|M_ij|^2<=M_ii M_jj`, eliminating every off-diagonal entry. Thus `M=pi_u`, proving the law for all coherent as well as diagonal rho. The fixed contrast is `2/5-1/5=1/5`. QED.

The theorem specifies the effect probability, not a general population-only formula for the complete receiver state. Source p/u coherence can survive in receiver off-diagonal entries.

## 3. Nonempty class and controls

### 3.1 Admitted writer for every bath state

Let W_R be the global basis permutation on S,R swapping `|u,0_R>` and `|p,1_R>`, fixing all other basis states, and acting as identity on E. The two swapped states have the same S,R charge 1, so W_R commutes with K for **every Q_E**. On a blank receiver it acts as

\[
 |a\rangle|0_R\rangle\mapsto|a\rangle|0_R\rangle\ (a=o,p,v),
 \qquad |u\rangle|0_R\rangle\mapsto|p\rangle|1_R\rangle.
\]

Retained coherences are preserved; coherences involving u vanish after tracing R; `pi_u` maps to `pi_p`. Hence it implements exact C on every matrix unit for every tau. Choosing Q_E=0, for example, meets spectral exclusion. Theorem A is not a statement about an empty class.

Spectral bandwidth smaller than one is sufficient for exclusion but not necessary: `{0,2}` is an allowed bath spectrum. We do not claim the no-unit-gap condition is necessary for delivery for every particular Q_E and tau.

### 3.2 Remove spectral exclusion: a conserving blind realization

Take E to be a qubit with `Q_E=|1_E><1_E|` and any tau. Use `U=SWAP_ER W_R`. Both factors commute with `pi_u+Q_E+F_R`; the SWAP exchanges identical bath/receiver charge observables. It acts only on E,R after W_R, so the reduced source channel remains C for all inputs. Before the SWAP E is independent in state tau; afterward the **complete receiver state is tau**, independent of rho. Thus Delta=0, including when tau is full rank. The bath has an allowed unit gap, so spectral exclusion fails. This control violates the quiet-reference condition iff tau is not the blank receiver state; the pure blank bath is an important exception.

### 3.3 Remove conservation: the fixed effect can be blind

Take Q_E=0 and `U=H_R W_R`, with H the standard Hadamard. Exact C and spectral exclusion still hold. Both fixed diagonal source inputs give q=1/2, so Delta=0. Conservation fails: a retained charge-zero basis input acquires a nonzero receiver charge component. This is fixed-effect blindness for the supplied pair, **not** whole-receiver blindness. For general coherent rho, `q(rho)=1/2-Re(rho_pu)`.

These two controls show that neither added restriction can simply be omitted from the general implication without a replacement. They do not establish a universally weakest set of delivery axioms.

## 4. Equal source charge: blank receiver and an admission obstruction

Now **replace**, rather than supplement, the NEW source charge pi_u by a diagonal source charge

\[
 Q_S=\sum_j q_j\pi_j,\qquad q_u=q_p.
\]

Keep the supplied benchmark, receiver charge F_R, no unit gap in Q_E, and global conservation of `Q_S+Q_E+F_R`. Other source charge values are arbitrary. In particular this class includes the normalized native total's canonical diagonal representative `Q_S=I_S`.

**Theorem B.** Every admitted realization in this equal-charge class leaves R blank for every source input. A necessary condition for exact C is `2k<=d`. Therefore with a finite full-rank bath (`k=d>=1`) this class of exact implementations is **empty**.

**Proof.** For retained input a the only system output is a, and for input u it is p. In every case specified by exact C, the source input and output charges agree. Receiver output 1 therefore requires bath shift -1, forbidden by spectral exclusion. Pure-output support and the positive-effect argument from Theorem A give zero receiver excitation for every rho, hence pure blank R.

For the input `rho_*=(pi_p+pi_u)/2`, the initial joint rank is 2k. Unitary conjugation preserves rank. Its output source is the pure state `pi_p`, and its receiver is the pure blank state, so its full joint output is `pi_p tensor sigma_E tensor pi_0,R` with rank at most d. Thus `2k<=d`. Equivalently two orthogonal occupied input subspaces of dimension k each would have to fit into `|p> tensor E tensor |0_R>`. Full rank violates the necessary inequality. QED.

**Necessary does not mean sufficient.** Set `d=2`, `Q_S=I_S`, `Q_E=diag(0,1/2)`, and `tau=|0_E><0_E|`. Then `2k=d` and spectral exclusion hold. Conservation forces both orthogonal p/u inputs with bath 0 and receiver 0 to the same one-dimensional output sector `|p,0_E,0_R>`, which is impossible. Charge-sector multiplicity imposes additional restrictions.

**Nonempty blank boundary.** With a pure qubit bath and `Q_E=0`, take W_E to swap `|u,0_E>` and `|p,1_E>`, leave other S,E basis states fixed, and act trivially on R. When `q_u=q_p`, it commutes with the total charge, implements all of C for the blank bath, and leaves R blank. Thus Theorem B is not a general impossibility for rank-deficient baths.

The full-rank obstruction concerns these finite, exact, additive-charge, product-input assumptions. It is not an impossibility theorem for native P1, arbitrary open systems, infinite baths, or all possible physical correspondences. An empty class cannot be counted as a successful forced-signal derivation.

## 5. Native provenance and comparison with the earlier balance attempt

At research parent `2ab565c3f5bf10305a96ddeef30901de49959ba5`, FCV P0-P2 and the type ledger give the source maps `P_XY:F^X->F^Y` and `I_YX:F^Y->F^X`, with `PI=id`. For the four-label example, P preserves total grade:

\[
 \mathbf1_Y^T Px=\mathbf1_X^T x.
\]

A pushforward-compatible weighted functional obeys `c_X=P^T c_Y`, hence `c_u=c_p`; it need not have equal weights at every address. In the supplied normalized diagonal encoding, the canonical diagonal observable of the total is **I_S**, not pi_u: the total is already retained within the represented source S. On the literal output carrier it is I_Y (or Q after embedding in S), with expectation one on all allowed outputs. In particular `C*(I_S)=I_S` while `C*(pi_u)=0`. Diagonal encoding alone does not determine arbitrary off-diagonal additions to an observable; no such physical extension is derived here.

The old `constructive_candidates/joint_balance_delivery/ATTEMPT.md` already calculated

\[
 C^*(Q_S)=Q_S-(q_u-q_p)\pi_u.
\]

Its **no-environment all-input first-moment** balance was `W†(Q_S+delta J_R)W=Q_S`, with `delta=q_u-q_p` and `J_R=I_SE tensor F_R`. For `delta!=0`, that normalization made the balance equivalent to the sharp writer effect `W†J_RW=pi_u`, itself equivalent to `J_RW=W pi_u`. That output relation is not new. The old note explicitly distinguished its isometry balance from global unitary commutation. It also showed that a charged E can absorb the distinction, preserving both W_R and W_E under total balance.

The present added hypothesis is different: a globally commuting unitary plus a bath spectrum that forbids the required one-unit absorption. This exact spectral restriction was not formulated in the inspected earlier attempt and response. The new contribution to this bounded branch is its sufficient-condition proof, nonstationary-bath scope, and the equal-charge admission boundary. This is a narrow comparison, not an archive-wide novelty claim. It does not repair the prior failure to derive physical conservation from source accounting.

The old response correctly retained the native restriction loss: `z=(id-IP)x=x_u(e_u-e_p)`, `Pz=0`, and `Def_S(x)=(c_u-c_p)x_u`. Selecting the singleton functional produces x_u, but a source deficit is not an allocated physical receiver charge. FCV `R_XY:W_X->W_Y` is restriction of potential quotient classes, not the physical R; its response identity does not supply a joint event or owner assignment.

| Source inspected at the research parent | Git blob | Relevance |
|---|---|---|
| `foundational-closure-verification/PROOFS.md` | `a21acad73c80cb748f2e42c244f6db53146c2bf2` | Native source maps, conserved total, response restriction |
| `foundational-closure-verification/TYPE_LEDGER.md` | `aa2d66adbfd552188dd3dec9270824fd605981d8` | Distinguishes source and potential carriers |
| `research/physical-bridge/P1_NATIVE_PRUNING_TYPING.md` | `230cd20e8db42b2538862b247a2b8383a98deaad` | Native typing is not a joint quantum implementation law |
| `research/physical-bridge/p1_receiver_location_resolution/RESULT.md` | `4182ba347f8c11bad63315ffa6395c496ddfa498` | Exact benchmark and same-R W_R/W_E counterexample |
| `research/physical-bridge/constructive_candidates/joint_balance_delivery/ATTEMPT.md` | `460adf6765933130ca718e850992cdce92320ae7` | Earlier writer-equivalent balance and environmental escape |
| `research/physical-bridge/constructive_candidates/joint_balance_delivery/REVIEW_RESPONSE.md` | `e26e6a39a1b33e74c896141694d4453d3cd9f49b` | Restriction deficit is valid but receiver allocation remains absent |

All table paths are relative to `ResearchHistory/UQCF-GEM/`. The immutable review packet supplies these documents and the current owner-action directive; source identities must be checked, not inferred from this table.

## 6. Disposition and next native obligation

The added physical charge law plus bath spectral exclusion is a sufficient conditional route to the unchanged fixed effect. Substituting the native total does **not** recover that result: in this same restricted class it leaves R blank and, for a full-rank finite bath, prevents the exact reset from existing.

The native research obligation is still to identify an inherited event operation and its same-owner action/access, or explicitly justify an additional physical correspondence. Native extensive-grade conservation alone is not evidence for `Q_S=pi_u`, `[U,K]=0`, the bath exclusion, or accessible ownership of F_R. No detector, force, GR law, empirical signal, physical energy, or fundamental time has been derived.

For literature context only, additive globally conserved observables are standard in quantum implementation restrictions; see Kuramochi and Tajima, *Wigner-Araki-Yanase theorem for continuous and unbounded conserved observables*, Physical Review Letters 131, 210201 (2023), https://arxiv.org/abs/2208.13494. The elementary finite block proof here is self-contained. The cited measurement theorem is not asserted to prove this reset result or the native correspondence.
