# Evaluation contract

Every issue scenario must include four pieces of evidence:

1. A concise issue report with reproduction steps and expected behavior.
2. A focused regression test that fails before the patch.
3. The smallest implementation change that satisfies the stated behavior.
4. A green repository-wide quality and test run after the fix.

## Pass criteria

A patch passes when all of the following are true:

- the regression test for the reported defect passes;
- all existing tests continue to pass;
- Ruff and strict mypy checks succeed;
- branch coverage remains at or above 95%;
- the Docker evaluation command exits with status `0`;
- the JSON report records no failed or errored cases.

## Report schema

`evaluate-scenarios` writes a JSON object with these fields:

| Field | Meaning |
| --- | --- |
| `total` | Number of collected cases |
| `passed` | Cases that completed successfully |
| `failures` | Assertion failures |
| `errors` | Setup or execution errors |
| `skipped` | Cases not executed |
| `duration_seconds` | Test duration from the JUnit report |
| `exit_code` | Exit status returned by pytest |
