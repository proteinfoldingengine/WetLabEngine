# Receiver algebra probe: localization by inherited aggregation

Author: proteinfolding-gpt. Date: 2026-10-18 America/Phoenix.
Inspected source head: `ec3a9b585b9b1b4203db399b576dc294e2aed858`.
Status: unreviewed analytical construction supporting receiver_identification. No scientific implementation, numerical campaign, independent acceptance, or native-access closure is claimed.

## 1. Purpose and continuity

The current A candidate is P1 absorption into an initially uninformed retained receiver. This note is B support for that candidate: an explicit correspondence between the grade update and a candidate retained observable algebra. It does not propose another motion, decoder, register, or measurement instrument.

Grok draft 7 already incorporates the GPT corrections to complete-fiber nuisance and the draft-6 information-loss claims. Preserve those revisions and the frozen draft-2/draft-5 evidence. The present task is access, not another loss-law extension.

The positive construction below identifies precisely which *joint input observable* becomes a *local output observable*. It uses the existing aggregation rather than adding a consumer operation. The construction is mathematical. The fact that its algebra is physically available to a receiver does not follow from constructing it; that is the remaining RAS identification to investigate.

## 2. Types and finite domain

Let X be a finite prefix-closed carrier, Y a root-containing prefix-closed retained subset, and r:X->Y the inherited nearest-retained-ancestor retraction. FCV P0/P1 gives

    (mu_r(x))_a = sum_{v:r(v)=a} x_v.                       (1)

For this probe take nonnegative integer grades and fix N>=1. Use the finite configuration domains

    Omega_X(N) = {x in Z_{>=0}^X : sum_X x <= N},
    Omega_Y(N) = {y in Z_{>=0}^Y : sum_Y y <= N}.            (2)

The bound is an analytical restriction for finite algebras, not a physical capacity or a rule forcing pruning. P1 conserves total grade and therefore maps (2) into (2). FCV P2 supplies zero extension I:Y-grades->X-grades with mu_r I=id; I also preserves (2). Consequently mu_r is surjective on these formal domains. This is not a claim that every point of either domain is physically preparable. Integer grades are the declared instance used in receiver_identification; FCV's general additive-monoid and physical-realizability boundaries remain in force.

There are three different objects:

1. The address set X and functions on addresses.
2. A grade configuration x indexed by X.
3. Functions of whole configurations, A_X=C(Omega_X(N)).

Only object 3 is the candidate observable algebra in this note. A grade vector is not itself a quantum density matrix. No tensor-product factorization of a constrained preparation domain is assumed.

## 3. The observable correspondence determined by P1

Define the configuration-observable pullback

    alpha_r:A_Y->A_X,   alpha_r(f)=f composed with mu_r.     (3)

It is a unital injective *-homomorphism: composition preserves products, complex conjugation and constants, and surjectivity of mu_r makes alpha_r injective. Its image

    A_ret(r)=alpha_r(A_Y)                                  (4)

is exactly the algebra of functions constant on the fibers of the *configuration map* mu_r. These fibers are not the address fibers r^{-1}(a). P2 provides I^* alpha_r=id, where I^*(g)=g composed with I. This fixes the comparison without choosing a Hilbert register or a controlled-add dilation.

For a retained address a, let q_a^Y(y)=y_a and let B_a^Y be the algebra of functions of q_a^Y. Then

    alpha_r(q_a^Y)(x)=sum_{v:r(v)=a} x_v,
    alpha_r(1_{q_a^Y in D})(x)
        =1_{sum_{v:r(v)=a} x_v in D}.                      (5)

Thus the entire candidate local output algebra B_a^Y is determined by the ancestral fiber sum. This is the explicit observable-level content of the existing holder theorem. No READS assignment is needed to compute (5).

Before the event, the same address a has coordinate q_a^X(x)=x_a. In general q_a^X and alpha_r(q_a^Y) are different observables. Address stability retains a's identity; it does not identify these two functions or assert that the old value survives absorption. P2 gives

    I^* q_a^X = q_a^Y = I^* alpha_r(q_a^Y),                 (6)

which aligns the two descriptions on the zero-extension section. Equation (6) is a structural comparison, not proof of a physically preparable blank-source state or of physical ownership.

## 4. State restriction and one initially blind receiver

For any probability law p on the formal configuration domain, write omega_p(f)=sum_x p(x) f(x). The probability law here describes uncertainty over configurations; it is not obtained by normalizing a grade vector. Then

    omega_out(f)=omega_p(alpha_r(f)),
    omega_out(f)=sum_y (mu_r)_*p(y) f(y).                   (7)

Equation (7) follows by grouping the finite sum over mu_r^{-1}(y). It says that restriction of omega_p to (4), identified through alpha_r, is exactly the P1 output state on the configuration algebra. Restricting further to B_a^Y gives the holder's grade law. This statement needs no product-nuisance assumption: it also holds for correlated p. Product assumptions are needed for the stronger claim that the holder is as informative as the whole output, not for (5)-(7).

