# Sprint B / B2
## First explicit DESI-linked expansion-response ansatz

### Goal
Construct the simplest bridge-to-observable forward model:

E_bridge(z) = E0(z) * R_bridge(z)

with the response factor tied to the locked bridge closure state, not re-fit at the observable layer.

---

## 1. Locked bridge inputs

Use the certified closure package:

- gamma_* ≈ 0.26671093
- chi_* ≈ 0.40117290
- m_* ≈ 1.40117290
- x_diff,* ≈ 0.37911244

These define the bridge state. The observable ansatz should only transform these into a redshift response.

---

## 2. Design principles for the first ansatz

The first ansatz should satisfy:

1. Baseline continuity
   If the bridge response amplitude is zero, recover E_bridge(z)=E0(z).

2. Low complexity
   Use the smallest possible response family.

3. Bridge-locked sign
   The sign of the deformation must be fixed by the bridge, not chosen to fit data.

4. Bridge-locked amplitude scale
   The amplitude should be derived from a closure scalar, not fit freely.

5. Controlled redshift support
   The response should grow smoothly over the target redshift interval instead of being singular or arbitrary.

---

## 3. Minimal response structure

Let the bridge induce a dimensionless expansion-response factor:

R_bridge(z) = 1 + A_bridge * S(z; z_c, p)

where:
- A_bridge is a locked bridge amplitude
- S(z; z_c, p) is a bounded shape function over redshift

Choose the simplest bounded shape:

S(z; z_c, p) = (z / z_c)^p / (1 + (z / z_c)^p)

So the forward model is:

E_bridge(z) = E0(z) * [1 + A_bridge * (z / z_c)^p / (1 + (z / z_c)^p)]

---

## 4. Locked bridge amplitude

Tie the amplitude to the mismatch between retained-coherence flow and diffusion lag:

A_bridge = kappa_A * (chi_* - x_diff,*)

Since:
chi_* - x_diff,* ≈ 0.40117290 - 0.37911244 ≈ 0.02206046

the raw bridge scale is already small, which is desirable for a first response ansatz.

For the first sprint pass, lock:
kappa_A = 1

So the first locked amplitude is:
A_bridge^(0) ≈ 0.02206

---

## 5. Locked shape defaults

To avoid unnecessary freedom, lock the shape defaults for the first pass:

z_c = 1
p = 2

Then:
S(z) = z^2 / (1 + z^2)

So the first explicit observable ansatz becomes:

E_bridge(z) = E0(z) * [1 + 0.02206 * z^2 / (1 + z^2)]

---

## 6. Derived observable proxies

From E_bridge(z), the first public-facing quantities to compute are:

1. Hubble-rate proxy
   H_bridge(z) = H0 * E_bridge(z)

2. Comoving distance proxy
   D_M(z) proportional to integral_0^z dz' / E_bridge(z')

3. Alcock–Paczynski-style proxy
   F_AP(z) proportional to D_M(z) * H_bridge(z)

These are enough for a first DESI-linked comparison layer.

---

## 7. First falsification rule

If the locked bridge-induced response produces the wrong sign of deviation, or an amplitude incompatible with the target DESI-linked observable across the chosen redshift interval, then this bridge version is wrong as an expansion-response theory.

---

## 8. What this ansatz is and is not

It is:
- a minimal locked bridge-to-observable map
- low complexity
- falsifiable
- tied to the closure state rather than refit

It is not:
- a production cosmology model
- a Boltzmann solver
- a full likelihood pipeline
- the final observable theory

It is the first public-science bridge.

---

## 9. Next Sprint B steps

B3
Choose the exact public comparison quantity:
- H(z)-style response
- D_M(z)-style response
- F_AP(z)-style response

B4
Lock a quantitative failure threshold:
- maximum allowed sign error
- maximum allowed amplitude mismatch
- redshift interval of validity

Prepared as the first explicit observable ansatz for Sprint B.
