# Independent review before execution

A fresh source-only reviewer checked PREREGISTRATION.md, THEOREM.md, producer.py, verifier.py and the scientific controls. No numerical work was run locally. The reviewer found the branch-rigidity and projection proof sound, including the general-r lower bound, matching serial swaps, independent scalar and LEX bounds, and incidence-Hamming shortest-path argument. The two enumeration methods, edge reconstruction, partitions, exhaustive pair identities, paths and cuts were judged sound.

One closure issue was identified: an alternate valid unit path could establish the endpoint obstruction even if the frozen named candidate failed. The gate now separately requires named candidate validity and its shortest-path check before certifying the predicted witness outcome. A distinct control passes a matching but illegal named candidate to ensure legality is checked, not merely equality with preregistered bytes. Contrary outcomes remain reportable.

Pipeline and artifact closure review is required before merge; numerical counts remain unverified until GitHub execution.
