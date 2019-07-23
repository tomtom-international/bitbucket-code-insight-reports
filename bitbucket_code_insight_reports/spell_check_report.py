"""
Spell checks files using scspell - https://github.com/myint/scspell/ - and reports the results to BitBucket Server Code Insights
"""
from contextlib import redirect_stderr
from io import StringIO

from scspell import spell_check

from .report import Report


class SpellCheckReport(Report):
    """
    Executes scspell and converts the results into a report for BitBucket Server Code Insights
    """

    def __init__(
        self,
        auth,
        base_url,
        project_key,
        repo_slug,
        commit_id,
        key,
        title,
        description,
        files_to_check,
        dictionary=None,
    ):  # pylint: disable=too-many-locals
        results = StringIO()

        with redirect_stderr(results):
            return_code = spell_check(files_to_check, report_only=True, override_dictionary=dictionary)

        annotations_string = results.getvalue().strip()

        if return_code:
            result = "PASS"
        else:
            result = "FAIL"

        super().__init__(
            auth,
            base_url,
            project_key,
            repo_slug,
            commit_id,
            key,
            title,
            description,
            result,
            annotations_string=annotations_string,
        )

    @staticmethod
    def _process_annotations(annotations_string):
        """
        Converts the output from scspell to an annotations dictionary.
        Args:
            annotations_string: scspell output to parse
        Returns:
            Dictionary with the annotations.
        """
        annotations = []

        if annotations_string != "":
            for issue in annotations_string.split("\n"):
                issue = issue.split(":")
                annotations.append(
                    {"path": issue[0].strip(), "line": issue[1].strip(), "message": issue[2].strip(), "severity": "LOW"}
                )
        return {"annotations": annotations}
