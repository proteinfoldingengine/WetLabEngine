# Protected grading: recovered sources and one occupied-record candidate

Author: proteinfolding-gpt. Date: 2026-10-18.
GitHub inspection baseline: `a8cf8efe2818b88fbf002803dff096a0ac2c32fa`.
Status: source recovery and unreviewed analytical continuation of the existing single-transfer candidate. Native interaction/access NOT_DERIVED. No scientific execution or new mechanism implementation.

## 1. Constructive result

The recovered v10.1 report supplies a more concrete candidate for the occupied/empty record than an unnamed scalar coordinate: a graded object `(H,N)`, with nonnegative integer-spectrum operator N, and additive composition

    N_AB = N_A tensor I + I tensor N_B.                       (1)

The corresponding candidate binary effect is

    Q = 1_(0,infinity)(N).                                   (2)

This effect is determined by N's positive spectral subspace. Its definition requires neither an absolute energy calibration nor a new numeric decoder. It is a mathematical candidate effect; writing (2) does not prove the receiver can measure or otherwise use it.

The positive transfer target is now specific: identify the inherited retained owner with an already justified graded output object, and show that the actual event carries the source-plus-owner grade into that output. A grade-preserving event would then force an occupied record from a positive-grade input and an empty record from a zero-grade input. Section 3 proves this consequence without choosing a copying gate, beam splitter, or particular outcome law.

The source recovery also exposes a material premise boundary. v10.0 explicitly introduces the protected token as a new physical axiom; v10.1 explicitly retains the grading and grading-preserving processing as extra structure. They do not derive those physical premises from the earlier ungraded theory. This boundary must accompany their reuse.

## 2. What was recovered, and the exact genealogy limit

The three original reports are preserved byte-for-byte under `originals/`:

| Source | Positive inherited content | Original qualification |
| --- | --- | --- |
| v10.0, Minimal Protected Source Primitive Consistency | One-generator positive monoid; unit fixing gives amount n; independent composition adds n | Introduces a protected source token explicitly; physical token identity and conservation are new assumptions |
| v10.1, Protected Token Naturality / Splitting | Graded object `(H,N)`; additive tensor rule; vacuum neutrality; grading intertwining under suitable maps | N and restriction to grading-preserving operations remain additional structure; factor count cannot replace N |
| v10.2, Protected Grading Provenance-Coupling | Under the declared composition, covariance and boundedness assumptions, `F(n,t)=g n t`, `abs(g)<=1/2` | Conditional on the v10 grading extension; gain remains unselected |

v10.0 explicitly names v9.222 as the preceding stop boundary. v10.1 names v10.0, and v10.2 names v10.1. Those are direct textual links.

The later v13.26 section 1 refers to an archived protected-grading result without a filename or hash. These recovered reports directly address that construction and its premise status, but no exact v13.26-to-v10 file dependency has been established. This recovery does not certify that its author used these exact bytes, nor an archive-wide history or historical approval of the added axiom.

The verified downstream citation is exact: v15.56 `retained_amplitude.py` names v13.26 and returns `relative_retained_grade_earned: True`. FCV TYPE_LEDGER in turn cites those sources while explicitly preserving physical-realization limits.

Consequently, the safe reading is **inherited relative grading within a declared architecture**, not a proof that a protected physical source quantity or a local reader was derived from bare lineage/provenance. This qualification does not retract P0/P1 finite-additive mathematics or v13.26's retained-to-observer calibration result. FCV's general additive-monoid setting is also not restricted to the integer grading of this candidate.

## 3. One effect can suffice: conditional grade-to-record implication

This section gives the strongest elementary consequence of the recovered graded structure. It is support for the existing candidate, not a new native mechanism or a separately admitted review campaign.

Let an already justified event be represented on finite-dimensional graded objects by a trace-preserving quantum operation

    Phi(rho) = sum_j K_j rho K_j^dagger,
    sum_j K_j^dagger K_j = I,
    N_out K_j = K_j N_in  for every j.                       (3)

The last condition is the grading-intertwining condition used in v10.1, here stated for every event branch. It is a condition to establish for the actual event; no K_j is selected or implemented here. The existence of such an event between particular carriers is not proved by this conditional statement.

Suppose an input state is supported in grade n:

    rho_n = P_n^in rho_n P_n^in,  Tr(rho_n)=1,               (4)

where P_n^in is the n-eigenspace projection. For any vector v in that eigenspace,

    N_out K_j v = K_j N_in v = n K_j v.

Thus `K_j P_n^in = P_n^out K_j P_n^in`. Each positive summand in Phi(rho_n) is supported in output grade n; trace preservation gives total trace one. With `Q_out=1_(0,infinity)(N_out)`,

    Tr(Q_out Phi(rho_0)) = 0,
    Tr(Q_out Phi(rho_n)) = 1  for n>0.                       (5)

