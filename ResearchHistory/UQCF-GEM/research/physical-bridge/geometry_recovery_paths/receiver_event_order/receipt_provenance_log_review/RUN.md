# Custody verification and original publication archive

The [source trace and replay](../receipt_provenance_log/RESULT.md) were frozen at f64e414a36671f37f745a2b4f42d5187d0637649. The original [historical publication ZIP](historical-publication.zip) was fetched from official GitHub Actions artifact 11060037308 of [run 36626045181](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36626045181). Its 1,134,963 bytes matched GitHub's SHA-256 3bca38711fc59c27a614536ee28fdc7b690902f0cabe8544d3729a1406e84b78. Both retained copies of the historical process log in that ZIP matched the replay. Every one of its 25 evidence-manifest entries verified. The [archive check](verify_historical_zip.py) takes the ZIP and pinned checkout as arguments. Its [result](historical_archive_check.json) records the original execution SHA and log digest.

Both contemporary runs passed the historical replay and the inherited foundation. The [first review](first/review.txt) in [run 45915772087](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/45915772087) returned DERIVED for the program, OPEN for the participant bridge and an explanatory sentence in its verdict field. The repository's required enum rejected that response. The source audit was skipped by that job and its original partial evidence is archived below.

A second request specified the permitted verdict tokens in the question. The science and validator were unchanged. In [run 45915964042](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/45915964042) at 54c79a4dbbc5a26c305afdaf4ec2b6f76b569d76, Gemini returned ACCEPTED, DERIVED and OPEN. The [verbatim response](review.txt) and [source-bound audit](publication_audit.json) match the original response and pinned inputs. Both jobs passed. Local and hosted results matched. The original archives below matched GitHub's digests and passed ZIP and available checksum-manifest verification.

| Original archive | Bytes | SHA-256 |
| --- | ---: | --- |
| [First receipt-custody-foundation](first/receipt-custody-foundation.zip) | 307,060 | `d9f7cb0ebdec9deb4860f8c0604624c3bda80b693871e43e784250eb7944dabb` |
| [First receipt-custody-review](first/receipt-custody-review.zip) | 48,050 | `52f4c9beeb537a70e62ca4e5b729d2c85df991611b2d5aa9e309e09998040b2f` |
| [Second receipt-custody-review](receipt-custody-review.zip) | 72,512 | `81024e05b13b8ac348935e9891018d012605cc31a5c7866af7a8b4393a48bb90` |
| [Second receipt-custody-foundation](receipt-custody-foundation.zip) | 307,063 | `c6172fea32ab63451df255fcb68c73f316fe5721866455ef853eea6a19b12e02` |
