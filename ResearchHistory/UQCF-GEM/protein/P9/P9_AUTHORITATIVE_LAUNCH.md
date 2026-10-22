# P9 Authoritative Measurement Launch

This commit authorizes the first and only preregistered P9 native-evaluation measurement.

Frozen scientific preregistration:
- `f194ad2eabfb722983bf2aac84df4da51f49712c`

Frozen source/protocol manifest:
- commit `0f723410c39ba4fe03471720ec59d5acfc0c1fc3`
- blob `16ab23c9405b371af6886cf034e79370c54359bc`

Core RED -> GREEN:
- RED run `35383675093`, job `105725497187`: expected missing `p9_core`
- GREEN head `b4573dd46436adc36fd7b957b4f546bdf0f00079`
- GREEN run `35383868978`, job `105726089975`: 8/8 passed

Measurement RED -> GREEN:
- RED run `35384177378`, job `105727066161`: expected missing `p9_measurement`
- GREEN implementation head `9b1cffb92deb74ae09aa73a018ba9f2405d45e45`
- GREEN run `35384332131`, job `105727569880`: 5/5 passed

Premeasurement certification:
- commit `394825cd62ecce101358cce012cdc6f3126f8482`
- blob `95bfc9f8fd7389e689778eccc7078d83e0d0f0d4`

Authoritative workflow:
- commit `63d038c790df009ef7e26cb52e5e3a3965afdb2a`
- blob `7a2ffda9937bc2d683b348e2b2c9bc9c0cf7637d`

At the moment immediately before this launch commit, no P9 96-state native-evaluation/handoff outcome had been executed or exposed.

No coefficient, score formula, target, seed, checkpoint, generator dynamics, handoff dynamics, endpoint, statistical test, or GO/NO-GO rule is changed by this launch.
