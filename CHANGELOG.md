# Changelog

All notable changes to this project are documented in this file.

## 1.0.0 - 2026-08-21

### Added

- Reproducible issue evaluation command with JSON and JUnit reports
- Webhook signature, retry scheduling, and event routing scenarios
- Structured GitHub issue template and evaluation contract
- Python version matrix, static analysis, coverage, and Docker execution jobs

### Fixed

- Return `False` for malformed SHA-256 signature headers
- Start retry backoff at the configured base delay
- Keep wildcard event routes inside their dot-delimited namespace
