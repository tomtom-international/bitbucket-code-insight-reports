# -*- coding: utf-8 -*-

"""Console script for bitbucket_code_insight_reports."""
import sys
import argparse
from getpass import getpass

from bitbucket_code_insight_reports.bitbucket_code_insight_reports import Report, TerraformReport


def parse_args(args):
    """Returns parsed commandline arguments.
    """

    parser = argparse.ArgumentParser(description="Uploads information to code insights in BitBucket.")

    auth_group = parser.add_argument_group("Authentication Options")
    auth_group.add_argument("-u", "--user", type=str, required=True, help="User to authenticate with BitBucket")
    auth_group.add_argument("-p", "--password", type=str, default=None, help="Password to authenticated with BitBucket")

    report_info_group = parser.add_argument_group("Report Options", description="Options to configure the report")
    report_info_group.add_argument("--report_key", type=str, required=True, help="BitBucket key for report.")
    report_info_group.add_argument("--report_title", type=str, required=True, help="Human readable title for report.")
    report_info_group.add_argument("--report_desc", type=str, required=True, help="Description for the report.")
    report_info_group.add_argument("--report_type", choices=['terraform', 'custom'], required=True, help="Report type")

    bitbucket_group = parser.add_argument_group("BitBucket Configuration", description="Info to access the repository and PR")
    bitbucket_group.add_argument("--base_url", type=str, required=True, help="URL of the BitBucket server.")
    bitbucket_group.add_argument("--project_key", type=str, required=True, help="BitBucket key for the project.")
    bitbucket_group.add_argument("--repo_slug", type=str, required=True, help="Name of repo in BitBucket.")
    bitbucket_group.add_argument("--commit", type=str, required=True, help="Commit hash for the commit to upload the report to.")

    custom_report_group = parser.add_argument_group("Custom Report Options", description="Arguments only for use with the custom report type.")
    custom_report_group.add_argument("--status", type=str, required=False, choices=["PASS", "FAIL"], help="Status of the report, PASS/FAIL.")
    custom_report_group.add_argument("--annotations", type=str, default=None, help="""Annotations in a JSON string as shown in
        https://docs.atlassian.com/bitbucket-server/rest/5.16.0/bitbucket-code-insights-rest.html#idm361726402736""")

    return parser.parse_args(args)

def main():
    """Console script for bitbucket_code_insight_reports."""
    args = parse_args(sys.argv[1:])

    if args.password is None:
        password = getpass("Enter your BitBucket Server password: ")
    else:
        password = args.password

    auth = (args.user, password)

    if args.report_type == "terraform":
        report = TerraformReport(auth, args.base_url, args.project_key, args.repo_slug, args.commit, args.report_key, args.report_title, args.report_desc)
    elif args.report_type == "custom":
        report = Report(auth, args.base_url, args.project_key, args.repo_slug, args.commit, args.report_key, args.report_title, args.report_desc, args.status, args.annotations)

    report.post_base_report()
    report.post_annotations()
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
