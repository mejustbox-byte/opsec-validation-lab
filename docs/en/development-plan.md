# Development plan

Alpha implements an offline manifest consumer and four assertion checks. It consumes opsec-1.0; it does not run platform auditors. The acceptance matrix is exercised with synthetic fixtures and an explicitly unexecuted live case.

Next milestones are independently reviewed live-scenario catalogs, documented adapter coverage for existing auditors, evidence-signature verification and optional isolated orchestration. Each integration needs producer/version compatibility tests and positive, negative and unavailable scenarios. None is enabled implicitly.

Do not expand the meaning of pass when adding integrations: missing evidence stays not_tested and matching an expected failure remains only a successful assertion. Real-lab claims require private execution evidence and reviewable metadata; public fixtures remain synthetic.

[Index](index.md)
