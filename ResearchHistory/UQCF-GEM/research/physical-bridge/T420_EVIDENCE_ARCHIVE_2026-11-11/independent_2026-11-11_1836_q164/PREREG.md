# Q164 PREREG (2026-11-11T18:36:12-07:00). Science, local, supporting math. NOT_DERIVED; Not claimed.
Trigger: GPT PR111 6811477174 / research b6506048 (Q159_RESPONSE_TRACE_REVIEW.md). Its scope control: G_X x before and G_Y P x after give p-to-v values (1/20,-3/20) -> (2/15,-1/15), gaining 1/12 under a uniform reference reset, so a threshold read at 1/10 flips.
Question (= planned Q164): does an inherited producing operation use the potential↔source counting identification, and is GPT's gain exactly that identification?
Claims to test:
(C1) GPT's numbers, reproduced with the source's own green()/laplacian() (blob 94d946df).
(C2) Gain = [G_Y(P 1_X/n - 1_Y/m)]_p - [...]_v, independent of the state for fixed total. It is the source's 'background' term (1/m - b/n) under G_Y.
(C3) For ANY reference pair with P ω_X = ω_Y (P1-covariant reset, same total), retained gauge-invariant contrasts of G_X(x - Mω_X) and G_Y(P x - Mω_Y) agree on Y for every x. So the gain is zero and no threshold on a retained contrast can flip.
(C4) Counting references are P-covariant iff every fiber has size 1, i.e. no event.
Premises: G, L, P, S INHERITED (diagnostic). The reference reset is SUPPLIED by whoever computes. P-covariance is the INHERITED P1 naturality applied to references.
PASS: C1–C4 exact on GPT's tree plus 2 other trees, with 20 random rational x and ω_X each, seed 164. FAIL: any mismatch.
