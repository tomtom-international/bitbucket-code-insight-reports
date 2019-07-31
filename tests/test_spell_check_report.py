import pytest

from unittest.mock import patch
from hypothesis import strategies as strat, given, example

from bitbucket_code_insight_reports.spell_check_report import SpellCheckReport


@pytest.fixture
def gen_scspell_annotation():
    """
    Generates scspell annotions
    Args:
        locations: list of path, line number and word tuples (path, line, word)
    Returns:
        annotations_dict: formatted dictionary of annotations
        annotations_str: scspell output
    """

    def _gen_scspell_annotation(results):
        dicts = {"annotations": []}
        strs = []
        for result in results:
            dicts["annotations"].append(
                {
                    "path": result[0],
                    "line": str(result[1]),
                    "message": "'{word}' not found in dictionary (from token '{word}')".format(
                        path=result[0], line=result[1], word=result[2]
                    ),
                    "severity": "LOW",
                }
            )
            strs.append(
                "{path}:{line}: '{word}' not found in dictionary (from token '{word}')".format(
                    path=result[0], line=result[1], word=result[2]
                )
            )
        return dicts, "\n".join(strs)

    return _gen_scspell_annotation


@patch("bitbucket_code_insight_reports.spell_check_report.StringIO")
@patch("bitbucket_code_insight_reports.spell_check_report.spell_check")
@given(word=strat.text(min_size=1, alphabet=strat.characters(blacklist_categories=("C"))))
@example(word=":")
@example(word="silly:example:to:check")
def test_init(word, mock_spellcheck, mock_stringio, gen_scspell_annotation):
    """
    Tests the init function runs scspell and processes the results
    """
    test_annotations, scspell_output = gen_scspell_annotation([("test/file.cpp", 5, word), ("file3.cpp", 18, word)])
    mock_spellcheck.return_value = False
    mock_stringio.return_value.getvalue.return_value = scspell_output
    test_report = SpellCheckReport(
        "test",
        "test.coam",
        "test",
        "test",
        "test",
        "test",
        "test",
        "test",
        files_to_check=["test/file.cpp", "file3.cpp"],
    )

    assert mock_spellcheck.called_with(["test/file.cpp", "file3.cpp"], report_only=True, base_dicts=None)

    assert test_report.result == "FAIL"
    assert test_report.annotations == test_annotations
