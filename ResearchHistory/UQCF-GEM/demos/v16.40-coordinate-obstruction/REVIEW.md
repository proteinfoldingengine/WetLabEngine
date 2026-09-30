# Independent review before execution

A fresh source-only reviewer checked PREREGISTRATION.md, THEOREM.md, producer.py, verifier.py and the scientific controls. No numerical work was run locally. The reviewer found the branch-rigidity and projection proof sound, including the general-r lower bound, matching serial swaps, independent scalar and LEX bounds, and incidence-Hamming shortest-path argument. The two enumeration methods, edge reconstruction, partitions, exhaustive pair identities, paths and cuts were judged sound.

One closure issue was identified: an alternate valid unit path could establish the endpoint obstruction even if the frozen named candidate failed. The gate now separately requires named candidate validity and its shortest-path check before certifying the predicted witness outcome. A distinct control passes a matching but illegal named candidate to ensure legality is checked, not merely equality with preregistered bytes. Contrary outcomes remain reportable.

Pipeline and artifact closure review is required before merge; numerical counts remain unverified until GitHub execution.

## Pipeline review and resolutions
The fresh reviewer checked integrity.py, run.py, run_campaign.py, publish.py, test_integrity.py and the workflow. Artifact/API/source/merge bindings were coherent. The parent optimized-fixture reference is now explicitly anchored and retained as an input. Coverage is checked against every retained suite record and passing log, both RED controls, command exit statuses and uncached fixture-verifier coverage. All source inputs additionally match their Git HEAD blob identities before packaging. The inherited manifest contains v16.39/inherited.txt and the three v16.38 canonical scientific inputs. No other blocking defect or new performance bottleneck was found. Numerical results and actual downloaded artifacts require separate inspection.
