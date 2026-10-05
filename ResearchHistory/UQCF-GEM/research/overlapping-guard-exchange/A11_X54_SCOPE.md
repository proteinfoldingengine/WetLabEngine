# A11.X54 analytical scope - quadratic sparse-anchor renewal

Parent: 89b29986c918d06e9376629c7fcbba481bbf821d.
Objective: remove X53's dense complementary-four carrier and prove a reusable multicover handover from a quadratic family of actual three-role supports.

Already-known reasoning disclosed before freeze:
- Let m>=10, A={0,1,2,3}, R={4,...,m-1}, n=m-4>=6. Declare one type Q={a,u,v} for every anchor a in A and outside pair {u,v} subset R, with arbitrary positive original labelled copies. There are 4*C(n,2) types.
- This template has unique four-role cover A. If a candidate four-set misses anchor a, hitting every outside pair requires at least n-1>=5 outside roles, impossible.
- Every role footprint F of size<=4 other than A has an actual avoiding type: choose an anchor outside F and two outside roles outside F. The only noncommon pair during a one-label full ownership cycle is its selected pair x0,x2, with footprint A.
- Existing type v={2,5,7} is a new witness and u={1,4,6} an old witness for that pair. Selected-label covers A, L={0,2,4,6}, and K2={m-1,0,1,2} have explicit exception sets. Process v first, all source exceptions of L second, b={0,5,7} third, remaining source exceptions of K2 fourth, all other types fifth. This appears to preserve actual pair witnesses and old/new copy coexistence, with b before c={3,4,6} so the endpoint-cover pair fails on that schedule.
- Use arbitrary initial singleton or larger role groups. For t>=1 full-cycle columns, each role starts with t selected labels plus its own fixed original padding. Move column h from role j to j+1, one full cycle at a time. Counts restore after every cycle; original supports/floors may be saturated and unequal.
- Every cycle changes every root; the full endpoint union is two-covered. For t>=2 every root remains unfinished relative to BOTH outer endpoints after the first cycle, yet the protection and next-cycle conditions renew.
- Literal endpoint-containing primitive lists attain the outer endpoint-incidence minimum. With one copy per type, the symbolic count appears to be exactly 12*t*(n-1)^2, derived from cyclic adjacency counts, not a benchmark.

Prove all actual pair cases, exact endpoint tau4, five-stage eligibility, floor/copy legality, renewal and next-cycle availability, well-founded descent, full labelled restoration and minimum count. The singleton one-cycle control should require exactly three cover identities on THIS constructed schedule; no all-order obstruction is proposed. Supplied template/cyclic columns/group counts remain hypotheses; arbitrary endpoints are not normalized to this form.

Freeze exact candidate for fresh whole-argument and distinct reporting reviews. Publish only analytical files on the research branch with conflict/readback/source checks. No numerical execution, implementation, benchmark, integration merge, numbered stage or physical claim. Preserve all failed constructions, v16.55/v16.54 and evidence. Separate efficiency work remains unstarted.
