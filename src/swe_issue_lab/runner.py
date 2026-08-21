"""Run the scenario suite and write a machine-readable evaluation report."""

import argparse
import json
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from xml.etree import ElementTree


@dataclass(frozen=True, slots=True)
class EvaluationSummary:
    total: int
    passed: int
    failures: int
    errors: int
    skipped: int
    duration_seconds: float
    exit_code: int


def parse_junit_report(report_path: Path, *, exit_code: int) -> EvaluationSummary:
    root = ElementTree.parse(report_path).getroot()
    suites = [root] if root.tag == "testsuite" else list(root.findall("testsuite"))
    total = sum(int(suite.attrib.get("tests", "0")) for suite in suites)
    failures = sum(int(suite.attrib.get("failures", "0")) for suite in suites)
    errors = sum(int(suite.attrib.get("errors", "0")) for suite in suites)
    skipped = sum(int(suite.attrib.get("skipped", "0")) for suite in suites)
    duration = sum(float(suite.attrib.get("time", "0")) for suite in suites)
    passed = total - failures - errors - skipped
    return EvaluationSummary(
        total=total,
        passed=passed,
        failures=failures,
        errors=errors,
        skipped=skipped,
        duration_seconds=duration,
        exit_code=exit_code,
    )


def run_evaluation(*, output_path: Path, test_path: str = "tests") -> EvaluationSummary:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    junit_path = output_path.with_name("junit.xml")
    command = [
        sys.executable,
        "-m",
        "pytest",
        "-q",
        test_path,
        f"--junitxml={junit_path}",
    ]
    completed = subprocess.run(command, check=False)
    summary = parse_junit_report(junit_path, exit_code=completed.returncode)
    output_path.write_text(
        json.dumps(asdict(summary), indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"Evaluation: {summary.passed}/{summary.total} passed "
        f"({summary.duration_seconds:.3f}s)"
    )
    return summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run issue scenarios and write a JSON evaluation report."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("artifacts/evaluation-report.json"),
        help="Path for the JSON report",
    )
    parser.add_argument(
        "--tests",
        default="tests",
        help="Test directory or file to evaluate",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    summary = run_evaluation(
        output_path=arguments.output,
        test_path=arguments.tests,
    )
    return summary.exit_code
