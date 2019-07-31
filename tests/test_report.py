import pytest
import json

from hypothesis import strategies as strat, given

from bitbucket_code_insight_reports.report import Report


@pytest.fixture
def gen_annotations():
    """
    Generates an annotations dict with a single object
    """

    def _gen_annotations(path, line, message, severity="HIGH"):
        annotations = {"annotations": [{"path": path, "line": line, "message": message, "severity": severity}]}
        return annotations

    return _gen_annotations


@given(
    auth=strat.text(min_size=1, alphabet=strat.characters(blacklist_categories=("C"))),
    base_url=strat.text(min_size=1, alphabet=strat.characters(blacklist_categories=("C"))),
    project_key=strat.text(min_size=1, alphabet=strat.characters(blacklist_categories=("C"))),
    repo_slug=strat.text(min_size=1, alphabet=strat.characters(blacklist_categories=("C"))),
    commit_id=strat.text(min_size=1, alphabet=strat.characters(blacklist_categories=("C"))),
    key=strat.text(min_size=1, alphabet=strat.characters(blacklist_categories=("C"))),
    title=strat.text(min_size=1, alphabet=strat.characters(blacklist_categories=("C"))),
    description=strat.text(min_size=1, alphabet=strat.characters(blacklist_categories=("C"))),
    path=strat.text(min_size=1, alphabet=strat.characters(blacklist_categories=("C"))),
    line=strat.integers(min_value=0),
    message=strat.text(min_size=1, alphabet=strat.characters(blacklist_categories=("C"))),
)
def test_init(
    auth, base_url, project_key, repo_slug, commit_id, key, title, description, path, line, message, gen_annotations
):
    result = "PASS"
    test_annotation = gen_annotations(path, line, message)
    test_annotation_string = json.dumps(test_annotation)

    test_report_url = (
        base_url
        + "/rest/insights/1.0/projects/"
        + project_key
        + "/repos/"
        + repo_slug
        + "/commits/"
        + commit_id
        + "/reports/"
        + key
    )

    test_report = Report(
        auth, base_url, project_key, repo_slug, commit_id, key, title, description, result, test_annotation_string
    )

    assert test_annotation == test_report.annotations
    assert auth == test_report.auth
    assert test_report_url == test_report.url
    assert title == test_report.title
    assert description == test_report.description
    assert result == test_report.result

    report_info = "\nURL: {url}\n".format(url=test_report_url)
    report_info += "Title: {title}\n".format(title=title)
    report_info += "Description: {desc}\n".format(desc=description)
    report_info += "Result: {result}\n".format(result=result)
    report_info += "Annotations: {annot}\n".format(annot=json.dumps(test_annotation, indent=4, sort_keys=True))
    assert report_info == test_report.output_info()


def test_force_pass(gen_annotations):
    """
    Ensure that using `force_pass` in initialization will make everything return passing
    """
    test_report = Report(
        "test",
        "test",
        "test",
        "test",
        "test",
        "test",
        "test",
        "test",
        False,
        json.dumps(gen_annotations("/test", 3, "test")),
        return_code=1,
        force_pass=True,
    )
    assert test_report.result == "PASS"
    assert test_report.return_code == 0
