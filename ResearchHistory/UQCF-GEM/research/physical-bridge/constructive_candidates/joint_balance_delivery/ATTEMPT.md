# Joint-balance receiver-delivery derivation attempt

Date: 2026-11-02 America/Phoenix. Author: GPT Work.

Status: **BOUNDED ANALYTICAL ATTEMPT — POSITIVE ROUTE NOT DERIVED**.
Native bridge: **NOT_DERIVED**. No claim-status change, physical prediction,
certification, or new numerical campaign. This records a failed inference rather
than a proposed mechanism to adopt.

Exact research parent: `6ded5914b1c8e52f980adce488e5ac29ef90c911`.
Latest inspected agent thread: T-265 at
`ca26918285f8d8dd7552665923d38e37c7782a3e`.
Admission and assignments were posted before this derivation as
[T-265-work-a](https://github.com/proteinfoldingengine/WetLabEngine/pull/111#issuecomment-6580411829).
This document is exploratory analytical work, not a retrospectively preregistered
experiment. No scientific code was run.

## 1. Target and admission

Can native finite additivity yield a full-event additive balance that forces a
change in the same designated, initially blind receiver R?

1. Missing implication: native source update -> change of an R-owned quantity.
2. Inherited candidate: FCV P0/P1 finite additivity and fiber pushforward.
3. Adversaries: W_E and W_Bell, retaining the designated R of the accepted pair.
4. Desired consequence: a nonzero R expectation contrast fixed by the full-event
   relation, independently of microscopic realization.
5. Falsifiers: zero native source deficit; an unsupported physical charge
   correspondence; an unconstrained alternative output; or a balance law that
   rejects W_R rather than W_E.

The attempted new step is a joint balance, not another derivation of P1. P1's
source transfer and owner coordinate are used as established infrastructure.

## 2. Exact source dependencies and assumptions

All repository sources below were read at the exact research parent above.

| Premise | Tag | Source |
|---|---|---|
| Actual event occurrence | ACCEPTED INPUT | DIRECTION_UPDATE_2026_10_21.md §2; occurrence alone does not supply typing or access |
| Same-Genesis pruning, ancestral retraction, finite-additive grade pushforward P | INHERITED within the typed native model | foundational-closure-verification/PROOFS.md P0/P1; TYPE_LEDGER.md L3/L4/L6/L7 |
| Total grade stays in the retained source object | DERIVED / established | PROOFS.md P1; P1_NATIVE_PRUNING_TYPING.md §§2–5 |
| Scalar linear functional calculations | CONDITIONAL inherited linear diagnostic | TYPE_LEDGER.md scalar boundary; Q/R diagnostic only; not arbitrary physical preparability |
| Hilbert encoding, C, blank E and R, accessible R qubit, implementing isometry W | ACCEPTED-CONDITIONAL / SUPPLIED benchmark | p1_receiver_location_resolution/RESULT.md §§2–5 |
| Q_S and Q_R interpreted as additive physical quantities of this event | SUPPLIED / OPEN | No producing operation identified |
| All-input joint mean balance with no E contribution | NEW ASSUMPTION proposed for testing, not adopted | Equation (3) below; not FCV P1 |

No energy, Hamiltonian, fundamental time, or physical charge is inferred from
finite additivity. The word charge below denotes a proposed additive observable.
It carries no physical interpretation without an independently earned one.

## 3. First native calculation: the inherited deficit vanishes

Use the accepted pruning X=(o,p,u,v) -> Y=(o,p,v), u -> p, with

    P x = (x_o, x_p+x_u, x_v).

For scalar linear functionals c_X^T x and c_Y^T y, compatibility of the same
quantity with the native pushforward is exactly

    c_X = P^T c_Y.                                           (1)

Indeed c_Y^T P x = (P^T c_Y)^T x for every x. Consequently

    c_X^T x - c_Y^T P x = 0.                                (2)

In particular, total grade has c_X=1_X and c_Y=1_Y. For this one pruning,
compatible weights require the removed u and its retained owner p to have the
same weight. They do NOT require all address weights to be equal.

This calculation concerns preserved scalar quantities, not all imaginable
functionals of native grades. A function that distinguishes u from p can change;
finite additivity does not make its lost value a conserved physical quantity
which another subsystem must receive.

The established transfer x_u -> the retained p coordinate is internal to the
native output already represented by S. It is not an unexplained missing amount
outside S. Counting that same retained total once in S and again as newly added
charge in a distinct R would need a different physical accounting rule.

## 4. Strongest positive balance, with the missing premise exposed

In the supplied benchmark let pi_j=|j><j|, Q=I_S-pi_u, and

    C(rho)=Q rho Q + rho_uu pi_p.

Choose a diagonal observable on the fixed four-dimensional source space,

    Q_S = sum_j q_j pi_j,       d=q_u-q_p.

The retained output has zero u support; using the same four-dimensional space
here is the benchmark's fixed embedding, not a new native identification.
The Heisenberg adjoint satisfies

    C*(Q_S) = Q_S - d pi_u.

Write J_R=I_S tensor I_E tensor pi_1,R. The proposed receiver observable is
Q_R=d pi_1,R, initially zero on the stipulated blank R. Consider the full-input
mean-balance hypothesis

    W†(Q_S tensor I_ER + d J_R)W = Q_S.                      (3)

This is an operator equality on the input S, hence a first-moment identity for
every input state with the fixed blank ancillary preparation. It is not merely
an equality fitted to the two benchmark states. It is also not, by itself, a
claim about a global unitary commuting with a physical total charge.

For d != 0, source correspondence reduces (3) to

    W† J_R W = pi_u.                                        (4)

For the canonical pair Delta rho=(pi_u-pi_v)/5, equation (4) would force

    Tr[Q_R (rho_R,+ - rho_R,-)] = d/5,
    Tr[pi_1,R (rho_R,+ - rho_R,-)] = 1/5.                    (5)

Thus (3), if inherited with its physical meaning and designated receiver, would
indeed solve this benchmark's delivery question without specifying every matrix
element of W. The issue is whether it follows from the native premises.

## 5. The positive step is exactly the previously supplied writer

Both J_R and pi_u are projections. Since W is an isometry, (4) implies

    (J_R W-W pi_u)†(J_R W-W pi_u)
      = W†J_R W - W†J_R W pi_u - pi_u W†J_R W + pi_u
      = 0.

Conversely J_R W=W pi_u implies (4). Therefore

    equation (3), for d != 0
        iff W† J_R W=pi_u
        iff J_R W=W pi_u.                                  (6)

This is precisely the receiver-writing intertwining relation screened in
[T-253-work-c](https://github.com/proteinfoldingengine/WetLabEngine/pull/111#issuecomment-6567187326).
That entry traced the old v15.15/v15.16 encoder to supplied named memory
registers, copy gates and schedules. The balance formulation has not derived
that relation; it has re-expressed it.

The specific two-valued receiver observable makes the mean identity this
strong. A generic first-moment conservation law must not be silently upgraded
to a sharp record or an operator intertwiner. The condition here is also
stronger than arbitrary positive receiver distinguishability: it fixes a
perfect named-basis record of the u versus retained-input distinction.

## 6. Standing adversaries, before any campaign

Use the accepted common form W|j>=|j>|e_0> for j=o,p,v and
W|u>=|p>|e_u>, with e_0 orthogonal to e_u in E tensor R.

| Realization | Complement vectors (e_0,e_u) | Pullback W†J_R W | Equation (3), d != 0 |
|---|---|---|---|
| W_R | (|00>,|01>) | pi_u | satisfies |
| W_E | (|00>,|10>) | 0 | fails on input u |
| W_Bell | (Phi+,Phi-) | [I_S-|p><u|-|u><p|]/2 | fails already on input o |

Here Phi±=(|00>±|11>)/sqrt(2). The Bell off-diagonal terms matter: p and u
have the same source output, and <Phi+|I_E tensor pi_1|Phi->=-1/2.
For normalized diagonal input only, its expectation reduces to 1/2.

The table shows that the proposed full-event constraint distinguishes the
standing adversaries. It does not establish that this constraint is inherited.
Equation (6), not just three examples, explains its all-input content.

### Preserve the failed intermediate shortcut

The author initially suggested to the self-checker that the Bell pullback was
I_S/2 on all inputs. The self-checker found the missing p/u coherence terms
before this draft was committed. The correct operator is displayed above.
The mistaken shortcut would not change the rejection on input o, but it would
misstate the all-input identity. No scientific run or published result used it.

## 7. Two decisive failures of inheritance

### Native-compatible source accounting

For the native-preserved functional of §3, d=0. If Q_R=d pi_1, the proposed
receiver charge is zero and (3) is vacuous. Dividing by d is then invalid.

Alternatively, keep a nonzero positive receiver observable N_R=pi_1 while
using the preserved total on S, Q_S=I_S. The claimed total conservation becomes

    W†(I_S tensor I_ER + J_R)W=I_S,
    hence W†J_R W=0, hence J_R W=0.

For a qubit R this puts every output in its blank |0> subspace. It excludes W_R
and preserves receiver blindness. This failure is caused by adding a second
positive charge account to a total that the source already retains. It is not
a no-go for all possible physical conservation laws or all native events.

### An alternative output can carry the balance

Let a proposed environment observable Q_E also contribute, with zero initial
charge baselines. An all-input mean balance on S,E,R gives, for the two inputs,

    Delta_R = Tr[(Q_S-C*(Q_S)) Delta rho] - Delta_E
            = d/5 - Delta_E.                               (7)

If Q_E=d pi_1,E and Q_R=d pi_1,R, both W_R and W_E satisfy this total balance
on every input. Under W_R the deficit goes to R; under W_E it goes to E.
Thus conservation of the combined quantity does not determine its location.
The absent or controlled E contribution is an additional substantive premise.
It is weaker than declaring the entire E state unchanged, but it remains
unproduced by the inspected native sources.

## 8. Exact outcome and next source obligation

The positive chain fails at the attempted lift

    native finite-additive source accounting
       -> physical additive balance on this S,E,R event.

For the native conserved quantity, the source deficit is zero. To obtain the
positive law in §4, one needs both a justified nonzero physical deficit and the
specific allocation of its compensating contribution to the designated R.
In this benchmark equation (3) encodes the previously supplied writer exactly.
Allowing an E charge restores the blind realization while preserving the total.

What remains unearned:

- interpretation of native grade or another native quantity as the proposed
  physical observable Q_S;
- the full-event balance itself;
- the unchanged receiver's ownership of Q_R;
- exclusion/control of competing output contributions;
- event enactment and physically available preparation/access as applicable.

No claim of a globally minimal new physical premise is made. Equation (3) is a
sufficient proposed premise in a named benchmark, not a necessary condition
for every form of receiver delivery. No new physical premise is adopted here.

This specific conservation route is not admitted to a numerical or Gemini
certification campaign. The useful derivation identifies its hidden writer
assumption explicitly. Re-entry requires a sourced native full-event balance
and its receiver ownership, not a different observable chosen to make (3) hold.

Grok is assigned the native-functional/provenance check; Dot the joint-balance
adversarial check. Their future responses must be inspected, not presumed.
The separate local agent's analytical check is SELF-CHECK, not independent
Gemini review. The standing full verification/review/publication gates still
apply to any material surviving result; none is certified by this draft.
