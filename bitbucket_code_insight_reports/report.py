# -*- coding: utf-8 -*-

"""Main module."""
import json

import requests


class Report:
    """
    Generates a basic report for BitBucket Code Insight
    """

    def __init__(  # pylint: disable=too-many-locals
        self,
        auth,
        base_url,
        project_key,
        repo_slug,
        commit_id,
        key,
        title,
        description,
        result,
        annotations_string="",
        return_code=None,
        file_name=None,
        force_pass=False,
    ):
        """
        Sets up the BitBucket code insights report
        Args:
            auth: Authentication tuple for BitBucket
            base_url: base URL for BitBucket
            project_key: project key in BitBucket for the target PR
            repo_slug: repository slug (i.e. name in the URL) for the target PR
            commit_id: commit ID for the target PR
            key: key to use for the report
            title: title to use for the report
            description: description to provide for the report
            result: result to use for the report (PASS/FAIL)
            annotations_string: (optional) JSON string of annotations for the report
            return_code: (optional) return code to return from the tool
            file_name: (optional) file name to read results from
            force_pass: (optional) Boolean, true to force setting the result to PASS and the return_code to 0 (for use in non-blocking CI steps)
        """
        self.auth = auth
        self.title = title
        self.description = description

        self._check_return_and_result(force_pass, return_code, result)

        if file_name is not None:
            with open(file_name, mode="r") as report_file:
                annotations_string = report_file.read()

        self.url = self._build_base_report_url(base_url, project_key, repo_slug, commit_id, key)
        self.annotations = self._process_annotations(annotations_string)

    def _check_return_and_result(self, force_pass, return_code, result):
        """
        Determine what needs to be set for return_code (which is what the tool itself should return to the calling function) and what should be set
        for result (which is what is posted to BitBucket).
        Args:
            force_pass: bool to indicate that everything should be set to passing and the tool should return 0
            return_code: int
        """
        # This allows the user to force everything to pass, as for a non-blocking CI step
        if force_pass:
            self.return_code = 0
            self.result = "PASS"
            return

        self.result = result
        if return_code:
            self.return_code = return_code
            return

        # Determines the return code status if it isn't set, as is the case for checks not directly invoked from this tool
        if self.result == "PASS":
            self.return_code = 0
        else:
            self.return_code = 1
        return

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
        return (
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
        Args:
            annotations_string: annotations to load
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

    def output_info(self):
        """
        Returns string with base report and annotation information
        """
        report_info = "\nURL: {url}\n".format(url=self.url)
        report_info += "Title: {title}\n".format(title=self.title)
        report_info += "Description: {desc}\n".format(desc=self.description)
        report_info += "Result: {result}\n".format(result=self.result)
        report_info += "Annotations: {annot}\n".format(annot=json.dumps(self.annotations, indent=4, sort_keys=True))
        return report_info
