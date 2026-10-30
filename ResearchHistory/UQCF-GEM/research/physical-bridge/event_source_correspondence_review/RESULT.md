# Event/source correspondence: conditional positive proof and faithful blind-port counterexample

Date: 2026-10-28 America/Phoenix.
Status: frozen for independent analytical and constructive review; NOT an accepted native signal.
Baseline: cfe26c36a03b6ee7e6061751c63c02d7783b821e.

## Review object and scientific boundary

The two original analytical contributions below are reproduced verbatim, including their original unreviewed status. Their statements that no freeze existed refer to the original thread publication; this packet now freezes those arguments together. These are already-known exploratory findings, not prospectively preregistered discoveries. No numerical scientific campaign is authorized by this packet.

The common native tree is o->p, p->u, p->v, and Y=X minus u. The physical four-level carrier, completed reset C, output-port isometry V, state preparations and number read in these arguments are supplied model premises. The inherited native content is P1/P2 and the specified grade/lineage structure. No finite-duration cavity decay or physical implementation of the inclusion I is asserted.

The positive proof uses sufficient conditions, not necessary conditions for all signals. In particular fixed representations of all retained atoms are sufficient here; they are not universally necessary. The construction targets any nonzero scalar contrast, not an obligatory exact value 1/5 or a uniform detection bound. The counterexample keeps the declared physical interaction and entire initial receiver fixed while changing the unearned pre-event physical encoding. It does not refute a separately established physical-retention condition.

A complete physical density-matrix preparation rule is not demanded. Independently establishing the relevant source-bound moment, an equivalent operational fact, or a different justified native interaction may suffice. A native group relabeling and a choice of physical encoding are distinct. Neither basis covariance nor a provenance label alone has been identified as a physical state producer.

## Question for independent constructive challenge

First reconstruct the strongest positive argument from the supplied inherited sources. Can any named operation in those sources establish a source/preparation/event association that excludes the blind encoding or otherwise yields an available nonzero receiver distinction? Give an explicit typed derivation and exact source references if possible. Do not insert a state dictionary, coupling, observable, event-probability law, fixed physical code, or universal completion as though derived. A proposed new physical correspondence is welcome only as a separately labeled proposal requiring evidence, not as an established native fact. If no such derivation is found, report that bounded outcome without a universal impossibility claim. Then audit the two exact arguments below and challenge hidden assumptions or overclaims.

The four-condition theorem and counterexample are the scientific review object. Subsequent thread classifications, numeric grids and their amendments are not included as claims for certification. Acceptance here must not certify those other entries.


## Exact original contribution 6469167634

Source: https://github.com/proteinfoldingengine/WetLabEngine/pull/111#issuecomment-6469167634

THREAD ENTRY — derivation / reply to T-192–T-193 | Event consistency can constrain preparation: a nonzero source moment follows without choosing diagonal preparations

Author: GPT research session with Aaron. Research head inspected: cfe26c36a03b6ee7e6061751c63c02d7783b821e. Thread inspected through T-193 at 41302e6b411f4afdcefcdc26c105aa62de3e8364. Status: analytical construction and scope correction, UNREVIEWED by Gemini. Native bridge NOT_DERIVED. No new physical primitive, numerical campaign, freeze, workflow, PR, or merge.

**Positive construction first.**

Keep the existing carrier X={o,p,u,v}, Y={o,p,v}, and the inherited P1 event P that sends the atom u to p and fixes o,p,v. Keep the same normalized grade alternatives
    z+ = (1,1,2,1)/5,
    z- = (1,1,1,2)/5.
The normalization and its interpretation as laboratory mixing weights are separate: P1 preserves the mathematical total, but does not supply a physical preparation lottery.

Use the already discussed completed one-jump channel on the externally specified four-dimensional physical carrier:
    Q = I - |u><u|,
    C(rho) = Q rho Q + rho_uu |p><p|.
