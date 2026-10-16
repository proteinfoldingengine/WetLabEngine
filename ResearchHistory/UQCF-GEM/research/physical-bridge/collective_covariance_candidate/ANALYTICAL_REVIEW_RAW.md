# Independent analytical review: collective-covariance candidate

Review date: 2026-10-16 UTC.

Reviewer role: independent adversarial mathematical/scientific reviewer, separately dispatched from the candidate author. This review was authored from the four exact local inputs listed below and the identified source context. I did not modify the producer's inputs.

**Decision: no blocking mathematical or claim-boundary defect found. The exact candidate is suitable to proceed to a separate publication audit as a bounded conditional analytical assessment. No revision is required by this review. The native informational-difference milestone remains NOT ACHIEVED.**

This is argument review, not numbered-stage certification, a historical numerical reproduction, publication closure, or approval to merge to main.

## Exact reviewed inputs

Repository named by the packet: `proteinfoldingengine/WetLabEngine`.

Branch named by the packet: `research/uqcf-overlapping-guard-exchange`.

Frozen source parent: `0583236e036fc9bfad2481721be6cfc4dd9a4cf3`.

Source tree named by both manifests: `2203341fc5437bd400b5289324bfad6115e62029`.

The reviewed directory is `/workspace/scratch/554be2c0fb22/uqcf-research/candidate/`.

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| `RESULT.md` | 16341 | `5b58822c309013cfb6c07b528a3dafc8360f15d3c587a2fb52143ec04f4b3eb7` |
| `INDEX_APPEND.md` | 2004 | `ca85e0ea7dc98ba062b9a80a72426ffbcb8ee2909aacd038f608abde6e6a4a06` |
| `source_packet.json` | 186446 | `c51f7dafd232c38e8426b3abaa472bb7f474d6585cf974b1d069a3ed6774c7dd` |
| `source_identities.json` | 5399 | `330c4a81b1d6500a27168489cc309120725d37e2b4fa6bcfd16d181f72e4f059` |

For all eleven source records, I independently encoded the packet's content as UTF-8 and recomputed its byte length, SHA-256, and Git blob SHA-1 using `SHA1("blob " + decimal_byte_length + NUL + bytes)`. Every value matched the identity manifest and the packet's declared Git blob. The source path sets were exactly equal and the manifest had no duplicated path. Parent, tree, and immutable GitHub URL construction also agreed.

| Packet source, relative to `ResearchHistory/UQCF-GEM/` | Matched Git blob |
| --- | --- |
| `AGENTS.md` | `e5407215a81b914fc02f5c107333a2f0261634ee` |
| `research/physical-bridge/NATIVE_EVENT_MILESTONE.md` | `46c27da7d5a049820ebde455b91863f071b621e5` |
| `research/physical-bridge/COUPLED_C3_NATIVE_RECORD_ORIGIN_CONTINUATION.md` | `abbfeef0b2a720fe78ba7fb18838ad5b7386b9bc` |
| `research/physical-bridge/retained_reader_write/RESULT.md` | `d85dd9e4178488de9bf27c81111c46a477823a2c` |
| `research/physical-bridge/compatible_history_seed/RESULT.md` | `73a72a552b8a23f74f2d075196060a2af5efb48d` |
| `research/physical-bridge/record_compatibility_bridge/RESULT.md` | `91ab61e84a7d18a90198f1084107da571b6d5cb2` |
| `research/physical-bridge/finite_interaction_witness/ASSESSMENT.md` | `e0deabc1a9b26ad1a3be7284487828df452796b6` |
| `v15/v15.09/REPORT.md` | `ec73ef9240dcef062c95a82c511a874d0d2923ef` |
| `demos/v15.56-response-selector-obstruction/source-free-covariance/DERIVATION.md` | `b8f058013143bc0785d34a30d43e3f5ca65dd1f2` |
| `demos/v15.56-response-selector-obstruction/covariant-source-couplings/DERIVATION.md` | `714ccd9f382745c9f29b18e1be5ef0159ada8aac` |
| `demos/v15.56-response-selector-obstruction/covariant-source-couplings/RESULTS.md` | `4a5efc95b50d57ef07deb24d924b27061c601f07` |

These checks establish content identity against the supplied blob identifiers. They do not independently authenticate that the remote parent commit has the declared tree or contains every listed path. That Git reachability/publication check belongs to the separate publication audit; this review does not pretend to have performed it.

## Mathematical reconstruction and adversarial checks

### The unitary classification is correct and complete

