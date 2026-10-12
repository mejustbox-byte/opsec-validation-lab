# Threat model and limits

Untrusted manifests and reports can contain malformed input, sensitive identifiers or misleading assertions. Strict loading, size/depth caps, exact manifest fields, basename-only evidence paths and exclusive output creation reduce common errors. The CLI emits generic errors and does not echo source content. It does not execute manifest content or retrieve URLs.

Residual risks include CPU/RAM use within bounded inputs, filesystem races, hardlinks, compromised runtime/dependencies, dishonest hashes/provenance and sensitive case identifiers. SHA-256 detects accidental byte changes only relative to the supplied manifest. Sanitization_reviewed is an assertion; a secret-bearing artifact with that flag remains secret-bearing. The tool neither approves publication nor anonymizes data.

Unavailable and invalid evidence are visible coverage gaps. An expected fail or not_tested status may legitimately match a scenario; passing LAB-001 only means the expected result was observed. Production readiness, security completeness and actual environment state cannot be inferred from the lab exit code.

[Index](index.md) · [Other language](../ru/limitations.md)
