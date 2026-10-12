# OPSEC Validation Lab

Install Python 3.12+ and bootstrap the exact released contract wheel. Initial installation needs network; verification runs locally. Output filenames must not exist. The first verification returns 0; the unexecuted live example writes output and returns 2. Code 1 means an assertion mismatch; 3 means malformed input or unavailable output. These are lab assertion codes, not infrastructure assurance.

```bash
python -m pip install -r requirements-bootstrap.txt
python -m pip install .
opsec-lab check-manifest examples/suite.synthetic.json
opsec-lab verify examples/suite.synthetic.json --observed-at 2026-10-12T00:00:00Z --output result.json
opsec-lab verify examples/live-unexecuted.json --observed-at 2026-10-12T00:00:00Z --output live-result.json
```

[Documentation](docs/en/index.md)

Alpha 0.1.0a1. Nineteen test methods passed on Linux/macOS; Windows passed eighteen with the FIFO-specific test skipped. Eleven bilingual documentation pairs and clean wheel installation passed on all three operating systems with Python 3.13. No live environment tested.
