# P8B Authoritative Measurement Launch

This commit authorizes the first prospective P8B native-evaluation measurement under the frozen contract.

Frozen premeasurement head:

`a85a50c9f9ccdc95871afb653a5200da3ce01007`

Required prior certifications:

- P8 source certification: run `35358832587`, artifact `10553705794`
- P8B core RED: run `35359790594`
- P8B core GREEN: run `35360068820`
- P8B measurement RED: run `35360601418`
- P8B measurement GREEN: run `35360883897`

The launch does not modify the scientific implementation, coefficients, targets, seeds, thresholds, controls, optimizer, step budget, endpoint, or GO/NO-GO rule.

The authoritative workflow must refuse execution if the diff from the frozen premeasurement head contains anything other than the authoritative workflow and this launch marker.
