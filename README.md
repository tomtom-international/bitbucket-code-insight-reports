# bitbucket-code-insight-reports

[![Azure DevOps builds](https://img.shields.io/azure-devops/build/tomtomweb/GitHub-TomTom-International/5/master.svg)](https://dev.azure.com/tomtomweb/GitHub-TomTom-International/_build/latest?definitionId=32&branchName=master)
[![Azure DevOps tests](https://img.shields.io/azure-devops/tests/tomtomweb/GitHub-TomTom-International/5/master.svg)](https://dev.azure.com/tomtomweb/GitHub-TomTom-International/_build/latest?definitionId=32&branchName=master)
[![Azure DevOps coverage](https://img.shields.io/azure-devops/coverage/tomtomweb/GitHub-TomTom-International/5/master.svg)](https://dev.azure.com/tomtomweb/GitHub-TomTom-International/_build/latest?definitionId=32&branchName=master)

[![PyPI - Version](https://img.shields.io/pypi/v/bitbucket-code-insight-reports.svg)](https://pypi.org/project/bitbucket-code-insight-reports/)
[![PyPI - License](https://img.shields.io/pypi/l/bitbucket-code-insight-reports.svg)](https://pypi.org/project/bitbucket-code-insight-reports/)
[![PyPI - Python Versions](https://img.shields.io/pypi/pyversions/bitbucket-code-insight-reports.svg)](https://pypi.org/project/bitbucket-code-insight-reports/)
[![PyPI - Format](https://img.shields.io/pypi/format/bitbucket-code-insight-reports.svg)](https://pypi.org/project/bitbucket-code-insight-reports/)
[![PyPI - Status](https://img.shields.io/pypi/status/bitbucket-code-insight-reports.svg)](https://pypi.org/project/bitbucket-code-insight-reports/)
[![PyUp - Updates](https://pyup.io/repos/github/tomtom-international/bitbucket-code-insight-reports/shield.svg)](https://pyup.io/repos/github/tomtom-international/bitbucket-code-insight-reports/)


Upload reports to BitBucket server for use with the Code Insights feature.

Designed to be extensible, so it can be hooked to anything that outputs file paths, line numbers and errors.

## Features

* Report failing lines from the output of `terraform fmt --diff -check -recursive`
* Report failing lines from the output of `git diff` (must be provided with an input file)

## Usage

```
usage: bitbucket-code-insight-reports [-h] [--file FILE] -u USER [-p PASSWORD]
                                      --report_key REPORT_KEY --report_title
                                      REPORT_TITLE --report_desc REPORT_DESC
                                      --report_type
                                      {terraform,git-diff,custom} --base_url
                                      BASE_URL --project_key PROJECT_KEY
                                      --repo_slug REPO_SLUG --commit COMMIT
                                      [--status {PASS,FAIL}]
                                      [--annotations ANNOTATIONS]

Uploads information to code insights in BitBucket.

optional arguments:
  -h, --help            show this help message and exit
  --file FILE           Input file for report (not required for all report
                        types.

Authentication Options:
  -u USER, --user USER  User to authenticate with BitBucket
  -p PASSWORD, --password PASSWORD
                        Password to authenticated with BitBucket

Report Options:
  Options to configure the report

  --report_key REPORT_KEY
                        BitBucket key for report.
  --report_title REPORT_TITLE
                        Human readable title for report.
  --report_desc REPORT_DESC
                        Description for the report.
  --report_type {terraform,git-diff,custom}
                        Report type

BitBucket Configuration:
  Info to access the repository and PR

  --base_url BASE_URL   URL of the BitBucket server.
  --project_key PROJECT_KEY
                        BitBucket key for the project.
  --repo_slug REPO_SLUG
                        Name of repo in BitBucket.
  --commit COMMIT       Commit hash for the commit to upload the report to.

Custom Report Options:
  Arguments only for use with the custom report type.

  --status {PASS,FAIL}  Status of the report, PASS/FAIL.
  --annotations ANNOTATIONS
                        Annotations in a JSON string as shown in
                        https://docs.atlassian.com/bitbucket-
                        server/rest/5.16.0/bitbucket-code-insights-
                        rest.html#idm361726402736
```


## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [tomtom-international/cookiecutter-python](https://github.com/tomtom-international/cookiecutter-python) project template.
