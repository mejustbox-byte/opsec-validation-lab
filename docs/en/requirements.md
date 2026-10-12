# Requirements

The lab verifies a supplied normalized report against a scenario manifest. It never invokes an auditor, a collector, a shell command or a tenant API. Its purpose is to make expected results, versions and evidence class reviewable without presenting fixture success as infrastructure validation.

R1 requires exact result identity and status equality, including extra results. R2 requires producer name, version and ruleset equality plus declared platform and version. R3 requires the report synthetic flag to match the scenario class; live scenarios additionally require an execution identifier. R4 records a boolean manual sanitization-review declaration. R4 does not inspect whether secrets remain.

Acceptance includes positive and negative scenarios for each implemented assertion, malformed manifests, missing evidence, incorrect hashes, unavailable live scenarios, CLI exit codes and exclusive output creation. Reports must conform to opsec-1.0. Future collectors and live execution need separate designs and evidence.

[Index](index.md) · [Other language](../ru/requirements.md)
