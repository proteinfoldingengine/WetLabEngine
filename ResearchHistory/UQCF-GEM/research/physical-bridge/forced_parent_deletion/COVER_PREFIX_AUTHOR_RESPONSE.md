# Author challenge before independent review

This file preserves a collaborator's literal adverse finding on the first full draft, blob dceb0c3b9e5fe83e84f950f1a44682edbd0b2d4b. The collaborator was GPT /root/grade_consumer_source, not Gemini or Grok. This check does not substitute for the required independent Gemini whole-argument review.

> No substantive proof defect found in frozen blob `dceb0c3b9e5fe83e84f950f1a44682edbd0b2d4b`. The only wording correction is at line 67: \(T\) violates coarse preservation **as a rule**, not on every input. It preserves the coarse source when \(g(j)=g(h)\), including \(g_0\), and violates it for \(g_1\). The latter is sufficient for the counterexample. Suggested wording: “At H9, \(T\) violates coarse preservation for \(g_1\), although it fixes \(g_0\).” No change to the proof or result is needed.

Author resolution: accepted. Section 4 now states that T violates coarse preservation on g1, fixes g0, and fails the condition exactly when g(j) differs from g(h). The same fixed linear T still maps both positive preparations to the same grade. No scientific source or recorded path changed. The original draft text is also present in the append-only PR153 comment 7067193458.

The collaborator inspected all archived high-path states for the K marginal argument. This is additional author-side checking, not a numerical campaign, independent model acceptance, or physical identification.
