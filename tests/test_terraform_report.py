import pytest
import json
from unittest.mock import patch, mock_open, call, Mock

from hypothesis import strategies as strat, given

from bitbucket_code_insight_reports.terraform_report import TerraformReport


@pytest.fixture
def gen_terraform_annotation():
    """
    Generates terraform annotions
    Args:
        locations: list of path and line number tuples (path, line)
    Returns:
        annotations_dict: formatted dictionary of annotations
        annotations_str: terraform fmt style output
    """

    def _gen_terraform_annotation(locations):
        dicts = {"annotations": []}
        strs = []
        for loc in locations:
            dicts["annotations"].append(
                {
                    "path": loc[0],
                    "line": str(loc[1]),
                    "message": "Error found in this block. Run `terraform fmt --diff -check` to see the issue (or run without `-check` to fix automatically)",
                    "severity": "HIGH",
                }
            )
            strs.append(
                """
{path}
--- old/{path}
+++ new/{path}
@@ -{line},14 +{line},14 @@
- bad format
+ good format
                """.format(
                    path=loc[0], line=loc[1]
                )
            )
        return dicts, "\n".join(strs)

    return _gen_terraform_annotation


@patch("bitbucket_code_insight_reports.terraform_report.Terraform.cmd")
def test_init(mock_terraform, gen_terraform_annotation):
    """
    Tests the init function runs terraform fmt and processes the results
    """
    test_annotations, diff_output = gen_terraform_annotation(
        [("test/infra/main.tf", 5), ("test/infra/provider.tf", 146)]
    )
    mock_terraform.return_value = (0, diff_output, "")
    test_report = TerraformReport("test", "test.coam", "test", "test", "test", "test", "test", "test")

    assert test_report.result == "PASS"
    assert test_report.annotations == test_annotations