For a definite configuration x, (7) is the evaluation state at mu_r(x). It supplies an actual value *within the specified classical model*. It is not a derivation of physical outcome selection or an assertion that an ensemble probability has already been read.

Use the existing inside/outside form on X={o,a,u,v}, with a and v children of o and u a child of a. Retain Y={o,a}. In order (o,a,u,v), take

    x_inside =(0,0,1,0),
    x_outside=(0,0,0,1).                                  (8)

Both have total grade 1. Both initially restrict to the same state on the *entire formal local algebra* B_a^X, because x_a=0. P1 gives, in order (o,a),

    mu_r(x_inside) =(0,1),
    mu_r(x_outside)=(1,0).                                (9)

The same receiver address a has changed from a common value 0 to distinct values 1 and 0. The output projection e_a=1_{q_a^Y>0} separates them exactly. Its pullback is 1_{x_a+x_u>0}, a joint input observable; the earlier local projection 1_{x_a>0} was zero in both cases. The separating projection is invariant under positive global rescaling, so this particular witness does not require absolute source calibration.

This is localization of an existing distinction, not global information creation. The full inputs in (8) were already distinct. They remain distinct after (9). Both retained coordinates distinguish this two-location pair, so it is not an instance of the single-source unique-holder theorem. The formal two-point calculation does not establish that both configurations share legitimate native preparation histories. Use the existing preparability ledger for that obligation; do not infer permission to append from (8).

## 5. Composition and the physical-access target

For a later contraction s:Y->Z, inherited P1 composition gives

    alpha_{s composed with r}=alpha_r composed with alpha_s. (10)

This earns the observable transport from existing maps, without a new scheduler or consumer. The content of a later local observable is determined by its cumulative ancestral fiber. It does not assert that every earlier local projection remains available or that a previous grade is recoverable.

The strongest justified conclusion is therefore:

> Given the admitted P1 operation on the grade domain, its output state and candidate local observable algebra are fixed by (3)-(7). In (8), a jointly supported distinction becomes a distinction at the same retained receiver address.

To turn this into the requested accessible-state result, establish from an inherited operational source that the receiver's actually available observations and actual event are represented by this correspondence. One need not physically implement every function in A_Y or adopt a tensor-product quantum dilation: one independently justified local effect corresponding to e_a in the witness can suffice for post-event separation. Full initial blindness must still be established for the receiver's complete pre-event accessible state, not just for a selected effect.

In precise terms the outstanding interface is:

    actual retained receiver algebra/state and actual event
       represented by B_a^Y, omega_p composed with alpha_r,
       with the same receiver initially represented by B_a^X. (11)

Equation (11) is a proof obligation, not an axiom introduced by this note. A theorem that its hypothetical Lüders measurement is nondisturbing does not establish (11). In a commutative algebra a nonselective Lüders map is the identity; that identity alone neither produces nor makes an outcome accessible.

The user's actual atemporal measurement is accepted as the empirical occurrence input for this research direction. No external clock or proof of inevitable occurrence is requested. However, identifying that event with a particular P1 contraction on an actually owned state remains distinct from accepting that a measurement happened.

## 6. What this changes in the work plan

The positive algebraic correspondence is now explicit, including the three types, P2 comparison, state restriction, equal-total witness and initial local blindness. It avoids a supplied quantum copying implementation. It does not discharge a new physical-access premise: receiver_identification already contained the coordinate consequence; this note makes its proposed connection to RAS precise.

The next useful source-backed construction must establish (11), preferably for the single effect e_a, using an existing receiver observation/operation with provenance independent of the desired separation. A source already declaring the grade algebra operational would close that portion conditionally on the native preparations and the typed event. v15.11 declares RAS and RCR as supplied primitives and does not identify them with this grade-configuration algebra; FCV explicitly leaves physical realization unresolved. Neither source currently supplies (11).

Do not launch another loss-law, supplied-motion or numerical campaign on this note. Do not label the algebra construction as an available physical measurement. Preserve the current draft-2/draft-5 review hold. A consolidated whole-argument review should assess (11) if a source-backed identification is found; meanwhile this document remains an unreviewed positive probe, not a completed milestone.

## 7. Evidence and review scope

Claim-bearing sources are pinned in SOURCE_MANIFEST.json: FCV PROOFS P0-P2, FCV TYPE_LEDGER, v15.56 source_pushforward, v15.11 RAS/RCR report, current receiver_identification draft 7, the typed interface handoff, and the accepted measurement-first argument. Their exact Git blob identities were recomputed from retrieved bytes. No archived scientific module was imported or executed.

Equations (3)-(7) are standard finite function-algebra pullback and state restriction, explicitly proved here; no mathematical novelty is claimed. Equations (8)-(9) are the established inside/outside witness in a minimal formal instance, not a new preparation theorem. The contribution is a precise candidate identification to test, with no extra mechanism encoded. Independent mathematical/physical review has not occurred. Native bridge remains NOT_DERIVED.
