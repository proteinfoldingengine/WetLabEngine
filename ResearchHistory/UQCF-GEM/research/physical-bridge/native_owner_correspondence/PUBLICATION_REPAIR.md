# Publication-only packaging correction

The verified run 41540085233 produced a 118,205,941-byte original verification ZIP containing a 118,089,388-byte source-snapshot ZIP. The verification, independent review and fresh publication replay jobs succeeded. The original archive push was rejected by GitHub because both ZIPs exceed its 100-MB per-file limit; job 125604331291 records the failure.

The original scientific argument and execution c721762f4890a81036fb2bff11d394881384496f are unchanged. This separate workflow performs no science and no Gemini request. It downloads the original artifacts, checks API digests and every original member manifest, stores any large original ZIP in ordered 40-MiB chunks, and preserves large extracted members by exact references into that original ZIP rather than duplicating their bytes. Reconstruction recipes include original byte counts and SHA-256. It preserves every completed original-job log, including the archive failure, and verifies remote commit readback of all stored files.

This is a packaging correction only. The original workflow's overall conclusion remains failure due to the archive job; the separate repair result must be reported alongside it. Prior review is not rebound to changed scientific content.
