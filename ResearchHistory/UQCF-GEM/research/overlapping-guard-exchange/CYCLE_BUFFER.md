# Breaking precedence cycles with existing root slots

Status: candidate analytical proof for independent review. Parent checkpoint: 27a05182d8fbfd621a7b571b60f6f4ff65379e95. Native admissibility and certified baseline are unchanged from SCOPE.md. No numerical execution, tests, implementation or new version is introduced.

## 1. Buffer slots are existing constraints

Keep exact-q endpoints A,C, t=q-1, actual old and destination t-guards on I,J, and K=I intersect J. Choose a set T of existing indices outside I union J. These are the proposed buffer slots; T can be empty. Slot b retains its fixed positive floor a_b. No slot or palette label is added.

We study this explicit method class. While the old guard I is fixed, replace each buffer root by a chosen support Z_b subset P with |Z_b|>=a_b, using A_b -> A_b union Z_b -> Z_b. Also prepare J minus I to its destination supports. Hold all buffers and all nonshared roots fixed during a one-pass sequential union replacement of K. Once J is complete, restore every remaining root, including the buffers, to its exact requested destination while holding J fixed.

Preparation and restoration are protected by their unchanged guards and respect each slot's floor. The only open obligation is the shared-slot stage.

Define F_0 to contain every prepared root outside K union T: C_i on J minus I and A_i on every other such slot. Crucially, F_0 omits ALL proposed buffer roots, even their original supports. For every H subset P of size at most t-1 hitting F_0, set

    L(H)={i in K: H misses A_i},
    R(H)={i in K: H misses C_i}.

Both are nonempty because F_0 includes the old and destination exclusive guard roots. Let Q be the family of these H for which L(H) and R(H) are disjoint. Common-miss sets are already protected throughout any shared-root replacement and need no buffer or ordering obligation.

Using only the obstructions that hit the OLD buffer roots would be unsound: changing those roots can release a previously excluded small transversal. Quantification over F_0 covers all possible newly exposed sets before selecting any Z_b.

## 2. Exact label capacity for an assigned protective role

Assign a subfamily Q_b of Q to each buffer b, with the Q_b pairwise disjoint as families of obstructions. Some obstructions may remain unassigned. Put

    W_b = P minus union_{H in Q_b} H.

An empty Q_b gives W_b=P.

**Lemma B1.** A floor-safe buffer support that is missed by every assigned H exists exactly when |W_b|>=a_b.

Indeed H misses Z_b for every H in Q_b exactly when Z_b is contained in W_b. This allows a support of size at least a_b precisely under the stated inequality. One may choose exactly a_b labels. Different buffers may use overlapping supports; the native carrier imposes no label exclusivity across slots.

This is usable protection capacity at a specific slot for a specified family of obstructions. It is not implied by total complementary capacity or by a degree-slack count. It adds no admissibility restriction: failure means this particular buffer assignment cannot be used.

## 3. Necessary-and-sufficient certificate for the buffered method

For every unassigned H in Q, choose j(H) in R(H), i(H) in L(H) and draw the edge j(H)->i(H) on K.

**Theorem B2.** A lower-guard path in the method class of Section 1 exists if and only if there is an assignment of obstructions to buffer slots such that:

1. |W_b|>=a_b for every buffer b;
2. witness edges for all unassigned obstructions can be chosen to form an acyclic directed graph.

The equivalence fixes A,C,I,J,T and the preparation of nonbuffer roots. It concerns choices of buffer supports and a one-pass shared-root order within this method class. It is not an equivalence with arbitrary root connectivity.

Sufficiency: choose Z_b subset W_b of size a_b and install it under the old guard. During the shared stage, each assigned H misses its fixed buffer root. Every H with a common missed shared index was already excluded from Q and remains protected by that index. For H in Q left unassigned, a topological order of the witness graph satisfies the exact ordering criterion S2 of SEQUENTIAL_HANDOVER.md. A small H missing F_0 cannot hit the full tuple. These cases exhaust every set of at most t-1 labels, so the lower guard holds throughout.

Necessity: suppose some permitted buffer supports and a shared-slot order give a safe path of the stated form. For each H in Q that misses at least one Z_b, assign H to one such b. Its buffer support lies in W_b, so |W_b|>=|Z_b|>=a_b. Every remaining H hits all buffers as well as F_0. The exact S2 criterion therefore requires a new missed index before a last old missed index. Choose such a forward witness edge for each. All edges increase position in the safe order and hence are acyclic. This constructs the required certificate.

An H may incidentally miss an installed buffer even if not assigned to it; that only adds protection. Assignment disjointness loses nothing, because one missed root suffices for that H. For T empty, B2 reduces to S3. For K empty, Q is empty and guard preparation already suffices.

## 4. Eligible moves, renewal and endpoint restoration

The capacity inequalities prove that each buffer support can actually be selected. Every preparation edit has the old guard unchanged. A finite acyclic graph always has a zero-indegree vertex until exhausted; choose one and complete its finite union replacement. S2 and the fixed buffers prove eligibility of all its incidence changes. The number of remaining shared slots decreases. Afterward J is complete and protects every finite restoration edit, including removal of the buffers' temporary protective supports.

Thus protection is renewed in three explicit stages: old guard during installation, buffers plus ordered old/new missed-root witnesses during exchange, and destination guard during restoration. No second unit of deficit is charged for installing or removing a buffer, because each such step already has an unchanged t-guard. Intermediate tuples need not be exact-q.

This gives a finite path with tau>=q-1 between the original exact-q endpoints. The accepted maximum-layer-removal theorem supplies a path with tau in {q-1,q}. The normalized path need not retain the simple buffer schedule; no path-length efficiency is claimed. Native lifting remains conditional on the accepted child interfaces and fixed-root clearance, exactly as in GUARD_HANDOVER.md Section 6.

## 5. A sufficient way to break a selected cycle system

Choose one witness edge for every H in Q. Remove a collection of OBSTRUCTION RECORDS whose remaining witness edges are acyclic. Assign the removed obstructions to existing buffers with the B1 capacity inequalities. B2 then supplies a repair, even if the original selected graph had cycles. If several obstructions supplied the same directed edge, removing one record does not remove that edge while another unassigned record still supplies it.

This is a sufficient certificate, not a minimum-buffer algorithm. An arbitrary cyclic witness selection need not be unavoidable; another selection can be acyclic without buffers. Conversely, failure of one assignment or feedback choice does not prove that every buffered certificate fails.

## 6. Remaining boundary

B2 resolves forced precedence cycles whenever suitable existing outside-guard slots and obstruction-avoiding supports can be exhibited. CYCLE_BUFFER_EXAMPLE.md supplies an all-floor-h compact family, h>=3, with k<sum_i a_i, where the unbuffered schedule is impossible but one existing buffer resolves it.

The general theorem remains open when no such outside-guard slots exist, when the assigned obstructions exhaust too much of the palette for the available floors, or when no acyclic residual choice is established. Those are gaps in this method, not proved root disconnections or native barriers. Exact-endpoint capacity inequalities do not yet guarantee a buffered certificate. No universal existence, originality, implementation certification, efficiency or physical claim is made.
