import re

from .report import Report

class GitDiffReport(Report):
    def __init__(self, auth, base_url, project_key, repo_slug, commit_id, key, title, description, file_name):
        with open(file_name, mode="r") as diff_file:
            annotations_string = diff_file.read()

        # If there weren't any changes, then its a pass
        if annotations_string == "":
            result = "PASS"
            return_code = 0
        else:
            result = "FAIL"
            return_code = 1

        super().__init__(auth, base_url, project_key, repo_slug, commit_id, key, title, description, result, annotations_string, return_code)

    def _process_annotations(self, annotations_string):
        """
        Converts `git diff` output to an annotations dictionary.
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
                    line_number = entries[error_counter].split(' ')[1][1:].split(',')[0]
                    error = "{title}: Error found starting here.".format(title=self.title)

                    annotations.append({
                        "path": path,
                        "line": line_number,
                        "message": error,
                        "severity": "HIGH"
                    })

        return {'annotations': annotations}