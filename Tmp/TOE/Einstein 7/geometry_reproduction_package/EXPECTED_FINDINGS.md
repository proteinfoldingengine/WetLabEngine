# Expected Findings

The exact numeric values may vary by Python installation, available stdlib files, and platform.

The expected pattern is:

```text
synthetic_direct_geometry_internally_passed
import_dependency_fine_path_not_closed OR related not_closed result
function_call_fine_path_not_closed OR related not_closed result
function_call_triadic_grammar_not_closed OR related not_closed result
```

If empirical software graph branches pass unexpectedly, inspect whether the graph extraction created a very small or unusual graph.
