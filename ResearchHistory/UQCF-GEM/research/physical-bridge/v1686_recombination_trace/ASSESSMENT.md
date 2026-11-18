# Does the V1686 recombination rule deliver an extensive grade?

**Finding.** The archived V1686.35 operation can move a source contrast into a preselected neighboring cell and use the resulting field in another recombination. The same operation can produce the same destination contrast while preserving the source contrast as well. An exact source debit distinguishes these cases. The returned field belongs to a newly constructed composite in the program. A physical owner's access to that field remains open.

## Source and question

At research parent `e7e01bab68ba5171dacd91333f98d208d810dac3`, inspect [the V1686.35 program](../../../../../Tmp/TOE/Einstein%209_v1686_l3_geometry_plus_information/v1686_35_forced_hd_export_fix_colab.py), Git blob `b780961cebf14a5bff0153d109e2855c878090ec`. Lines 107–128 define the two input/output state types. Lines 234–289 define the gate, kernel, output construction and a caller that consumes it. Lines 335–355 use the resulting fields for diagnostics. The comparison is with [the inherited P1 fiber sum](../../../foundational-closure-verification/PROOFS.md), §§P0–P1, and [the receiver-location benchmark](../p1_receiver_location_resolution/RESULT.md), §§2–4. The matrix and lattice coordinates in those two constructions have different types.

T-301 and T-399 concern a related formula with the same roll direction on both arguments. V1686.35 rolls its first field forward and its second backward, averages the two lattice axes, then multiplies by a **pointwise** gate. These are substantive differences. This trace does not reopen the settled linear endomorphism classification or identify either operator with every version of the retained connection.

## What the code produces

Let $a,b$ be the two real periodic array fields and $D$ the two positive coordinate directions. Put $h_i=\min(|a_i|,|b_i|)/(1+\min(|a_i|,|b_i|))$. The scalar $s$ is the product of the program's harmonic closure weight and retained-order sign. With $F_{i,d}=a_i b_{i+d}/2$, direct expansion of lines 250–253 and 269–284 gives

$$
 z_i=a_i+b_i+s h_i\sum_{d\in D}(F_{i-d,d}-F_{i,d}).
$$

Summing over the periodic array and shifting each incoming term one lattice step gives

$$
 \sum_i (z_i-a_i-b_i)=s\sum_{i,d}(h_{i+d}-h_i) F_{i,d}.
$$

A single directed term thus adds $s h_{i+d}F_{i,d}$ at its destination and subtracts $s h_i F_{i,d}$ at its origin. Equal endpoint gates balance that term. Total balance can also arise by cancellation across edges. If either input field vanishes at a cell, its own gate vanishes and its correction there is zero.

## A fixed receiving cell and two controls

Use a periodic $5\times5$ array with $u=(2,1)$, $r=(2,2)$, $v=(0,0)$ and $w=(4,4)$ in zero-based indices. Write $e_i$ for a unit field. Use unit closure weights and input order signatures $(1),(2)$, giving $s=1$. Compare

$$
 a^+=e_r+e_u,\qquad a^-=e_r+e_v,\qquad
 b=\beta e_r+\eta e_u+(1-\eta)e_w.
$$

Here $\beta\in\{1,4\}$ and $\eta\in\{0,1\}$. Each comparison keeps $b$, the entire nominated input branch B and both branch identities fixed. Both preparations have $a_r=1$, $b_r=\beta$, and equal initial totals. Relocating one unit of B between $u$ and the inert $w$ keeps its total fixed between controls.

The minus preparation has zero correction. In the plus preparation the contribution from $u$ to $r$ has $F=\beta/2$, $h_r=1/2$, $h_u=\eta/2$. Other edges give zero correction. Therefore the full array contrast is

$$
 z^+-z^-=e_u-e_v+\tfrac{\beta}{4}(e_r-\eta e_u).
$$

| Destination scale | Gate at source in plus preparation | Output contrast at source $u$ | At destination $r$ | Change in total between preparations |
|---|---|---:|---:|---:|
| $\beta=1$ | Open ($\eta=1$) | $3/4$ | $1/4$ | $0$ |
| $\beta=1$ | Closed ($\eta=0$) | $1$ | $1/4$ | $1/4$ |
| $\beta=4$ | Open ($\eta=1$) | $0$ | $1$ | $0$ |
| $\beta=4$ | Closed ($\eta=0$) | $1$ | $1$ | $1$ |

In all rows the contrast at $v$ is $-1$ and all other cells have zero contrast. At $\beta=4,\eta=1$ the **whole contrast** matches the lifted P1 action that removes $u$ into $r$ while retaining $v$. The input and output arrays still occupy the same grid, and common background at $u$ remains. This is one match on a chosen pair. Changing just the location of B's auxiliary unit produces the same reading at $r$ with a different total. Even the unit-valued destination reading cannot by itself distinguish transfer from duplication in this executable.

## Ownership and scientific scope

The supported public entry point takes two branch objects. Line 277 creates a fresh `RecombinedState`. Its vector and concatenated input provenance go to the next call at lines 286–289. Input B is fixed in each preparation pair and gets no write. The composite field contains a real, model-internal difference at a coordinate fixed before comparison. Its source tuple identifies both participating inputs globally. The program provides no lineage map from the chosen lattice cell to P1's retained parent and no operation assigning that cell's value to B's own available record.

**Premise ledger.** INHERITED within the archived simulation are the opposite rolls, pointwise gates, output type, and subsequent use. INHERITED within the P1 type are the ancestral retraction and finite-additive pushforward. ACCEPTED INPUT is atemporal pruning occurrence. SUPPLIED for this analytical test are the array preparations, chosen cell and comparison with a hypothetical P1 parent. Physical preparability, event identification and an owned available effect remain open. No fundamental clock is used.

For a designated proper receiver the array calculation imposes no joint constraint that distinguishes the established receiver-writing, environment-writing or correlation-only implementations. For the retained-source reading, the unit-contrast row is a model witness. Its availability to the nominated owner has not been derived. No physical signal, curvature law or gravitational force is inferred.

The next source would have to bind the output of this actual operation to the surviving owner's state or a native use at that owner. A new fit, a new choice of gate, or repetition of the destination reading does not address that question.
