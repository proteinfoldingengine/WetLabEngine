# C3 partial-seed event theorem — author-side audit

Date: 2026-10-07.
Status: AUTHOR-SIDE ANALYTICAL AUDIT; independent review pending.
Frozen scope 542782cd198b65e9bfd79dd88193251666e74637.
Proof e7a6c7286f08256efd188e3a5357f08cb7a1b961.

1. Prefix constraints q0+s_j in [0,N] yield L=max(0,-min s), U=min(N,N-max s).
2. Sufficiency is constructive: if next event adds, next count<=N ensures an absent label; if next event deletes, next count>=0 ensures a present label.
3. Every spectator-only prepared state preserves tau3 and floor2, so count-feasible histories are also native protected histories.
4. Feasible current q interval is exactly [L+s_n,U+s_n], not merely a bound.
5. Current b determined iff interval is {0} or entirely positive; ambiguous iff A=0<B.
6. In ambiguous case the two fibers share N/sign ledger but optimal first moves differ (+w(r4) vs -d(r4)); the eight-edit buffer route remains universally legal.
7. Positive controls: N2 signs (-,+) forces b1; (+,+,-,-) forces q0=0. Negative controls: N2 (+,-) leaves b ambiguous; N1 (+,+) invalid.
8. Known N and COMPLETE valid spectator-only direction stream remain declared inputs. No native observer-access claim.

No numerical campaign, formal proof assistant or independent review is claimed.
