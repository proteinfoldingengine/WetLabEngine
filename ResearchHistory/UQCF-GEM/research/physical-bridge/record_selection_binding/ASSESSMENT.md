# Does the existing actual-record operation implement the P1 benchmark?

Author analytical source screen, November 20, 2026 America/Phoenix. This tests one concrete event identification in the current encoding. The algebra below was worked out before the proposed finite replay. Native event correspondence and owner access remain open.

## Inspected operations

The original v15.11 routine supplies two operations. The nonselective operation pinch sums $P_i\rho P_i$ over a supplied complete orthogonal resolution. The selected operation select_record first performs that pinching, then projects onto the explicitly supplied record and normalizes by its positive weight. A missing record or a zero-weight selected outcome raises an error. Its report expressly leaves actual record selection supplied. [Original implementation](https://github.com/proteinfoldingengine/WetLabEngine/blob/e7e01bab68ba5171dacd91333f98d208d810dac3/ResearchHistory/UQCF-GEM/v15/v15.11/ontology_continuity_audit.py) · [Ontology report](https://github.com/proteinfoldingengine/WetLabEngine/blob/e7e01bab68ba5171dacd91333f98d208d810dac3/ResearchHistory/UQCF-GEM/v15/v15.11/REPORT.md)

The source benchmark uses the ordered basis $(o,p,u,v)$, $Q=I-\pi_u$, and
$$C(\rho)=Q\rho Q+\rho_{uu}\pi_p.$$
Its correspondence with physical P1 remains supplied. Use the existing normalized pair with diagonals $(1,1,2,1)/5$ and $(1,1,1,2)/5$. The candidate identification here keeps this basis and source encoding, uses the existing projectors $(Q,\pi_u)$, and selects record zero. The choice of this record/projector identification is an explicit test hypothesis, with the same choice in both preparations. [Benchmark](../p1_receiver_location_resolution/RESULT.md)

## Selected retained record

Write $q=\operatorname{Tr}(Q\rho)>0$ and $\tau=Q\rho Q$. The actual source routine gives
$$S_Q(\rho)=\tau/q.$$
For $q<1$, equality with $C$ is equivalent to
$$\tau/q=\tau+(1-q)\pi_p
\quad\Longleftrightarrow\quad \tau=q\pi_p.$$
For $q=1$ equality always holds. For $q=0$ the selected operation is undefined, while $C$ is defined. Thus in this same-code test the selected retained record implements $C$ only when there is no removed population or when the normalized retained state is already entirely at the parent. This proof allows arbitrary valid coherences. Neither condition holds for either canonical preparation.

The expected full diagonal outputs, in $(o,p,u,v)$ order, are

| Input | Selected retained record | P1 benchmark |
|---|---|---|
| $(1,1,2,1)/5$ | $(1/3,1/3,0,1/3)$ | $(1/5,3/5,0,1/5)$ |
| $(1,1,1,2)/5$ | $(1/4,1/4,0,1/2)$ | $(1/5,2/5,0,2/5)$ |

The parent-effect probability difference is $1/12$ for the selected operation and $1/5$ for the benchmark. The record probabilities before conditioning are $3/5$ and $4/5$. These probabilities belong to the supplied quantum representation. The comparison does not identify them as new native outcome probabilities.

## Nonselective operation

The same supplied resolution gives
$$E(\rho)=Q\rho Q+\pi_u\rho\pi_u.$$
It leaves both diagonal input states unchanged. The parent effect therefore has zero contrast on this pair, since both parent populations initially equal $1/5$.

More generally every nonselective pinch implemented by this routine is unital on the same full matrix space because its projectors resolve the identity. The benchmark instead has $C(I)=Q+\pi_p$, which differs from $I$. Therefore choosing another complete orthogonal resolution inside this unchanged representation cannot turn this exact pinching implementation into $C$ on all inputs. This does not classify instruments with feedback, output re-encoding, different input/output spaces, nonprojective operations or other physical event classes.

## Relation to the existing measurement compatibility result

The earlier measurement-first proof establishes that conditioning on a union of full ancestral fibers commutes with pushforward. It compares two compositions. It does not equate the conditioning operation itself with the pushforward. Here the retained subset $Y$ omits $u$ while retaining $p$, so its indicator cuts the pruning fiber $\{p,u\}$. That compatibility criterion does not supply this candidate identification either. [Existing compatibility equations (2)–(4)](../measurement_first_review/RESULT.md)

The event-binding question has a concrete source-level answer for this candidate. The inspected actual-record routine cannot be substituted for the supplied benchmark on the current pair. A different event correspondence would require its own producing operation and source-supported representation. An actual event may have an unconditioned source channel together with a separately selected record, but that is a joint-instrument identification and is not supplied by equating the two functions tested here. Actual occurrence remains accepted input. Physical ownership and readout availability remain separate obligations.

## Prospective bounded check

Import the original source unchanged after checking Git blob 8871e50f19322adbb62f34ea3837ba8e6cb16c8b. Invoke its actual pinch and select_record entry points with the declared resolution and record. Compare all four diagonal coordinates against independent Fraction arithmetic for the two canonical inputs and two equality controls, $(1/5,3/10,0,1/2)$ and $(0,2/5,3/5,0)$. Verify the zero-record-weight rejection on $\pi_u$ and the explicit-record requirement. Check unitality on $I$ and the benchmark's unequal image. Use absolute numerical tolerance $10^{-14}$ for the original NumPy outputs, and exact arithmetic for all expected probabilities.

The check is a local source replay of these cases, with no archival campaign or complete foundational-stack replay claimed. This candidate fails admission as a new physical P1 producer, so the disposition is a bounded analytical rejection of this identification. An independent scientific acceptance, new Gemini review, stage certification, new physical law or gravity signal is not claimed.
