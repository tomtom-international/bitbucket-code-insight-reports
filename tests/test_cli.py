#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `bitbucket_code_insight_reports` package."""
from argparse import ArgumentError

import pytest

from bitbucket_code_insight_reports import cli


def test_arg_parse():
    """Test the parsing from the CLI."""

    args = [
        "--user",
        "test_user",
        "--password",
        "test_password",
        "--report_key",
        "test_report_key",
        "--report_title",
        "test_report_title",
        "--report_desc",
        "test_report_desc",
        "--base_url",
        "test_url",
        "--project_key",
        "test_project_key",
        "--repo_slug",
        "test_repo_slug",
        "--commit",
        "test_commit",
        "--report_type",
        "custom",
        "--status",
        "PASS",
        "--annotations",
        "test_annotations",
        "--file",
        "test_file.txt",
        "--file_list",
        "test_file_1",
        "test_file_2",
        "--dict",
        "/some/path/to/dictionary",
        "--silent",
    ]

    parser = cli.parse_args(args)

    assert parser.user == "test_user"
    assert parser.password == "test_password"
    assert parser.report_key == "test_report_key"
    assert parser.report_title == "test_report_title"
    assert parser.report_desc == "test_report_desc"
    assert parser.base_url == "test_url"
    assert parser.project_key == "test_project_key"
    assert parser.repo_slug == "test_repo_slug"
    assert parser.commit == "test_commit"
    assert parser.report_type == "custom"
    assert parser.status == "PASS"
    assert parser.annotations == "test_annotations"
    assert parser.file == "test_file.txt"
    assert parser.file_list == ["test_file_1", "test_file_2"]
    assert parser.dict == ["/some/path/to/dictionary"]
    assert parser.silent == True
