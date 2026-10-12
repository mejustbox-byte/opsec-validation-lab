# Manifest lab-1.0

A manifest has exactly schema_version, suite_id and cases. Each case has id, kind, report, sha256, producer, expected and provenance. Kind is synthetic or live. Report and hash are both populated or both empty; empty evidence is allowed so an unexecuted live scenario can be represented honestly.

Producer contains name, version and ruleset. Expected is a nonempty list of check_id, asset_id and status records. Pair identities must be unique. Matching compares the entire actual result map with the entire expected map; missing and unexpected actual results both fail LAB-001. A not_tested expected status can match: the assertion passes, while the original report still declares an untested check. Lab success is therefore not auditor success.

Provenance contains platform, platform_version, execution_id and sanitization_reviewed. These are supplied declarations, not independently collected facts. Empty platform declarations fail LAB-002 when evidence exists. A live execution ID is required to avoid LAB-003 not_tested. A false review flag leaves LAB-004 not_tested. No signatures, timestamps or execution-log verification are supplied by this manifest.

[Index](index.md) · [Other language](../ru/manifest.md)
