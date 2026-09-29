# v16.23 publication-only correction

First publication run36571592480, job109416676142, at f7043bfa7263e3454df6d23800c15583a1ab93d2 failed before downloading evidence or rerunning the science. The helper expected an actions/ prefix but its fixed callers supplied paths relative to actions. The guard correctly stopped the request, and no evidence commit was made. The always-upload step also failed because there were no files yet; no artifact is claimed for that attempt. Its exact run/job logs are preserved by the corrected publisher.

The corrected API-path function validates a narrow set of Actions subpaths and inserts the repository/actions prefix exactly once. Two packaging regression tests cover all required endpoint forms and reject external, traversal, unrelated and query-bearing forms. These are publication utility tests, separate from the82 scientific/inherited tests.

No scientific module, mathematical input, proof, verifier, or certificate was changed. The corrected publication must freshly reproduce and hash-check all scientific output before committing. This failed packaging run is not relabeled a scientific GREEN or omitted from publication provenance.
