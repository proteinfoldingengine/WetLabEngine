# ROUND16_SOURCE_REFRESH_PROTOCOL.md

## Why this memo exists
Round 16 is currently blocked not by the frozen scaffold, but by poor candidate-source acquisition.

Several target systems were activated correctly, but the initial PDF candidates were unrelated papers and therefore unusable for source locking.

Blocked systems so far:
- MACS J0025.4-1222
- Abell 2744
- Abell 520
- ACT-CL J0102-4915 (El Gordo)

This means the next step must be a stricter acquisition protocol.

---

## Source-refresh rule
No new candidate source should be treated as valid until it passes all of the following checks:

1. **Correct system identity**
   The title or abstract must explicitly reference the target cluster/system.

2. **Correct observable class**
   The paper must contain at least one of:
   - X-ray gas morphology / map
   - weak lensing mass map
   - strong+weak lensing mass reconstruction
   - offset table or figure useful for gas–mass separation

3. **Extraction relevance**
   The paper must plausibly support:
   - page locking
   - map extraction
   - table calibration
   - or direct scoreable profile/offset construction

4. **No generic review substitutions**
   Review papers, unrelated astrophysics papers, methods papers, and general survey papers do not count.

5. **Immediate front-page audit**
   Every downloaded PDF must be front-page scanned before it is entered into the tracker as a serious candidate.

---

## New workflow
For each blocked system:

### Step A
Find 3–5 candidate PDFs.

### Step B
Run front-page scan immediately.

### Step C
Reject all unrelated papers before any page-level scan.

### Step D
Only after a system has at least:
- one valid gas/X-ray anchor
- one valid lensing/mass anchor

may it move to:
- downloaded
- mapped_candidate
- page-locking

---

## Strategic implication
Round 16 remains alive because the current failures are acquisition failures, not model failures.

The reference core remains:
- Bullet Cluster
- Abell 2261
- Abell 1689

These keep the round grounded while expansion targets are refreshed.

---

## Recommended acquisition priority
1. MACS J0025.4-1222
2. Abell 2744
3. Abell 520
4. El Gordo

This order preserves the original merger-expansion intent while focusing first on the most Bullet-like analogs.
