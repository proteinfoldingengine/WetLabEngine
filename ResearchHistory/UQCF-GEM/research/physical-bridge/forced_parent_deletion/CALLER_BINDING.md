# The original caller reaches the later computation and bypasses the prune witness

The pinned V1687.16 program creates its four branch vectors from a seed and fixed support masks. It evaluates all five groupings on those vectors. Its later algebra audit does consume the original B3 and B4 arrays. The two-prune input that gives the 207-unit change is outside that builder's matched-input domain. This locates the first missing correspondence at the write into the branch vector, before the original next computation.

## Existing write and later use

In the original script, lines 34–51 define MASKS, values_for_mask, gate_values and build_base. Inactive slots are zero. Active slots use the remainder modulo 29, with a nonzero fallback when the base value is zero. Hence each supplied mask is exactly the nonzero support at every integer seed. Line 56 invokes bracket4_all, which evaluates B3 and B4 in the same unconditional dictionary at lines 16–23. Line 101 supplies the default seed via build_base(). There is no state-update argument in that constructor.

At lines 87–99 and 105, algebra_generator_audit receives the built arrays, computes six pair recombinations, appends all five already computed brackets and visits every unordered pair of the resulting 15 vectors. Profiling the unmodified audit confirmed that exact array objects for both B3 and B4 reach recombine. There are 105 pairs. This is an actual later numeric consumer in the software. It receives an enumerated table of states and returns aggregate projection-faithfulness diagnostics. The call does not establish receiver ownership or physical activation.

The projection in nested_bracketing_faithfulness does construct separate inputs. It subtracts the H4 residual direction after projection onto the span containing the original branch vectors. When the residual is nonzero its direction is orthogonal to every original branch vector, and when it is zero the direction is zero. The projection fixes those input branches in exact arithmetic. Replaying the inherited implementation confirms this to 1e-9. It is a symmetric linear operator, whereas the tested literal leaf-to-parent fold has a 1 at row parent, column leaf and a 0 at row leaf, column parent. This route supplies no write corresponding to the two specific pruning edits.

The supported B4 example in the earlier comparison removes J3 slots 3 and 9 into 4. It clears two original active slots and writes a formerly inactive slot. The input mask rejects it at every seed, independently of the gate. All six B4 scalar matches change at least one such support condition. This rejection concerns the pruned input vectors. It does not by itself rule out another native operand with a coincident output.

## Exact seed calculation at the same probe

Keep the entire left vector J1 and the outer gate fixed at their archived defaults. With integer seed s, J1[0] is −9. The raw expression before its zero fallback is (5(s+3)+14) mod 29 minus 14. The fallback at slot 0 gives +1, so the value −9 forces 5(s+3)+14 ≡ 5 mod 29. This fixes s ≡ 1 mod 29 and therefore fixes all four branch vectors.

The outer gate is entry 17. Its numerator is (s+17) mod 11 plus 2, and its denominator is (s+34) mod 7 plus 3. Within these ranges, setting the ratio to 3 gives only (9,3) and (12,4). The resulting congruences, combined with s ≡ 1 mod 29, give seeds 1 and 1654 modulo 2233. This covers all Python integer seeds in the source formula, including negative seeds. Enumerating one period with the actual native builder functions independently recovered the same two classes. The right operands and balanced probe changes were calculated with exact rational gates.

| Seed residue | Grouping | Slope 2→3 | Slope 1→2 |
|---|---|---:|---:|
| 1 | B3 | −63 | 0 |
| 1 | B4 | −270 | −60 |
| 1654 | B3 | −48 | −8 |
| 1654 | B4 | −2941/8 | −741/8 |
| Two-prune input supplied to B4 | B4 | −63 | 3 |

The alternate seed preserves the left input and the outer gain while changing inner gates. It matches neither the two-prune intermediate operand nor its site-3 slope in B4. The B3 row at the default seed retains the known one-slope collision and differs at the second read. Thus the original program both generates and consumes a numerical response, with the cited two-prune branch input absent from its actual construction. A physical theory connecting an event to that response still needs an inherited operation that writes the relevant grade vector or selects the history.

The [registered test](CALLER_BINDING_PROTOCOL.md) fixes this source domain. [Exact replay](check_caller_binding.py) · [complete values and mask controls](evidence/caller_binding/result.json). The first local harness attempt failed on list indexing before finishing the witness check. Converting the copied branch collection to a NumPy array corrected that setup error. The replay invokes the original definitions from a pinned source, skipping module-level writes and unrelated computations.