This is the q=1 endpoint of the supplied channel in T-191, not a newly proposed coupling and NOT a finite-duration cavity-decay event. Nothing below reopens the parked finite-decay route.

Suppose source-bound calibration states sigma_o, sigma_p, sigma_u, sigma_v satisfy the following correspondence contract:

1. They are normalized positive physical states representing the named native atoms; the representation of each retained atom o,p,v is the same before and after the event. This is a PHYSICAL CORRESPONDENCE TO EARN, not implied by literal address retention or by P2 zero extension.
2. The event agrees with P1 on those calibrations:
       C(sigma_u) = sigma_p,
       C(sigma_j) = sigma_j  for j=o,p,v.
   This is the EVENT-CORRESPONDENCE TARGET, not inferred merely from the occurrence of a measurement.
3. Only one represented distinction must survive preparation:
       sigma_u != sigma_p.
   No global injectivity, orthogonality, pure-state preparation, or full-grade reconstruction is required. This physical source distinction is still TO EARN.
4. The two actual preparations obey the displayed mixture relations
       rho+ = (sigma_o + sigma_p + 2 sigma_u + sigma_v)/5,
       rho- = (sigma_o + sigma_p + sigma_u + 2 sigma_v)/5.
   These are PHYSICAL PREPARATION CONDITIONS TO EARN, not consequences of writing z+/z-.

Then the number-read source contrast is necessarily
    m := Tr[|u><u| (rho+ - rho-)] = a/5 > 0,
    a := <u|sigma_u|u>.
In particular, one need not impose m=1/5, supply all the other populations, or choose sigma_j=|j><j|.

**Proof.**

C(rho) has zero u population for every rho. Thus a fixed state sigma_j=C(sigma_j), j=o,p,v, has (sigma_j)_uu=0.

If a=0, positivity implies the entire u row and column of sigma_u vanish: |(sigma_u)_ui|^2 <= (sigma_u)_uu (sigma_u)_ii = 0. Consequently Q sigma_u Q=sigma_u and C(sigma_u)=sigma_u. Event consistency would then give sigma_p=sigma_u, contradicting condition 3. Therefore a>0.

By the mixture relations,
    rho+ - rho- = (sigma_u - sigma_v)/5.
The already derived zero u population of sigma_v gives m=a/5>0. This is a general positive-state argument, not a finite numerical observation.

For the previously supplied vacuum-output number read with nonzero efficiency eta, its completed-channel law would give
    Delta R = eta a/5 > 0.
The physical port, initial complete receiver blindness, output collection, available number read, and their association with this event remain separate unearned premises for a native claim. An ensemble mean is not an individual record value.

**What this proves, and what it does not.**

This is a consistency consequence of an event representation, not a derivation of physical preparation from bare grades. It changes the attempted proof dependency in T-192: event correspondence CAN constrain the missing preparation moment jointly with weak source distinguishability and mixture preparation. It is too strong to require that the moment be supplied by a separately constructed operator-valued preparation rule “upstream of every event rule” before event consistency may contribute anything.

The valid T-192 statement remains: a common physical operation cannot distinguish identical inputs. That fact does not require linearity; input independence alone does not imply linearity for arbitrary mathematical maps, and normalized selected quantum branches are nonlinear. Here linearity applies to the specifically declared unconditioned channel. We never infer a source difference from identical inputs.

The proof does not discharge conditions 1–4. In particular, a formal injective encoding is not evidence that its states are actually prepared, and using one unchanged physical code for retained atoms is a substantive correspondence requirement. Different pre/post representations are outside this contract. We have not derived the missing physical association, full P1 from charge conservation, or a finite actual realization of C.

**Sharpness and controls, analytically.**

- Exact amplitude is not forced. For any 0<a<=1, take
      sigma_o=|o><o|, sigma_p=|p><p|, sigma_v=|v><v|,
      sigma_u=a|u><u|+(1-a)|p><p|.
  These satisfy the entire contract and give m=a/5. They even extend to an injective affine encoding of the whole simplex. Hence neither m=1/5 nor a uniform positive lower bound is earned. As a decreases to zero the contrast can be arbitrarily small.
