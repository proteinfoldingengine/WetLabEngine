# Test harness correction
The first implementation run passed complete independent certificate equality and the moving-cover fixture, but three adapted mutation controls were faulty.
- The first canonical source here has tau5 and protected=false. Assigning false again made no corruption. The corrected test flips the Boolean.
- The old six-root host index5 was retained in two list mutations. This domain has five roots and host index4. Corrected invalid-state and retained-marker controls now mutate the actual host entry.
These were test-harness defects, not mathematical counterexamples. The original frozen tests and absent-implementation RED are preserved in history; harness_failure.log preserves the full subsequent failed run (1 failure,2 errors). The producer, independent algorithm, theorem and enumeration domain are unchanged.

