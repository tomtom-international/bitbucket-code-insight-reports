"""
Module which generates a report based on the output of git diff
"""
import re
import os

from .report import Report


class GitDiffReport(Report):
    """
    Class to generate a report based on the output of git diff
    """

    def __init__(
        self, auth, base_url, project_key, repo_slug, commit_id, key, title, description, file_name, force_pass=False
    ):
        # If there weren't any changes, then its a pass
        if os.stat(file_name).st_size == 0:
            result = "PASS"
            return_code = 0
        else:
            result = "FAIL"
            return_code = 1

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
            return_code=return_code,
            file_name=file_name,
            force_pass=False,
        )

    def _process_annotations(self, annotations_string):
        """
        Converts `git diff` output to an annotations dictionary.
        Args:
            annotations_string: git diff output to parse
        Returns:
            Dictionary with the annotations.
        """
        annotations = []

        if annotations_string:
            # Split on the diff output pattern
            split_output = re.compile(r"(diff --git.*(.*\n){4})").split(annotations_string)
            for file_errors_counter in range(1, len(split_output), 3):
                path = split_output[file_errors_counter + 1][6:-1]

                entries = re.compile(r"(@{2}[\+\-\,\d\ ]*@{2})").split(split_output[file_errors_counter + 2])

                for error_counter in range(1, len(entries), 2):
                    line_number = entries[error_counter].split(" ")[1][1:].split(",")[0]
                    error = "{title}: Error found starting here.".format(title=self.title)

                    annotations.append({"path": path, "line": line_number, "message": error, "severity": "HIGH"})

        return {"annotations": annotations}
