# -*- coding: utf-8 -*-

"""Main module."""
import json

import requests

class Report:
    """
    Generates a basic report for BitBucket Code Insight
    """
    def __init__(self, auth, base_url, project_key, repo_slug, commit_id, key, title, description, result, annotations, return_code=None):
        self.auth = auth
        self.title = title
        self.description = description
        self.result = result

        if return_code is None:
            if result == "PASS":
                self.return_code = 0
            else:
                self.return_code = 1
        else:
            self.return_code = return_code

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