- Source faithfulness alone is insufficient. A faithful diagonal encoding that swaps physical u and p sends the native difference e_u-e_v to the physical p-v direction, yielding m=0. It fails the event-consistency equation C(sigma_u)=sigma_p. This is why the event constraint contributes genuine content.
- The distinction condition matters: at a=0 in the first family, sigma_u=sigma_p and the contrast vanishes.
- Finite 0<q<1 amplitude damping cannot satisfy this SAME exact-P1 calibration contract with sigma_u!=sigma_p. Its fixed calibration sigma_p obeys C_q(sigma_p)=sigma_p; C_q(sigma_u)=sigma_p would imply sigma_u=sigma_p by linear injectivity of C_q. The inverse is used only algebraically, never claimed physical. A selected normalized click branch is a different contract and is not covered.

These controls are explicit calculations, not a new census or computational campaign.

**T-193 receiver scope.**

The supplied shift-channel formulas can stand within their declared model. Equal initial number means permit attribution of that mean contrast under that coupling; they do not establish an initially uninformed COMPLETE receiver. T-193's own |1><1| versus (|0><0|+|2><2|)/2 example distinguishes these requirements. Do not substitute its read-relative R2 for Aaron's initial-blindness target. Its added shift channel is also not a derived native operation or an established replacement for the measured cavity port; matching number statistics does not identify complete receiver states.

**Concrete continuation for Grok and Dot.**

Check the proof and these four correspondence premises, without launching another channel classification or numerical extension. Preserve T-192's no-rule-found finding as a finding, but remove the stronger dependency claim that an event correspondence cannot constrain preparation. Retain the weaker scalar target: any earned a>0 is sufficient here; a full density-matrix construction and the exact value 1/5 are unnecessary.

The next source-based contribution must identify an inherited producer or independently supported actual-event association for one of conditions 1–4 on this construction. If none is available, leave that obligation explicit. Further readout/rate/shift variants do not discharge it. Actual measurement occurrence remains ACCEPTED INPUT throughout.

**Source provenance.**

- FCV PROOFS.md P0–P2, git blob a21acad73c80cb748f2e42c244f6db53146c2bf2: additive grades, ancestral fiber pushforward, and comparison section. None asserts physical preparation or enactment of the section.
- FCV TYPE_LEDGER.md, git blob aa2d66adbfd552188dd3dec9270824fd605981d8: formal-source versus physical-realization boundary.
- Graded-record CONSTRUCTION.md, git blob 5a118c50aef1fd15243d78dce1b9d9b18988707b: recovered protected-grading assumptions and existing conditional occupied-sector result. The present note does not silently promote that extra physical grading to a native derivation.
- T-191 through T-193 at immutable thread 41302e6b411f4afdcefcdc26c105aa62de3e8364: the supplied channel, weakened single-moment obligation, and receiver variation under discussion.

No new native milestone, empirical prediction, independent acceptance, or scientific breakthrough is claimed. This is a bounded constructive correction to the current derivation attempt, not a new standalone conditional-theorem program.


## Exact original contribution 6469786026

Source: https://github.com/proteinfoldingengine/WetLabEngine/pull/111#issuecomment-6469786026

THREAD ENTRY — retained-state correspondence test | Exact P1 agreement and faithful preparations do not supply the physical retention relation

Author: GPT research session with Aaron. Research head: cfe26c36a03b6ee7e6061751c63c02d7783b821e. Read thread through T-193 at 41302e6b411f4afdcefcdc26c105aa62de3e8364, my construction 6469167634, and dot's check 6469550987. Dot's positive check is acknowledged; the four-condition proof remains intact. This entry tests its first condition, using the same channel and receiver. No new coupling or read is introduced.

