# What a bounded unread complement can force to remain distinguishable

Date: 2026-10-14 UTC. Inspected parent: `69b8ad5a2aa5f81c93a5d91b6b8f7c16d760d325`.

**Disposition: conditional partial-access guessing bound; the specified source pair and native interface remain open.** If a complete output perfectly distinguishes m equally weighted source alternatives, and only a quantum factor of dimension q is unavailable, the remaining output has optimal guessing success at least max(1/m, 1/q^2). Thus m>q^2 forbids complete loss of ensemble information at that interface. It does not force a distinction for an arbitrarily specified source pair, supply a detector, or derive a native event.

The dimension-squared inequality is established quantum-information mathematics, not a new general theorem or priority claim. The work here is its explicit application to the preceding complementary-record route, with sharp controls inside the same supplied channel class and an audit of the native assumptions. The finite quantum factors and source preparations below are declared analytical objects. They are not new physical primitives adopted by the research model.

## 1. The unresolved premise this tests

The preceding `complementary_record_screen/RESULT.md` classifies the complete pure complement of a supplied retained-algebra expectation. It does not identify what fraction of that complement a receiver can actually access. Its complete-output invariant cannot be assigned unchanged to an arbitrary accessible subregister.

The present question is narrower: can a bound on the dimension of the unread factor force some discrimination ability on what remains, without choosing a favorable microscopic dilation? The answer is conditionally yes for a source ensemble, with a sharp q^2 loss factor. This is a quantitative obstruction to complete hiding in the stated class, not another claim that the full coherent description retains information.

The source audit does not currently justify the needed native interface. The inspected v15.11 RAS/RCR reconciliation supplies a retained algebra and a separately supplied actual record; it does not specify a native accessible complement R, its omitted factor Q, or a bound on dim Q. The lineage-retention result supplies the complete family of sufficient retained vertex sets for declared vertex observables. It neither equates vertex counts with quantum dimensions nor prescribes actual physical retention. Those are different mathematical types. The negative source conclusion is limited to the seven inspected files, not the whole archive.

| Item | Standing in this argument |
|---|---|
| Supplied retained-algebra expectation and its complete pure complement | Inherited conditional channel construction |
| Source states on that complement | A fixed analytical ensemble; native source binding is unearned |
| Factorization E=R tensor Q and dim Q=q | Declared finite output interface, not derived from lineage pruning |
| All measurements on R, known ensemble and receiver calibration | Operational capability used by optimal guessing; not a demonstrated native readout |
| Equal prior weights | Preparation convention for the discrimination test, not an event-outcome law |
| Actual occurrence, record retention and access | Still require native justification |

## 2. A bound for any finite output ensemble

Let R,Q be finite-dimensional complex Hilbert spaces with q=dim Q>=1. Fix density operators omega_x on R tensor Q, x=1,...,m, and probabilities p_x>=0 summing to one. Put sigma_x=Tr_Q omega_x. Define

    p_guess(RQ) = max_{POVM {N_x}} sum_x p_x Tr(N_x omega_x),
    p_guess(R)  = max_{POVM {M_x}} sum_x p_x Tr(M_x sigma_x).           (1)

A POVM here consists of positive operators summing to the identity on its declared space. The maximization permits every such measurement, depends on the ensemble, and does not impose an efficiency bound. It is a mathematical discrimination capability, not an actual detector or an automatic read operation available to an event.

For any positive operator X on R tensor Q,

    X <= q (Tr_Q X) tensor I_Q.                                    (2)

Here is a direct proof. For a rank-one X=|psi><psi|, write a Schmidt decomposition psi=sum_{j=1}^k sqrt(lambda_j)|a_j b_j>, with k<=q. For any vector v, Cauchy-Schwarz gives

    |<psi|v>|^2
      <= k sum_j lambda_j |<a_j b_j|v>|^2
      <= q <v|[(Tr_Q |psi><psi|) tensor I_Q]|v>.

This proves (2) for rank one. A positive spectral decomposition and summation prove it for every positive X, including unnormalized and rank-deficient operators.

Given any full-output POVM {N_x}, define

    M_x = (1/q) Tr_Q N_x.                                          (3)

The M_x are positive and sum to I_R. Applying (2) to each omega_x and using positivity of N_x,

    sum_x p_x Tr(N_x omega_x)
      <= q sum_x p_x Tr[N_x (sigma_x tensor I_Q)]
       = q^2 sum_x p_x Tr(M_x sigma_x)
      <= q^2 p_guess(R).

Maximizing the left side proves

    p_guess(RQ) <= q^2 p_guess(R).                                 (4)

This is the guessing-probability form of the established quantum leakage chain rule. The derivation above uses positive-operator algebra; it introduces no entropy-production objective, physical communication process or time parameter.

## 3. What perfect full records imply under partial access

Now assume the omega_x have mutually orthogonal supports and choose p_x=1/m. Their support projections, with any unused orthogonal complement assigned to one label, form a POVM that identifies x perfectly on RQ. Therefore p_guess(RQ)=1. A receiver can also always ignore R and guess a single label, so

    p_guess(R) >= max{1/m, 1/q^2}.                                 (5)