The Pauli proof in RESULT section 2 works for arbitrary complex coefficients. The single-factor vector coefficients must vanish under all proper rotations. The three coordinate half-turns eliminate every off-diagonal entry of the coefficient matrix T; coordinate quarter-turns then make the diagonal entries equal. There is no unexamined antisymmetric tensor term: an antisymmetric two-index tensor would correspond to a rotation-invariant vector, which must vanish. Thus the commutant is exactly the complex span of I and F.

I also checked the classification independently in the computational basis. Commutation with total Z separates the one-dimensional spaces spanned by |00> and |11> from the span of |01>,|10>. Commutation with the total raising and lowering operators links |00>, (|01>+|10>)/sqrt(2), and |11>, forcing one common eigenvalue on that triplet. The orthogonal singlet is one-dimensional and has its own eigenvalue. Unitarity makes the two eigenvalues phases. Hence U=u_+ P_+ + u_- P_-, which is exactly exp(i phi)[cos(theta) I-i sin(theta)F] for real phi and theta. Conversely these operators commute with every collective rotation and are unitary.

The relevant nonidentity condition is a nonidentity channel, or equivalently a nonscalar unitary. It is exactly sin(theta) != 0, as stated. A nontrivial global phase alone does not count as an interaction. Neither a Hamiltonian nor a time parameter is needed for this finite-operation characterization.

The quantifier is over a fixed common U on the two supplied identified qubit factors. The argument does not cover arbitrary source-dependent operators, larger carriers, general channels, or independently changing local frames. The text makes those boundaries explicit.

### The inherited pair acquires precisely the claimed local contrast

The source pair and blank are present in the preceding retained-reader report: |00> and |10>, with Q=I tensor |1><1|. They have the same initial memory state and zero initial Q probability. Their use is therefore not a replacement of the source pair chosen after a numerical signal.

For the classified U, |00> only gains a phase, while |10> maps to c|10>-i s|01>. Taking the source partial trace removes the cross terms and gives the two memory states stated by the author. Their difference is s^2(|1><1|-|0><0|). With the usual half-trace-norm convention, its trace distance is s^2, and the total-variation distance of the binary readout laws is also s^2. Equation (4) follows from the zero initial Q contrast.

This is a source contrast, not merely a change of the blank: the same operation and same reader are compared on both inputs. A positive outcome has no false positive for b=0 under the exact model. A zero outcome can remain ambiguous. The text correctly avoids calling a positive probability a guaranteed event or a deterministic write, except at the full-transfer values s^2=1.

The common-mixture extension is also correct. The averaged binary laws are (0,lambda), where lambda is the integral of sin^2(theta). A nonnegative measurable function has positive integral exactly when its strictly positive set has positive probability measure. Consequently the author's condition refers to positive measure of the set of nonidentity members, not to a positive atom at some particular angle. Independence of the mixture from b is explicitly part of the conditional interface, and no readable mixture label is added.

The absence of a uniform positive lower bound is correctly acknowledged. Strict pointwise positivity over nonidentity U does not by itself supply a common finite sampling guarantee or an experimental error budget. This limitation does not invalidate the eligible partial or probabilistic consequence in the ideal conditional model.

### Retention and access are separated correctly

For a trace-preserving tracial expectation retaining Q, E_A^*(Q)=Q. Therefore the Q probability after E_A equals that before E_A, and repeated application proves preservation under any finite succession retaining that same reader. The text claims preservation of this binary readout law; it does not infer occurrence of a measurement, an actual outcome, or stability under arbitrary future operations.

The invariant-reader control is substantive. Every jointly invariant effect lies in span{I,F}, so it commutes with U and has unchanged statistics. The singlet projection P_- has probability 0 on |00> and 1/2 on |10> already at input. That joint invariant distinction was not newly acquired by a blank memory. The report therefore does not obtain local access merely by replacing the intended reader with a convenient invariant joint detector.

The blank's orthogonal projector specifies a qubit reader without another independent axis once the blank and factor identification are supplied. This covariance of its description does not furnish an apparatus or a source-associated retained output. Sections 1, 4, and 6 explicitly retain those obligations. No RCR outcome selection is inferred.

### The rejecting controls have their advertised force

Identity remains in the symmetry class. An independently justified nonidentity occurrence is necessary for this route; a named event or strict pruning operation elsewhere does not establish it.

Independent local invariance forces U to commute first with all V tensor I, giving I tensor B, then with all I tensor W, making B scalar. This is compatible with the different three-qubit superoperator setting of v15.78. Dropping the independence of local frames is an additional representation restriction, not a native derivation.

