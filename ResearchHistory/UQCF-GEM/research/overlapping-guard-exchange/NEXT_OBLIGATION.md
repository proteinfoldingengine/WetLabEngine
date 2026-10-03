# Next obligation: renewal when outside buffer slots are unavailable

SEQUENTIAL_HANDOVER.md now gives an exact safety condition for each whole-root union replacement after a fixed preparation, and an equivalent acyclic witness-selection certificate for completing this restricted schedule. SEQUENTIAL_EXAMPLES.md demonstrates both a successful sequential repair beyond the all-unions bridge and a forced cycle that excludes every order in the restricted method.

The remaining obligation is therefore more specific: break an unavoidable precedence cycle through a floor-safe change of preparation, guard choice, or protected partial exchange, and prove that the chosen remedy renews protection. A cycle in one arbitrary choice of witness edges is not a method obstruction; impossibility requires ruling out every witness selection. The forced-cycle example does so using singleton miss sets, but belongs to a solved floor-one carrier and is not a higher-floor counterexample.

Do not infer that locally eligible greedy choices always reach completion. The theorem supplies an order from a complete acyclic certificate; it does not prove that an arbitrary partial schedule extends, nor that a certificate always exists for exact endpoints. General accessibility and cycle resolution remain open.

## Existing-buffer extension

CYCLE_BUFFER.md supplies a criterion for resolving the cycle by temporarily reshaping existing slots outside both selected guards. It accounts for newly exposed small hitting sets by omitting the original buffer constraints before deriving obligations. An assigned family of obstructions can be protected by slot b exactly when the labels outside their union can meet floor a_b. Every unassigned obstruction must retain a compatible precedence witness, with an acyclic residual graph.

The new unresolved obligation is a renewing exchange when no such outside-guard buffer certificate has been established. Important cases include I union J exhausting all slots and assignments whose obstruction-avoiding label pools are too small for available floors. Neither case proves native disconnection. An alternative may change guards, interleave incidence edits within shared roots, or temporarily use supports not equal to old/new unions.

Any proposed use of a root participating in the active guard must replace the protection lost by editing it; it cannot be treated as a free buffer. A valid next theorem should expose that replacement certificate, prove an eligible exchange exists under stated structural hypotheses, show renewal after the exchange, and supply a progress measure that does not strand the remaining target edits. Total complementary capacity and exact-endpoint redundancy are still insufficient as a proof of those properties.

No numerical campaign is authorized or proposed here. The five-root higher-floor family in CYCLE_BUFFER_EXAMPLE.md is a symbolic mechanism example inside an already solved endpoint class, not a reason to resume arity-by-arity validation.
