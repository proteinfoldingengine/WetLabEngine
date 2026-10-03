# Next obligation: protected resolution of forced cycles

SEQUENTIAL_HANDOVER.md now gives an exact safety condition for each whole-root union replacement after a fixed preparation, and an equivalent acyclic witness-selection certificate for completing this restricted schedule. SEQUENTIAL_EXAMPLES.md demonstrates both a successful sequential repair beyond the all-unions bridge and a forced cycle that excludes every order in the restricted method.

The remaining obligation is therefore more specific: break an unavoidable precedence cycle through a floor-safe change of preparation, guard choice, or protected partial exchange, and prove that the chosen remedy renews protection. A cycle in one arbitrary choice of witness edges is not a method obstruction; impossibility requires ruling out every witness selection. The forced-cycle example does so using singleton miss sets, but belongs to a solved floor-one carrier and is not a higher-floor counterexample.

Do not infer that locally eligible greedy choices always reach completion. The theorem supplies an order from a complete acyclic certificate; it does not prove that an arbitrary partial schedule extends, nor that a certificate always exists for exact endpoints. General accessibility and cycle resolution remain open.