The source-reset countercontrol is genuinely CPTP. Kraus operators K_ab=(|a><b|/sqrt(2)) tensor I, for a,b in {0,1}, give the stated map and satisfy sum K_ab^dagger K_ab=I. Partial trace and the maximally mixed source show collective channel covariance directly. Both pure sources change, but both memory states remain blank. Thus nonidentity channel activity plus covariance alone does not yield the claimed transfer; the unitary scope matters.

The distinction from the preceding swap average is exact. At theta=pi/4, the partial swap's output on |10> is pure with nonzero coherence between |10> and |01>; the average of identity and full exchange is mixed on that input. Their coincident local probabilities do not identify the two channels or turn the previous expectation into a reversible native coupling.

The inverse-operation control correctly defeats an unrestricted persistence claim, and the stated record write is not a universal cloning claim. None of these controls requires a numerical run.

## Native-source and milestone assessment

I read the packet's governing AGENTS and native milestone in full. I checked the immediately preceding retained-reader assessment, the relevant continuation entries, the compatible-record and compatible-history boundaries, the finite-interaction assessment, v15.09, and the v15.78/v15.79 symmetry distinctions.

The native milestone permits nonunique microscopic mechanisms and partial or probabilistic outputs. It still requires earned native input, action, and retained access. The candidate does not replace that criterion with a demand for deterministic outcomes, a uniform strength, full C3 implementation, gravity, or all conceivable dynamics. Its two-qubit unitary assumptions are explicitly restricted to this route.

The source packet supports the inherited quantum control pair and the reader-retention criterion. It does not establish a native source/receiver tensor carrier, a shared representation, a physical law imposing the collective symmetry, nontrivial reversible occurrence, or accessible local readout. RESULT accurately lists these as gaps. The compatible projection tree is never identified with a qubit, a Pauli frame, a Genesis address, or the incidence-source pair. The v15.09 carrier stop and v15.08 source-semantics stop are not reopened. The positive conditional RAS/RCR and earlier supplied interactions remain available in their original scopes.

The v15.79 use of transforming source data is correctly distinguished from fixed-operation invariance. It does not select the present family or its coefficients. The source-reset control also prevents converting a generic notion of event activity into a nontrivial unitary on the particular two-factor carrier.

INDEX_APPEND gives the same disposition and limitations as RESULT. It neither silently upgrades the result to native interaction nor claims numerical execution, an increased historical test count, or numbered-stage closure.

## Is this useful progress or repetition?

There is a limited, defensible addition relative to the immediately preceding report: the proposed symmetry assumption is converted into a complete unitary class, and that entire nonidentity class is shown to satisfy the already stated pair-specific acquisition criterion. The invariant-reader and nonunitary countercontrols identify which interface assumptions are doing the work. This is more precise than demonstrating one chosen copying gate or repeating the existing swap-average marginal calculation.

It is nevertheless standard conditional quantum mathematics on supplied inputs, not new native mechanism evidence. None of the first unearned native premises has been discharged. The family removes the need to choose a particular nonzero angle for qualitative separation, but it does not remove the need to justify why this carrier, symmetry, reversible action, nonidentity occurrence, and reader are physically available. Repeatedly exploring additional angles, simulations, or decoders would not advance that obligation.

The report's own stopping rule is therefore essential and appropriate: retain this as a conditional candidate specification and premise audit, and require independent native source/receiver/action/access evidence before treating this route as physical progress. Calling this an achieved native milestone or a newly discovered quantum mechanism would be misleading; the reviewed text does neither. The common-response continuation's earlier stop is not defeated merely by having a new conditional family.

I checked the cited [Ziman et al., Quantum homogenization, arXiv:quant-ph/0110164](https://arxiv.org/pdf/quant-ph/0110164), specifically the partial-swap definition/marginal formulas in section II and its uniqueness discussion under homogenization conditions in section IV. The report describes that prior context accurately and does not claim priority. The candidate's collective-invariance proof stands on its explicit assumptions; no reservoir or time law from that paper is imported into the native model.

## Review limits and final disposition

No critical or important correction is requested. The conclusion is conditional analytical acceptance of the exact four input hashes above, subject to the independent publication audit. A change to claim-bearing text requires a review of the changed text and rebinding to its new hashes.

My executable checks were document parsing and provenance hashing only. I imported no scientific module and performed no simulation, numerical matrix calculation, scientific enumeration, inherited test run, or historical replay. The mathematical checks above were direct reasoning. The packet's historical results were source context, not newly reproduced or recertified evidence.

Separate publication auditing must establish repository membership and durable final bytes, preserve this raw review as authored, and bind the eventual published text. This review is not that publication audit. Native interaction remains NOT ACHIEVED; broad C3/C4-C6 remain OPEN, Path A remains active, and Path B remains closed.