If the output is the receiver's available graded object and Q_out is an available effect, (5) is perfect empty/occupied separation. This conclusion holds for every event satisfying (3), regardless of its remaining freedom within sectors. It does not identify a computational state expectation with an actually recorded bit; physical availability of the effect is a separate condition.

The same support identity applies separately to each positive-probability selected branch: normalization of `K_j rho_n K_j^dagger` does not change its grade sector. Thus the exact conclusion does not depend on choosing a favored event outcome. Trace preservation above ensures normalization of the summed output.

For the same-total, initially blind witness, use the existing inside/outside distinction: receiver R starts in the same specified zero-grade state in both cases; in case 1 the unit source lies inside the event's source-plus-R region, and in case 0 it lies in a reference region outside it. The total protected grade of the two complete preparations is one. The region consumed into R has grade one versus zero. If (3) describes that regional event, (5) gives R occupied versus empty.

This description is conditional on an earned region/receiver association, the actual regional event, and legitimate preparations. It does not provide a tensor factorization for Genesis addresses or establish that the source region disappears physically merely because its address is pruned. The full initial available receiver state must be the same; equality of N_R alone would be insufficient if another available degree of freedom already carried the answer.

### A weaker probabilistic version

Exact preservation of every sector is stronger than needed for an informative output law. Let `sigma_b` be normalized positive output states and let an already justified output grading obey `0<=N_R<=M I`, with finite M>0. Assume only

    Tr(N_R sigma_0)=0,  Tr(N_R sigma_1)=1.                  (6)

For the integer grading, `Q_R<=N_R<=M Q_R`. Positivity therefore implies

    Tr(Q_R sigma_0)=0,
    Tr(Q_R sigma_1)>=1/M.                                  (7)

The binary outcome laws have total-variation distance at least 1/M, if that measurement is available. No probability selector is needed to calculate this bound, but neither its actual implementation nor the balance conditions in (6) are derived here. The capacity M is a declared spectral bound, not a new physical capacity rule forcing pruning. In an unbounded grading, positive finite expectation still implies nonzero occupancy probability but does not yield a uniform positive bound of this form.

For an integer M>=2 and a grading containing eigenvalues 0 and M, the formal state `(1-1/M)|0><0|+(1/M)|M><M|` has mean grade one and occupancy probability 1/M. This shows why expectation conservation alone does not imply the deterministic conclusion (5). It is an analytical control, not an assertion of native preparability.

This distinction matters to the earlier ancestry-retention result: its warning that first moments do not force the full P1 output remains correct. Equations (6)-(7) target only a binary probability contrast, which is a weaker eligible milestone consequence. They do not recover exact P1 or remove any access premise.

## 4. The correspondence still to earn

The next decisive claim must connect these specified objects and operations:

    retained source/owner object
      -> graded receiver object (H_R,N_R)
      -> actual event preserving its regional grade
      -> available occupied-sector effect Q_R.              (8)

Each arrow requires evidence independent of the desired separation. The current source-binding tuple locates a source event; it does not specify H_R, N_R, or which observations belong to R. The existing P1 map aggregates a formal measure; it is not automatically a quantum operation satisfying (3). Original v10.1 gives a conserved grading and illustrative redistribution, but does not identify that operation with a native pruning event at a Genesis address.

In particular, its beam-splitter control is a supplied operation illustrating conservation. Reusing that control would not earn (8). v10.2's response `g n t` is also not a local number-reading operation; the word access in that earlier response classification does not establish a receiver's access to (2).

The accepted occurrence premise remains a premise that an atemporal measurement/event occurs. It contains no supplied experimental apparatus, measured dataset, outcome-projector association, or proof of (8). References to it as an empirical input must not be read as independent experimental evidence for the proposed grading or event identification.

No new grading assumption is adopted by this note. The old extension is exposed so the ongoing construction can either derive the required local grading from permitted native primitives or explicitly keep that route conditional. Formal source grades and their accepted mathematical results remain available in their original scope.

## 5. Research disposition

The material advance in this pass is recovery of the earlier protected-grading reports, their explicit assumption boundary, and a concrete candidate record effect. The displayed proof gives an exact target for the actual-event correspondence; it does not close that correspondence.

Carry this source packet into the next whole-argument review if (8) is earned. Do not launch a separate numerical campaign or Gemini review merely for (5)-(7), which are elementary conditional consequences. No mathematical priority, independent acceptance, native milestone, or stage closure is claimed. No original scientific module was imported or executed. Byte counts, hashes and immutable publication checks concern evidence identity only.

The next scientific target stays one source-to-receiver transfer. It may use the occupied-sector effect without proving a full numerical P1 law, provided its state, event, access, and initial blindness are independently justified. This is the constructive use of the recovered source; protected amount by itself must not be promoted into an accessible record.
