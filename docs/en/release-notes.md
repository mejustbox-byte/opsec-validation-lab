# Alpha 0.1.0a1

Implements bounded lab-1.0 manifests, exact result/status matching, producer/platform declarations, synthetic/live classification and manual privacy-review attestations. Results include an opsec-1.0 assessment and a compact case catalog. The CLI never invokes manifest commands.

Nineteen test methods cover assertions, unavailable evidence, invalid input, special files, budgets and exclusive output creation. FIFO is unavailable on Windows and its test is skipped there; this is platform-specific evidence, not a cross-platform FIFO guarantee. Local Linux/Python 3.12 and clean wheel installation are verified. Hosted CI status is recorded separately.

Known limits: no actual auditor execution, live-environment validation, provenance authentication or automatic sanitization. Initial installation uses the separately released contract wheel with its published hash. PyPI publication is not included. This prerelease is not production-ready.

[Index](index.md)

Hosted CI run 38225486183 passed on a577778eb851ee59c03669bde0244d6494b92b3c. Windows skips only the FIFO test. All three platforms completed documentation and installed-wheel verification.
