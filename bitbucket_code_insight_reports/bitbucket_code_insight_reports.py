# -*- coding: utf-8 -*-

"""Main module."""
import re
import json

import requests

from python_terraform import Terraform

class Report:
    """
    Generates a basic report for BitBucket Code Insight
    """
    def __init__(self, auth, base_url, project_key, repo_slug, commit_id, key, title, description, result, annotations):
        self.auth = auth
        self.title = title
        self.description = description
        self.result = result
        self.url = self._build_base_report_url(base_url, project_key, repo_slug, commit_id, key)
        self.annotations = self._process_annotations(annotations)

    @staticmethod
    def _build_base_report_url(base_url, project_key, repo_slug, commit_id, key):
        """
        Generates the report URL from component strings.
        Args:
            base_url: URL of the BitBucket server
            project_key: Project key for the project the repository is in
            repo_slug: Key for the repository
            commit_id: Commit to apply the report to
            key: Name for the report
        Returns:
            Url for the report
        """
        return base_url + "/rest/insights/1.0/projects/" + project_key + "/repos/" + repo_slug + "/commits/" + commit_id + "/reports/" + key

    def post_base_report(self):
        """
        Publishes the report (without annotations)
        """
        body = {"title": self.title, "details": self.description, "result": self.result}
        requests.put(self.url, json=body, auth=self.auth)

    @staticmethod
    def _process_annotations(annotations_string):
        """
        Converts the annotations string provided to a dictionary
        Returns:
            Dictionary with the annotations.
        """
        return json.loads(annotations_string)

    def post_annotations(self):
        """
        Publishes the annotations to the report.
        """
        annotations_url = self.url + "/annotations"
        requests.post(annotations_url, json=self.annotations, auth=self.auth)

class TerraformReport(Report):
    """
    Executes `terraform fmt` and converts the results into a report for BitBucket Server Code Insights
    """
    def __init__(self, auth, base_url, project_key, repo_slug, commit_id, key, title, description):
        terraform = Terraform()
        return_code, annotations, error = terraform.fmt(capture_output=True, check=True, diff=True, recursive=True)

        if return_code == 0:
            result = "PASS"
        else:
            result = "FAIL"

        super().__init__(auth, base_url, project_key, repo_slug, commit_id, key, title, description, result, annotations)

    @staticmethod
    def _process_annotations(annotations_string):
        """
        Converts the output of `terraform fmt --diff -check` to an annotations dictionary.
        Returns:
            Dictionary with the annotations.
        """
        annotations = []

        if annotations_string:
            # Split on the diff output pattern
            split_output = re.compile(r"(.*\n-{3}.*\n\+{3}.*)").split(annotations_string)
            for file_errors_counter in range(1, len(split_output), 2):
                path = split_output[file_errors_counter].split('\n')[0]

                entries = re.compile(r"(@{2}[\+\-\,\d\ ]*@{2})").split(split_output[file_errors_counter + 1])

                for error_counter in range(1, len(entries), 2):
                    line_number = entries[error_counter].split(' ')[1][1:].split(',')[0]
                    error = "Error found in this block. Run `terraform fmt --diff -check` to see the issue (or run without `-check` to fix automatically)"

                    annotations.append({
                        "path": path,
                        "line": line_number,
                        "message": error,
                        "severity": "HIGH"
                    })
        return {'annotations': annotations}
