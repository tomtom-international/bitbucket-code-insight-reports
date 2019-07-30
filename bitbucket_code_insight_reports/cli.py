# -*- coding: utf-8 -*-

# pylint: disable=too-many-function-args

"""Console script for bitbucket_code_insight_reports."""
import sys
import argparse
from getpass import getpass

from bitbucket_code_insight_reports.report import Report
from bitbucket_code_insight_reports.terraform_report import TerraformReport
from bitbucket_code_insight_reports.git_diff_report import GitDiffReport
from bitbucket_code_insight_reports.spell_check_report import SpellCheckReport


def parse_args(args):
    """Returns parsed commandline arguments.
    """

    parser = argparse.ArgumentParser(description="Uploads information to code insights in BitBucket.")

    parser.add_argument(
        "--file", type=str, default=None, help="Input file for report (not required for all report types.)"
    )
    parser.add_argument(
        "--silent", action="store_true", default=False, help="Don't output what has been sent to BitBucket."
    )
    parser.add_argument(
        "--force_pass",
        action="store_true",
        default=False,
        help="Ensure that the report status on BitBucket can only be passing.",
    )

    auth_group = parser.add_argument_group("Authentication Options")
    auth_group.add_argument("-u", "--user", type=str, required=True, help="User to authenticate with BitBucket")
    auth_group.add_argument("-p", "--password", type=str, default=None, help="Password to authenticated with BitBucket")

    report_info_group = parser.add_argument_group("Report Options", description="Options to configure the report")
    report_info_group.add_argument("--report_key", type=str, required=True, help="BitBucket key for report.")
    report_info_group.add_argument("--report_title", type=str, required=True, help="Human readable title for report.")
    report_info_group.add_argument("--report_desc", type=str, required=True, help="Description for the report.")
    report_info_group.add_argument(
        "--report_type", choices=["terraform", "git-diff", "spell-check", "custom"], required=True, help="Report type"
    )

    bitbucket_group = parser.add_argument_group(
        "BitBucket Configuration", description="Info to access the repository and PR"
    )
    bitbucket_group.add_argument("--base_url", type=str, required=True, help="URL of the BitBucket server.")
    bitbucket_group.add_argument("--project_key", type=str, required=True, help="BitBucket key for the project.")
    bitbucket_group.add_argument("--repo_slug", type=str, required=True, help="Name of repo in BitBucket.")
    bitbucket_group.add_argument(
        "--commit", type=str, required=True, help="Commit hash for the commit to upload the report to."
    )

    custom_report_group = parser.add_argument_group(
        "Custom Report Options", description="Arguments only for use with the custom report type."
    )
    custom_report_group.add_argument(
        "--status", type=str, required=False, choices=["PASS", "FAIL"], help="Status of the report, PASS/FAIL."
    )
    custom_report_group.add_argument(
        "--annotations",
        type=str,
        default=None,
        help="""Annotations in a JSON string as shown in
        https://docs.atlassian.com/bitbucket-server/rest/5.16.0/bitbucket-code-insights-rest.html#idm361726402736""",
    )

    spellcheck_report_group = parser.add_argument_group(
        "Spellcheck Report Options", description="Arguments only for use with spellcheck report type."
    )
    spellcheck_report_group.add_argument(
        "--dict",
        type=str,
        nargs="+",
        required=False,
        default=[],
        help="Path to dictionaries to include when spell checking",
    )
    spellcheck_filelist_group = spellcheck_report_group.add_mutually_exclusive_group()
    spellcheck_filelist_group.add_argument(
        "--file_list", nargs="+", type=str, default=None, help="List of files to check."
    )
    spellcheck_filelist_group.add_argument(
        "--file_list_from_file",
        type=argparse.FileType("r"),
        default=None,
        help="File containing a newline separated list of files to check.",
    )

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
        report = TerraformReport(
            auth,
            args.base_url,
            args.project_key,
            args.repo_slug,
            args.commit,
            args.report_key,
            args.report_title,
            args.report_desc,
            force_pass=args.force_pass,
        )
    elif args.report_type == "git-diff":
        if args.file is None:
            print("You must provide a file for the git-diff report type.")
            exit(1)
        report = GitDiffReport(
            auth,
            args.base_url,
            args.project_key,
            args.repo_slug,
            args.commit,
            args.report_key,
            args.report_title,
            args.report_desc,
            args.file,
            force_pass=args.force_pass,
        )
    elif args.report_type == "custom":
        report = Report(
            auth,
            args.base_url,
            args.project_key,
            args.repo_slug,
            args.commit,
            args.report_key,
            args.report_title,
            args.report_desc,
            args.status,
            args.annotations,
            force_pass=args.force_pass,
        )
    elif args.report_type == "spell-check":
        if args.file_list:
            files_list = args.file_list
        elif args.file_list_from_file:
            files_list = args.file_list_from_file.read().strip().split("\n")
        else:
            print("You must provide a file list or a file with the file list")
            exit(1)
        report = SpellCheckReport(
            auth,
            args.base_url,
            args.project_key,
            args.repo_slug,
            args.commit,
            args.report_key,
            args.report_title,
            args.report_desc,
            force_pass=args.force_pass,
            files_to_check=files_list,
            dictionaries=args.dict,
        )

    report.post_base_report()
    report.post_annotations()

    if not args.silent:
        print(report.output_info())

    return report.return_code


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
