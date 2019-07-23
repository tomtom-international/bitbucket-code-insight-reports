from unittest.mock import patch, mock_open

import pytest

from bitbucket_code_insight_reports.git_diff_report import GitDiffReport


@pytest.fixture
def gen_get_diff_annotation():
    """
    Generates git_diff annotions
    Args:
        locations: list of path and line number tuples (path, line)
    Returns:
        annotations_dict: formatted dictionary of annotations
        annotations_str: git diffstyle output
    """

    def _gen_get_diff_annotation(locations, title):
        dicts = {"annotations": []}
        strs = []
        for loc in locations:
            dicts["annotations"].append(
                {
                    "path": loc[0],
                    "line": str(loc[1]),
                    "message": "{title}: Error found starting here.".format(title=title),
                    "severity": "HIGH",
                }
            )
            strs.append(
                """
diff --git a/{path}
index commitone..committwo 100644
--- a/{path}
+++ b/{path}
@@ -{line},7 +{line},8 @@ public final class SecondChangedClass extends UnchangedClass
         return null;
                """.format(
                    path=loc[0], line=loc[1]
                )
            )
        return dicts, "\n".join(strs)

    return _gen_get_diff_annotation


def test_init(gen_get_diff_annotation):
    """
    Tests the init function handles git diff input correctly
    """
    test_annotations, diff_output = gen_get_diff_annotation(
        [("test/some/class.c", 5), ("test/some/other/class.c", 146)], "Git Report"
    )

    with patch("os.stat") as mock_stat:
        mock_stat.return_value.st_size = 32
        with patch("builtins.open", mock_open(read_data=diff_output)) as mock_file:
            test_report = GitDiffReport(
                "test", "test.coam", "test", "test", "test", "test", "Git Report", "test", "test.txt"
            )

    assert test_report.result == "FAIL"
    assert test_report.annotations == test_annotations
