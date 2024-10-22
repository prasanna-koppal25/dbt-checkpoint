import pytest

from dbt_checkpoint.check_source_has_tests_by_group import main

# Input schema, valid_manifest, input_args, expected return value
TESTS = (
    (
        """
sources:
-   name: test
    tables:
    -   name: test1
        description: test description
    """,
        True,
        ["--tests", "unique", "--test-cnt", "1"],
        0,
    ),
    (
        """
sources:
-   name: test
    tables:
    -   name: test2
        description: test description
    """,
        False,
        ["--tests", "unique", "--test-cnt", "1"],
        1,
    ),
    (
        """
sources:
-   name: test
    tables:
    -   name: test3
        description: test description
    """,
        True,
        ["--tests", "", "--test-cnt", "2"],
        1,
    ),
    (
        """
sources:
-   name: test
    tables:
    -   name: test4
        description: test description
    """,
        False,
        ["--tests", "unique_combination_of_columns", "--test-cnt", "2"],
        1,
    ),
)


@pytest.mark.parametrize(
    ("input_schema", "valid_manifest", "input_args", "expected_status_code"), TESTS
)
def test_check_source_has_tests(
    input_schema,
    valid_manifest,
    input_args,
    expected_status_code,
    manifest_path_str,
    tmpdir,
):
    if valid_manifest:
        input_args.extend(["--manifest", manifest_path_str])
    yml_file = tmpdir.join("schema.yml")
    yml_file.write(input_schema)
    status_code = main(argv=[str(yml_file), *input_args])
    assert status_code == expected_status_code