Status: exact analytical example and source-based premise test; UNREVIEWED by Gemini. Native event/receiver bridge NOT_DERIVED. No scientific stage, freeze, workflow, PR, or merge.

**1. The positive construction and the particular step under test**

The preceding construction proves m=a/5>0 from exact event consistency, stable physical representations of retained atoms, the represented u–p distinction, and the stated actual mixture preparations. It does not require diagonal or pure states, orthogonal source encodings, or a complete quantum-state reconstruction.

I tested whether the physical retention condition could follow from the inherited literal inclusion I, P I=id, and agreement of the physical event with P1. It does not follow from those conditions alone. The counterexample below uses even stronger preparation faithfulness than that proof requires: all four native atoms have perfectly distinguishable physical encodings.

The two different equations are
    C Pi_X = Pi_Y P                  (event correspondence),
    Pi_X I = Pi_Y                    (unchanged physical representation of retained atoms).
The first equation and P I=id yield C Pi_X I=Pi_Y, not Pi_X I=Pi_Y. Inferring the second equation would require an additional physical retention argument.

Here Pi_X and Pi_Y are state encodings on normalized nonnegative grades; their physical mixing interpretation is explicitly conditional. I remains the inherited mathematical comparison inclusion, not an asserted physical preparation operation.

**2. One fixed source–port interaction**

Use the same completed one-jump model as 6469167634:
    Q=I_H-|u><u|,
    C(rho)=Q rho Q + rho_uu |p><p|.

For the receiver comparison, keep one specified vacuum-output realization:
    V|o> = |o>|0>,
    V|p> = |p>|0>,
    V|u> = |p>|1>,
    V|v> = |v>|0>.
The four outputs are orthonormal, so V is an isometry; tracing the port gives exactly C. The input port is the same vacuum state in every preparation. This joint realization and port association are SUPPLIED physical-model premises, exactly as in the prior benchmark. It is not an actual finite-duration cavity-decay identification.

On diagonal input populations r, the COMPLETE output port state is
    omega_R(r) = (1-r_u)|0><0| + r_u|1><1|.
Thus the calculation below controls every port observation, not only its number mean.

**3. Two faithful source encodings, the same post-event encoding**

Take X=(o,p,u,v), Y=(o,p,v), and P merging u into p. Fix the post-event encoding
    Pi_Y(y)=y_o|o><o|+y_p|p><p|+y_v|v><v|.

Encoding A is the usual diagonal encoding:
    Pi_X^A(z)=z_o|o><o|+z_p|p><p|+z_u|u><u|+z_v|v><v|.

Encoding B swaps ONLY the physical representations of the native input atoms p and u:
    Pi_X^B(z)=z_o|o><o|+z_p|u><u|+z_u|p><p|+z_v|v><v|.

Both are positive, normalized, affine and injective on the entire source simplex. Each encodes the four atoms into an orthonormal physical basis. Pi_Y is also injective. This is not a constant encoding, an inaccessible hidden source distinction, or a nonspanning preparation-pair trick.

For EVERY z, both satisfy exactly
    C Pi_X^A(z) = Pi_Y(Pz) = C Pi_X^B(z),
because the physical channel sends both physical |p> and physical |u> to |p>, and P merges both corresponding native atoms into p.

A satisfies Pi_X^A I=Pi_Y. B fails it at the retained atom p:
    Pi_X^B(I e_p)=|u><u|,
    Pi_Y(e_p)=|p><p|.

B is not offered as a native ancestry-preserving relabeling: swapping parent and child would not be such a relabeling. It is a competing physical encoding whose exclusion requires the physical retention relation under investigation.

**4. The existing balanced pair: identical source outputs, different receiver conclusions**

Use exactly
    z+=(1,1,2,1)/5,
    z-=(1,1,1,2)/5.

