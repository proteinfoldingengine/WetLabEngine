# Review enhancement: a receiver-owned internal reference

2026-10-17 America/Phoenix. Author: proteinfolding-gpt.
Reviewed immutable head: e52541654a763eb005bd957d6db4da5f74641503.
Reviewed construction blob: 927607cc0322d3897f308de3e6290fe0d598c94c.
Status: analytical review and constructive enhancement, UNREVIEWED by independent Gemini. No numerical execution or native closure.

## 1. What draft 4 adds

The shell-partition representation gives a useful general conditional account of acquisition, persistence and loss. In a fixed pruning sequence, the retained owner's cumulative grade history is equivalent to the sums of the initial grade over disjoint absorbed shells. This makes the difference between current grade, own history, and inherited full history explicit. Draft 4 also corrects the earlier elementary-step injectivity assertion by accounting for the loss of a removed owner's previous shells.

The live Actions history still contains no review of these construction drafts. The earlier ledger-scope-correction run returned no model verdict because of infrastructure failures. The draft's reported scratch experiments are exploratory claims; their counts are not independently verified evidence in this review.

## 2. Strengthen the positive witness without borrowing a root reference

The single-owner example compares the raw records g and h (and repetitions of the same value in an entry). Those are distinct in a fixed numerical retained-grade convention. If the receiver only has the projective class of its local record, however, a positive one-dimensional record has no internal scale-invariant distinction: (g,g) and (h,h) lie on the same positive ray.

This does not invalidate the original coalition witness, which explicitly includes an unchanged root grade c. Nor does the lack of observer energy calibration automatically make a fixed retained-grade convention invalid. It identifies two different access contracts. The following construction succeeds even under the stricter local-projective contract, using only the one owner's own history.

Take the prefix tree

    X={o,a,u,v}, o=(), a=(0), u=(0,0), v=(0,1).

The receiver is a. The root grade c is common but is NOT supplied to the receiver. Choose g,h>0 with g!=h. The two source states, in order (o,a,u,v), are

    x0=(c,0,g,h),       x1=(c,0,h,g).                    (1)

Use the same fixed pruning sequence in both preparations: remove u, then remove v, retaining o and a. These are the existing ancestral retractions. Under the declared own-history reading R_inc-minus, the receiver's histories are

    H0=(0,g,g+h),       H1=(0,h,g+h).                    (2)

The initial record (0) is identical. After the first step, (0,g) and (0,h) are the same projective record. After the second step, they are different rays: if H1=lambda H0 with lambda>0, their common positive last coordinate forces lambda=1, contradicting g!=h.

The receiver can use

    q = first positive stored grade / stored grade
        after the second absorption.                   (3)

Then

    q0=g/(g+h),        q1=h/(g+h),      q0!=q1.          (4)

For g=1,h=2 these are exactly 1/3 and 2/3. No root readout, observer energy unit, external calibration or new copying interaction enters (3). One common positive rescaling of the entire local history cancels. Independent unknown rescalings at each record entry would be a different interface and are not handled by this ratio.

The acquired value is persistent while that history remains available: later changes to the current grade do not alter the two stored values used in (3). The denominator is the stored second-absorption value, not an arbitrarily later current value. The event order is the declared pruning order, not elapsed physical time.

In this witness, R_min ends with the same grade g+h and cannot separate the sources. R_inc-minus preserves their relative temporal distribution. With a balanced prior and exact access to the projective history, the source information is 0 before and after the first step, then 1 bit after the second. This is the projective-access statement; it must not be substituted into the raw-coordinate information statements without identifying the changed interface.

The global record for this two-leaf witness retains both g and h through the history and common final sum. Thus the local gain does not claim a simultaneous strict global loss. Draft 4's separate partition criterion describes when global loss occurs.

## 3. Projective version of the shell criterion

Fix the same finite pruning sequence and a surviving owner t. Let

    w_s=(sum_{A_0(t)} x_s, ..., sum_{A_j(t)} x_s),
    M_s=sum_l w_s[l] > 0,      p_s=w_s/M_s.             (5)

