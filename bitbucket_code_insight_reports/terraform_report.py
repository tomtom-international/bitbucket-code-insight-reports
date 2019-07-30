"""
Module for generating reports based on terraform
"""
import re

from python_terraform import Terraform

from .report import Report


class TerraformReport(Report):
    """
    Executes `terraform fmt` and converts the results into a report for BitBucket Server Code Insights
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
        file_name=None,
        force_pass=False,
    ):  # pylint: disable=too-many-locals
        annotations_string = ""
        if file_name is None:
            terraform = Terraform()
            return_code, annotations_string, error = terraform.fmt(  # pylint: disable=unused-variable
                capture_output=True, check=True, diff=True, recursive=True
            )

        if return_code == 0:
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
            return_code=return_code,
            force_pass=force_pass,
        )

    @staticmethod
    def _process_annotations(annotations_string):
        """
        Converts the output of `terraform fmt --diff -check` to an annotations dictionary.
        Args:
            annotations_string: terraform output to parse
        Returns:
            Dictionary with the annotations.
        """
        annotations = []

        if annotations_string:
            # Split on the diff output pattern
            split_output = re.compile(r"(.*\n-{3}.*\n\+{3}.*)").split(annotations_string)
            for file_errors_counter in range(1, len(split_output), 2):
                path = split_output[file_errors_counter].split("\n")[0]

                entries = re.compile(r"(@{2}[\+\-\,\d\ ]*@{2})").split(split_output[file_errors_counter + 1])

                for error_counter in range(1, len(entries), 2):
                    line_number = entries[error_counter].split(" ")[1][1:].split(",")[0]
                    error = "Error found in this block. Run `terraform fmt --diff -check` to see the issue (or run without `-check` to fix automatically)"

                    annotations.append({"path": path, "line": line_number, "message": error, "severity": "HIGH"})
        return {"annotations": annotations}