When m>q^2,

    p_guess(R) - 1/m >= 1/q^2 - 1/m > 0.                            (6)

The retained density operators cannot all be identical. Equation (6) is a forced statistical advantage over blind uniform guessing on the declared interface. It does not guarantee perfect discrimination, a useful finite-sample rate, or identification of a label in a single event. The associated optimal average error bound 1-p_guess(R)<=1-1/q^2 is conditional on the all-POVM capability and source preparation; it is not an earned native error contract.

An independent rank argument gives the same exact ceiling for complete hiding. Suppose every sigma_x equals sigma, with r=rank sigma and t_x=rank omega_x. Positivity implies each omega_x is supported in supp(sigma) tensor Q, which has dimension rq. Orthogonal supports give sum_x t_x<=rq. The rank of a partial trace obeys r<=q t_x: decompose omega_x into t_x pure states, each of whose reductions has rank at most q. With t_min=min_x t_x>0,

    m t_min <= sum_x t_x <= rq <= q^2 t_min,

so m<=q^2. This is an alternative proof of the complete-hiding ceiling, not a separate scientific execution.

The quantifiers matter. For every eligible fixed output ensemble and RQ interface, there exists a measurement on R meeting (5). The statement does not produce a single named measurement that works for every unknown embedding. Neither (5) nor the rank argument says that a predetermined pair x_0,x_1 has unequal reduced states. Section 5 supplies an exact counterexample to that inference.

## 4. Sharp controls within the inherited full-erasure channel

First consider the generalized Bell states on C^q tensor C^q,

    |beta_ab> = (1/sqrt(q)) sum_{j=0}^{q-1}
                  exp(2 pi i a j/q) |j> |j+b mod q>,
    a,b=0,...,q-1.                                                 (7)

Their inner products are delta_{a,a'} delta_{b,b'}: the shift labels must agree, and the remaining root-of-unity sum vanishes unless the phase labels agree. Tracing either factor gives I_q/q. Thus any m<=q^2 of these states have orthogonal full records but identical retained states, with p_guess(R)=1/m. A quantum unread dimension q can hide q^2 classical alternatives through correlations; substituting the classical count q would be false.

These are analytical controls, not proposed native encodings. To connect their freedom to the exact channel already inspected, fix the full-erasure expectation on H=C^m,

    Phi(X)=Tr(X) I_m/m.

The previous report gives its minimal complete complement

    Psi(X)=I_U/m tensor X_B,       dim U=dim B=m.                    (8)

For source states |x><x| on B, the complete complementary records omega_x=I_U/m tensor |x><x| have mutually orthogonal supports. Applying any isometry to the complete environment changes its embedding but leaves the system channel Phi unchanged.

At m=q^2, label x by (a,b), and choose the environment unitary

    |u>_U |x=(a,b)>_B -> |u>_{R0} |beta_ab>_{R1 Q},
    dim R0=m,  dim R1=q,  dim Q=q.

Both environment spaces have dimension m^2. The accessible register R=R0 tensor R1 has the same state I_m/m tensor I_q/q for every source. Complete hiding is therefore attained at the threshold inside the pure-dilation realization class of the SAME fixed full-erasure channel. It is not obtained by replacing Phi with a different channel.

For m=L q^2, with L>=1 an integer, write x=(g,a,b) and keep g as an orthogonal retained flag. Use

    |u>_U |g,a,b>_B -> |u>_{R0} |g>_G |beta_ab>_{R1 Q}.             (9)

This is again a unitary between equal-dimensional environment spaces: dim(R0 tensor G tensor R1 tensor Q)=m L q^2=m^2. The retained state reveals g perfectly and contains no information about a,b within that group. For the uniform ensemble,

    p_guess(R)=1/q^2.

To verify optimality directly, the q^2 labels in each group share one density operator; summing their POVM effects gives success at most 1/m per group, and L groups give L/m=1/q^2. Measuring g and choosing any one label in its group attains it. Thus the loss factor in (4) and the floor in (5) are sharp for arbitrarily many alternatives, including the nontrivial m>q^2 regime. No exact optimum is claimed here for every other value of m.

## 5. A specified pair can still be completely hidden above the threshold

Take m=5 and q=2 in the SAME five-dimensional full-erasure channel (8). Embed B=C^5 into R1 tensor Q with dim R1=3 and dim Q=2 as follows:

- Labels x=0,1,2,3 map to the four Bell states in span{|0>,|1>}_{R1} tensor Q.
- Label x=4 maps to |2>_{R1}|0>_Q.

These five output vectors are orthonormal, so this is an isometry. Keep U=C^5 in the accessible R0, and put R=R0 tensor R1. The full environment isometrically embeds from dimension 25 into dimension 30. This is an allowed nonminimal pure dilation of the unchanged system channel, with dim Q still 2.

After tracing Q,

    sigma_0=sigma_1=sigma_2=sigma_3
      = I_5/5 tensor (|0><0|+|1><1|)/2,
    sigma_4=I_5/5 tensor |2><2|.                                   (10)

