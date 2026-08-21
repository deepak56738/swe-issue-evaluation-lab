import json
import subprocess
from pathlib import Path

import pytest

from swe_issue_lab import runner

JUNIT_XML = """<?xml version="1.0" encoding="utf-8"?>
<testsuites>
  <testsuite tests="5" failures="1" errors="0" skipped="1" time="0.125" />
</testsuites>
"""

SINGLE_SUITE_XML = """<?xml version="1.0" encoding="utf-8"?>
<testsuite tests="2" failures="0" errors="0" skipped="0" time="0.025" />
"""


def test_parses_junit_summary(tmp_path: Path) -> None:
    report = tmp_path / "junit.xml"
    report.write_text(JUNIT_XML, encoding="utf-8")

    summary = runner.parse_junit_report(report, exit_code=1)

    assert summary.total == 5
    assert summary.passed == 3
    assert summary.failures == 1
    assert summary.errors == 0
    assert summary.skipped == 1
    assert summary.duration_seconds == 0.125
    assert summary.exit_code == 1


def test_parses_single_suite_root(tmp_path: Path) -> None:
    report = tmp_path / "junit.xml"
    report.write_text(SINGLE_SUITE_XML, encoding="utf-8")

    summary = runner.parse_junit_report(report, exit_code=0)

    assert summary.total == 2
    assert summary.passed == 2
    assert summary.duration_seconds == 0.025


def test_runs_pytest_and_writes_json_report(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def fake_run(command: list[str], *, check: bool) -> subprocess.CompletedProcess:
        junit_argument = next(
            value for value in command if value.startswith("--junitxml=")
        )
        Path(junit_argument.split("=", maxsplit=1)[1]).write_text(
            JUNIT_XML,
            encoding="utf-8",
        )
        return subprocess.CompletedProcess(command, returncode=1)

    monkeypatch.setattr(runner.subprocess, "run", fake_run)
    output = tmp_path / "reports" / "summary.json"

    summary = runner.run_evaluation(output_path=output, test_path="scenario-tests")

    assert summary.exit_code == 1
    assert json.loads(output.read_text(encoding="utf-8"))["passed"] == 3
    assert "Evaluation: 3/5 passed" in capsys.readouterr().out


def test_main_returns_evaluation_exit_code(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    expected = runner.EvaluationSummary(1, 1, 0, 0, 0, 0.01, 0)

    def fake_evaluation(
        *,
        output_path: Path,
        test_path: str,
    ) -> runner.EvaluationSummary:
        assert output_path == tmp_path / "result.json"
        assert test_path == "tests/test_retry.py"
        return expected

    monkeypatch.setattr(runner, "run_evaluation", fake_evaluation)

    result = runner.main(
        [
            "--output",
            str(tmp_path / "result.json"),
            "--tests",
            "tests/test_retry.py",
        ]
    )

    assert result == 0
