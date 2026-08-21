# SWE Issue Evaluation Lab

[![Evaluation](https://github.com/deepak56738/swe-issue-evaluation-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/deepak56738/swe-issue-evaluation-lab/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-3776AB.svg)](https://www.python.org/)
[![pytest](https://img.shields.io/badge/tests-pytest-0A9EDC.svg)](https://docs.pytest.org/)
[![Docker](https://img.shields.io/badge/docker-ready-2496ED.svg)](Dockerfile)
[![license-MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A reproducible software engineering evaluation project built around realistic
GitHub issues, focused regression tests, small fixes, and machine-readable test
reports.

The target package contains webhook reliability utilities for signature
verification, retry scheduling, and event routing. Each evaluation case follows
the same issue-to-fix contract used in day-to-day repository maintenance.

## Highlights

- Three closed defect reports with focused regression tests
- Separate reviewed pull request for every issue
- 38 deterministic evaluation cases with 100% branch coverage
- JSON and JUnit report generation from a single command
- Ruff, strict mypy, and Python 3.11–3.13 test matrix
- Non-root Docker image that executes the complete evaluation suite

## Evaluation workflow

```text
Issue report → reproduce with a focused test → implement the fix
    → run quality gates → review the patch → close the issue
```

## Completed cases

| Issue | Regression evidence | Fix |
| --- | --- | --- |
| [Malformed signature headers](https://github.com/deepak56738/swe-issue-evaluation-lab/issues/1) | Invalid headers now return `False` instead of raising | [PR #7](https://github.com/deepak56738/swe-issue-evaluation-lab/pull/7) |
| [Retry base-delay off-by-one](https://github.com/deepak56738/swe-issue-evaluation-lab/issues/2) | Attempts one through four verify the documented sequence | [PR #8](https://github.com/deepak56738/swe-issue-evaluation-lab/pull/8) |
| [Wildcard namespace leakage](https://github.com/deepak56738/swe-issue-evaluation-lab/issues/4) | Neighboring event names are rejected at the delimiter boundary | [PR #9](https://github.com/deepak56738/swe-issue-evaluation-lab/pull/9) |

## Run the evaluation

```bash
uv sync --extra dev
uv run evaluate-scenarios
```

The command runs the scenario suite and writes:

```text
artifacts/
├── evaluation-report.json
└── junit.xml
```

## Run with Docker

```bash
docker build -t swe-issue-evaluation-lab .
docker run --rm swe-issue-evaluation-lab
```

## Quality checks

```bash
make check
```

## Project structure

```text
swe-issue-evaluation-lab/
├── src/swe_issue_lab/       # Target package and report runner
├── tests/                   # Baseline and regression scenarios
├── docs/                    # Evaluation contract and case notes
├── .github/ISSUE_TEMPLATE/  # Structured defect reports
├── Dockerfile               # Reproducible evaluation environment
└── .github/workflows/       # Tests, quality gates, and Docker run
```

See [docs/evaluation-contract.md](docs/evaluation-contract.md) for the pass/fail
contract.

## License

Released under the [MIT License](LICENSE).