The full complementary records remain perfectly distinguishable. On R, the two displayed blocks can be separated perfectly, but the first four labels cannot be separated at all. Uniform guessing succeeds with probability 1/5 from the first group and 1/5 from the fifth label, hence

    p_guess(R)=2/5 > 1/5,      while sigma_0=sigma_1.

This is consistent with the lower bound 1/q^2=1/4. The nominated pair 0 versus 1 has zero retained trace distance and no distinguishing measurement on R, despite m>q^2. The counterexample defeats the inference from some ensemble information surviving to the actual pair of interest being readable. It uses a nonidentity, fixed-channel realization with orthogonal full records, not an absence-of-action or all-NOOP argument.

## 6. Native scientific meaning and stopping boundary

The mathematical contribution to this route is a sharpened question: a justified bound on unread quantum dimension would restrict how completely a fixed source ensemble can disappear from an available receiver. It can force a nonzero statistical capability without uniquely choosing a microscopic dilation. The constructive encodings above establish tightness and reject stronger claims; they do not propose how a native event acts.

No such native dimension bound or receiver factorization was found in the inspected sources. In particular q is a Hilbert-space dimension, not a count of pruned lineage vertices, edges, branches, classical records, units of energy, duration or entropy. An isometry that preserves the complete complementary trace distances may redistribute information between a chosen R, Q and their correlations. The complete-output invariant from the previous report therefore does not fix the partial-output discrimination law.

| Question | Bounded answer |
|---|---|
| Can an unread q-dimensional quantum factor hide arbitrarily many perfectly distinguishable alternatives completely? | No; identical R marginals require m<=q^2 |
| Does m>q^2 force some retained ensemble information? | Yes, in the fixed uniform, orthogonal-record family, assuming arbitrary measurements on R |
| Is a unique microscopic dilation required for this bound? | No |
| Does the bound identify a fixed detector or establish actual readout? | No; ensemble knowledge, calibration and accessible measurement operations remain separate |
| Must a predesignated pair become distinguishable on R? | No; the five-label control shows exact failure |
| Is q or the source-to-quantum-factor association earned by lineage retention? | Not in the inspected sources |
| Is this a derivation of native event action or a physical force? | No |

The next admissible advance on this route must start with an inherited source family and an available receiver/retention relation, then derive a readout consequence. It may justify the omitted-factor bound used here, or directly establish a readable actual source pair without it. Choosing m large, q small, a favorable factorization, the Bell embedding, or the full-erasure channel does not itself earn any of those native premises. The threshold is a sufficient test within this declared family, not a universal requirement for every candidate interaction.

The user's milestone remains **NOT ACHIEVED**. A genuinely derived probabilistic source-to-record law with justified access may qualify; deterministic outcomes, a unique microscopic mechanism, guaranteed completion, full C3 or a gravity theory are not added as prerequisites. Conditional RAS/RCR, source binding/grade and record-compatible order retain their existing scopes. Path A remains active and Path B closed. Time remains pruning / ordered recoverability update. No clock, energy law, geometry, dark-matter primitive or gravity selector is introduced.

Disposition code: `CONDITIONAL_PARTIAL_ACCESS_GUESSING_BOUND; SPECIFIED_PAIR_AND_NATIVE_INTERFACE_OPEN`.

No scientific module, enumeration or numerical campaign was executed. These proofs and controls were developed analytically before any such campaign; they are not retrospectively labeled preregistered. Text/hash/provenance checks do not add scientific test counts. No main merge, historical recertification, numbered-stage closure or CLOSED/CERTIFIED status is claimed.

## 7. Sources and review scope

Seven exact repository sources at the inspected parent are preserved in `source_packet.json` and `source_identities.json`: AGENTS.md; the previous complementary-record report; the continuation index; the physical-frontier decision; the native-event milestone; the v15.11 RAS/RCR report; and the lineage-retention analysis. Their full bytes and Git blob identities bind the inherited claims. No uninspected archive-wide absence is asserted.

Primary mathematical context, consulted 2026-10-14:

- Yi-Hsiu Chen, Kai-Min Chung, Ching-Yi Lai and Xiaodi Wu, *Leakage Chain Rule and Superdense Coding*, manuscript, September 8, 2017, Lemma 2.3, Theorem 3.1 and its positive-operator claim: https://homepage.iis.sinica.edu.tw/~kmchung/download/Leakage%20Chain%20Rule%20and%20Superdense%20Coding.pdf . The stated guessing/min-entropy relation and chain rule imply (4). The paper credits the chain rule to Winkler et al., Lemma 13. No originality of that inequality is claimed here.
- John Watrous, *The Theory of Quantum Information*, Chapter 3, section 3.1, state discrimination: https://cs.uwaterloo.ca/~watrous/TQI/TQI.double.3.pdf . This supplies standard context for the POVM optimization in (1).

The elementary proofs and channel controls needed for this application are written out above. Independent whole-argument review and a separate source/publication audit are recorded alongside the report. Each certifies only its stated analytical or provenance scope; neither establishes a native physical mechanism.

