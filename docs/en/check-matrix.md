# Check matrix

| ID | Passing assertion | Negative/unavailable case | Limit |
|---|---|---|---|
| LAB-001 | Exact identity/status map | Changed status, missing or extra identity | No accuracy claim beyond supplied expectations |
| LAB-002 | Exact producer and populated platform | Version mismatch or empty platform | Platform is declared |
| LAB-003 | Matching evidence class | Synthetic/live mismatch; missing live execution ID | No proof execution occurred |
| LAB-004 | Manual review flag true | False flag remains not_tested | No automated sanitization |

Invalid evidence leaves all four checks not_tested; it never produces a pass. A malformed manifest is a command error and produces no assessment. Failure takes precedence over incomplete coverage in the assessment exit code. The catalog distinguishes invalid_evidence from unavailable without copying raw parser errors.

The unit matrix covers positive assertions, status/identity mismatches, version/platform changes, evidence-class conflict, missing execution, absent review, digest mismatch, malformed JSON, traversal, duplicate IDs, invalid types and output collision. It does not establish real AD, cloud, network or recovery behavior.

[Index](index.md) · [Other language](../ru/check-matrix.md)