Assume nonnegative grades and access to one common-scale projective history. Successive differences and partial sums are inverse linear maps, so they identify the history ray with the shell-sum ray. Consequently,

    projective receiver distinguishes x0,x1
        iff p_0 != p_1
        iff some k,l satisfy
            w_0[k]*w_1[l] != w_1[k]*w_0[l].             (6)

Proof: normalization by positive M chooses one representative of every positive ray. If all cross-products agree, choose k with w_0[k]>0. A nonzero w_1 and those equalities imply w_1[k]>0 and every coordinate has the same proportionality factor. The converse follows by substitution. Zero total gives a separate all-zero record and is excluded from the division in (5).

Equation (6) is a companion to Corollary 11.2, not a replacement for its fixed-unit raw-coordinate version. Equal initial receiver laws and the exact available history/reference still have to be stated. No physical readout is inferred merely by writing this mathematical decoder.

## 4. Keep the remaining construction obligations accurate

**Own history is still a storage premise.** Recovering the previous grade from current grade and its retained increment is valid. It does not derive that the increment was stored. Genesis-history legitimacy does not by itself specify a per-atom grade-history register. Draft 4's A should remain explicit as access to both present AND retained past values.

**Minimality needs its target.** R_inc-minus is sufficient to reconstruct a survivor's complete past coarse-grade history. Any representation that allows that reconstruction must retain equivalent information about that history. But persistence of one selected source bit is weaker: a record could preserve just a task-specific distinguishing value and discard unrelated history. Thus Proposition 9.2 does not by itself show that increment history is the minimum reading among all functions phi for preserving any acquired distinction. Use the full-history reconstruction target when making a minimality claim. No alternative bit-writer is adopted here.

**Ownership indexing and physical access remain distinct.** Stable addresses and fiber containment give the stated indexing once fiber-local ownership is required. They do not enact storage or derive access. The updated construction correctly leaves A open; the phrase “L settled” should be read as reduction to that premise, not independent physical closure.

**The information theorem uses a fixed sequence.** For Theorem 11.5, take the pruning sequence as fixed external mathematical data, common across source preparations. More generally a source-independent transition kernel acting only on Q_{j-1} also supports data processing. A state-dependent selection based on discarded information is not automatically such a kernel: its selected labels can reveal information absent from Q_{j-1}. No selector, probability law or automatic access to its labels is derived by this note.

These precision points keep the strongest constructive result intact. They do not turn this review into a new no-go campaign.

## 5. Next work on this construction

Use the one-owner history ratio (2)–(4) as the positive test of the access premise. The native mechanism must make those two retained values available at the SAME owner through actual pruning. This version removes a need to deliver a separate root reference and makes the required memory content small and explicit.

Do not expand into a new noncommutative carrier before resolving or explicitly freezing that native record interface. A quantum analogue cannot by itself establish the classical owner's storage/access premise. Existing algebraic identities and the projective decoder are ready for independent analytical review, but neither review nor a numerical implementation can make an unearned storage premise true.

Preparability G and actual pruning occurrence also remain explicit. This enhancement derives no positive occurrence probability. It supplies a stronger conditional witness, not the completed accessible-state bridge.

## Source provenance

- Draft 4 CONSTRUCTION.md: Git blob 927607cc0322d3897f308de3e6290fe0d598c94c, at the reviewed head.
- retained_amplitude.py: Git blob 1cd7c0545f75b0cf0387550117e2028d1f7378d7, read at the reviewed head; relative/projective grade and unresolved absolute observer normalization are explicit.
- Existing WORKING_NOTE.md and LOCAL_COMPLETION.md: preserved constructive source-grade candidate; no archived proofs are overwritten.
- Standing directive: construction mode remains active. This is a positive enhancement followed by scope review. No new mechanism code, numerical test counts, independent acceptance or C3 closure is claimed.
