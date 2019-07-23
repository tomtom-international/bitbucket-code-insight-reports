#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from __future__ import with_statement

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

import bitbucket_code_insight_reports


with open("README.md") as readme_file:
    readme = readme_file.read()

with open("CHANGELOG.md") as changelog_file:
    changelog = changelog_file.read()

requirements = ["python-terraform==0.10.0", "requests==2.22.0", "scspell3k==2.2"]

setup_requirements = ["pytest-runner"]

test_requirements = ["pytest", "pytest-cov", "coverage", "hypothesis"]

setup(
    author=bitbucket_code_insight_reports.__author__,
    author_email=bitbucket_code_insight_reports.__email__,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    description="Upload reports to BitBucket server for use with the Code Insights feature",
    entry_points={"console_scripts": ["bitbucket-code-insight-reports=bitbucket_code_insight_reports.cli:main"]},
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme + "\n\n" + changelog,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="bitbucket_code_insight_reports",
    name="bitbucket_code_insight_reports",
    packages=find_packages(),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/tomtom-international/bitbucket-code-insight-reports",
    version=bitbucket_code_insight_reports.__version__,
    zip_safe=False,
)
