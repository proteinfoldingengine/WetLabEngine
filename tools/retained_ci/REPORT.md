# Retained execution optimization results

{
  "commands": {
    "inherited": {
      "argv": [
        "/opt/hostedtoolcache/Python/3.11.16/x64/bin/python",
        "/home/runner/work/WetLabEngine/WetLabEngine/tools/retained_ci/run.py",
        "inherited",
        "out/science/inherited"
      ],
      "end_seconds": 63.43395392100001,
      "returncode": 0,
      "start_seconds": 0.000431568999999854
    },
    "science": {
      "argv": [
        "/opt/hostedtoolcache/Python/3.11.16/x64/bin/python",
        "/home/runner/work/WetLabEngine/WetLabEngine/ResearchHistory/UQCF-GEM/demos/v16.39-theorem-validation/run_campaign.py",
        "out/science/scientific"
      ],
      "end_seconds": 92.25587226700003,
      "returncode": 0,
      "start_seconds": 0.0002623889999995299
    }
  },
  "current_controls": 28,
  "fixture_benchmark": {
    "baseline_generations": 12,
    "baseline_producer_seconds": 119.90624646399998,
    "baseline_seconds": 149.06712731500002,
    "limitation": "single paired run; optimized suite shares CPU with concurrent science",
    "optimized_generations": 2,
    "optimized_producer_seconds": 20.42997194000003,
    "optimized_seconds": 49.49387750399998,
    "ratio": 3.0118296410086836,
    "same_runner": true,
    "verifier_calls_each": 12
  },
  "inherited_tests": 261,
  "parallel_phase_seconds": 92.25639624300001,
  "scientific_bytes_identical": true
}

All289 scientific controls/inherited tests run unchanged in every phase; independent verification remains uncached. Additional infrastructure controls run before expensive work. Fresh publication scientific bytes match the certified v16.39 parent and the new scientific execution. Source/API/ZIP/member/hash checks are automated and fail closed.

These are measured single-run timings, not guaranteed speedups. Publication completion still requires an actual-merge replay and its verified receipt before infrastructure closure.
