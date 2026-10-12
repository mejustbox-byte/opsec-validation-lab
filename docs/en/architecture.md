# Architecture

The CLI loads a bounded strict JSON manifest using the report-contract loader. Manifest validation rejects unknown keys, duplicate case IDs, duplicate expected identities, unsupported statuses and nested or absolute report paths. Each report is a single JSON filename in the manifest directory. Up to 256 cases and 10,000 expected identities per case are accepted; each JSON input is bounded to 8 MiB and depth 64 by the dependency.

The evaluator validates the normalized report and verifies the supplied SHA-256 against its bytes. A second parse is compared with the loaded object to detect differing content between reads. This reduces inconsistent observations but does not provide a race-free sandbox. Parent symlinks are rejected; hardlinks, concurrent replacement and privileged attackers remain outside the guarantee.

Output contains an opsec-1.0 assessment and a small case catalog. Raw report paths, producer evidence and messages are not copied. Case IDs and suite ID remain user-supplied and can disclose information. The lab assessment itself is marked synthetic because it assesses supplied declarations. This flag does not overwrite individual case classifications in the catalog.

[Index](index.md) · [Other language](../ru/architecture.md)
