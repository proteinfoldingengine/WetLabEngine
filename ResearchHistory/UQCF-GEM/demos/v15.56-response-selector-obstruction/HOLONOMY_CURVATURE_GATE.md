# Finite holonomy response -> curvature-density identifiability gate

**Pinned baseline:** `1ff3500689c3d764a9a9b7ce81c853303904ed74`.

## Adjudication

The matched-completion result survives as a genuine gauge-invariant **finite holonomy response**, but this finite bridge does **not** yet determine a curvature 2-form or curvature density.

A local curvature 2-form extracted from loop holonomy requires an independently supplied oriented area/bivector and a controlled small-loop/refinement prescription. Those objects are not supplied by the three-site completion-to-connection witness. This matches the existing v13.27 claim boundary: a raw SO(3) loop angle is not Riemann, sectional, or Regge curvature, nor a continuum curvature density, without area scaling and a refinement limit.

## Exact scale-freedom control

Keep the certified state, source, pair-correlation response, polar links and loop response unchanged. For `h=+1/100`, the existing source-scale-free loop-trace response is

`T'/M' = -144/625`.

If one merely declares a positive loop area `A`, a candidate density scales as `(T'/M')/A`. Three diagnostic area conventions, used only as non-identifiability controls, give:

- `A=1 -> -144/625`
- `A=3/7 -> -336/625`
- `A=11/5 -> -144/1375`

Nothing in the quantum state, source, connection, or holonomy changed. Thus finite holonomy response alone cannot identify a curvature magnitude.

## Trace-completeness control

Set the base edge rotation to identity while retaining a nonzero hidden response. Then the initial loop is `H=I`, so `Tr(H)=3` and `d Tr(H)=0`, while the matrix-valued holonomy derivative is nonzero. Loop trace is therefore a useful conjugacy observable where sensitive, but not a complete curvature/holonomy coordinate at every base point.

## Earned boundary

The certified arrow remains:

`supplied hidden completion + supplied source -> pair response -> polar-connection response -> gauge-invariant finite holonomy response`.

The next arrow,

`finite holonomy response -> curvature 2-form/density`,

is **not yet derived**. It requires, without fitting: (1) an oriented loop area/bivector from retained geometry, (2) a lawful shrinking-loop refinement family, and (3) a compatible local logarithm/Lie-algebra branch whose `log(H)/Area` converges.

No Riemann curvature, Regge deficit angle, Einstein tensor, gravity law, or new physical coupling is claimed.

## Next gate

Search the already-earned retained/solder/refinement stack for a canonical area/bivector and shrinking-loop family. If both exist, reuse this same matched-completion/source fixture and test convergence of the holonomy response to a gauge-covariant curvature response. If not, record the missing object as an architectural obstruction rather than substituting another proxy.