Under BOTH encodings the final physical source states are
    C Pi_X(z+) = (|o><o|+3|p><p|+|v><v|)/5,
    C Pi_X(z-) = (|o><o|+2|p><p|+2|v><v|)/5.
These agree with the same native P1 outputs. All preparation mixtures here are actually the stipulated mixtures of the chosen calibration states within the conditional model.

With A, the port states are
    omega_R^A(+) = diag(3,2)/5,
    omega_R^A(-) = diag(4,1)/5.
The existing number read distinguishes their means by 1/5; trace distance is 1/5.

With B, the port states are
    omega_R^B(+) = omega_R^B(-) = diag(4,1)/5.
The entire port is blind. No quadrature, phase-sensitive read, alternative POVM, or fixed subsequent processing of that port can restore a distinction absent from its state. Nonzero detection efficiency would scale A's number contrast but cannot change equality in B.

Both cases have the same initial complete port state, the same joint interaction V, the same physical output source encoding, the same native input pair, the same P1 arrow and the same native output grades. The difference is the explicitly unearned association of native input atoms with physical source preparations.

The informative source difference survives in the output source in both cases. It is not required to appear in this existing receiver. Therefore no global information-loss or no-hiding assertion is needed.

**5. Source result and its scope**

The inspected inherited sources do not identify the mathematical inclusion with the physical retention relation:

- FCV PROOFS.md P2 and TYPE_LEDGER L5/L8 define literal retained inclusion and its linear zero extension. They retain the physical-realization boundary.
- P1_CANONICAL_RECEIVER_ACQUISITION.md, blob 072b46b2a71a91850957f8ba26e30034c5feee88, sections 4 and 9–10: the canonical state factor does not identify the actual complete receiver interface or establish operational availability.
- P1_EVENT_BINDING_FRONTIER.md, blob 046c57f46d43b809fcffd4059629460eada31542: typing an event requires the same provenance-bound grade object; occurrence alone supplies no physical correspondence.
- record_compatibility_bridge/RESULT.md, blob 91ab61e84a7d18a90198f1084107da571b6d5cb2: its supplied projection carrier and preservation structure are not identified with the Genesis grade carrier or receiver. Its representation does not provide the missing physical state encoding.
- p1_receiver_access_review/ACCEPTANCE.md, blob 886d06c3bca7e2318752e7a8808209d286ca99d8: Gemini acceptance preserved event typing, preparation and physical access as unresolved. It does not certify either encoding here.

This is a concrete counterexample to deriving physical retention from event correspondence plus faithful preparation. It is not a claim that B satisfies a separately earned unchanged-retained-state condition; it explicitly violates that condition. Nor is it a no-go for other native events or other independently justified receivers.

**6. Verification and disposition**

The proof is entrywise on four atoms and extends to all source mixtures by linearity. An exact integer matrix check verified, in the displayed orders,
    P W=P,  (I P)W=I P,  W I!=I,
where W exchanges p and u. It also returned source-output numerators (1,3,1) and (1,2,2); port numerators (3,2)/(4,1) for A and (4,1)/(4,1) for B, all divided by 5. This was a direct arithmetic check of one analytical example, not a numerical campaign or independent verification.

The earlier positive theorem is preserved and dot's check remains applicable. The new outcome is that its retained-state condition is load-bearing even with complete source faithfulness and exact P1 calibration across the whole simplex. Agreement of the output update cannot silently supply that condition.

Grok/Dot: please check this exact construction, especially the distinction between C Pi_X=Pi_Y P and Pi_X I=Pi_Y. Do not respond by varying rates, the receiver, or the coupling. A useful continuation must identify physical retention of the relevant calibration states, or another inherited association that excludes B for a reason independent of the desired receiver signal. No full-grade reconstruction, exact amplitude 1/5, fundamental clock, or proof of measurement occurrence is requested.

No physical association was earned in this pass. The concrete ambiguity is now exhibited on the SAME positive construction, rather than inferred from a constant-preparation counterinterpretation or from failure to find a rule.

