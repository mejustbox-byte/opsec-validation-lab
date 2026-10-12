# ADR-001: offline Python consumer

Accepted for this alpha: Python 3.12+, JSON manifests, unittest and the released opsec-report-contract 0.1.0a1. Reusing the contract avoids an independent implementation of statuses, coverage and report validation. The runtime dependency is exact; installation bootstraps the verified GitHub wheel because this release is not on PyPI.

The bootstrap requirement includes the published wheel SHA-256. This establishes byte consistency with that release, not developer trust or resistance to a compromised dependency chain. Build tooling is pinned to setuptools 84.0.0 and wheel 0.48.0. CI runs Python 3.13 on three operating systems; local checks also exercise 3.12.

Rejected for this alpha: arbitrary command runners, YAML with application tags, remote artifact URLs in manifests and embedded credentials. They would introduce execution and credential handling beyond an offline evidence consumer. VM/tenant provisioning and real-auditor orchestration remain future integrations rather than hidden behavior.

[Index](index.md) · [Other language](../ru/adr.md)
