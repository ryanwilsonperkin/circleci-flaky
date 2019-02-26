#!/usr/local/bin/python3
"""
@author Ryan Wilson-Perkin

Fetch a list of flaky tests from a CircleCI project.

Searches the last 30 builds that have failed on the master branch, downloads any
junit.xml artifacts it finds for them, and reports the tests that have failed.

Branch name, test results file, number of builds, and number of results are all
customizable.

Installation:
    pip install requests

Usage:
    ./circleci_flaky.py --help
"""
import argparse
import collections
import fnmatch
import os
import sys
import xml.etree.ElementTree

# External dependencies
try:
    import requests
except ImportError:
    sys.exit("Could not find `requests` package. Please install it with `pip3 install requests`")


def get_token():
    token = os.environ.get("CIRCLECI_TOKEN")
    if token is None:
        sys.exit(
            "No CIRCLECI_TOKEN environment variable set\n."
            "Visit https://circleci.com/account/api to create a new token.\n"
            "Then invoke this command with CIRCLECI_TOKEN=your_token"
        )
    return token


def circleci_fetch(api, **kwargs):
    base_url = "https://circleci.com/api/v1.1"
    token = get_token()
    response = requests.get(
        f"{base_url}{api}",
        params={"circle-token": token, **kwargs},
    )
    return response.json()


def circleci_fetch_artifact(url):
    token = get_token()
    response = requests.get(
        url,
        params={"circle-token": token},
    )
    return response.text


def fetch_failed_builds(project_name, branch, builds):
    MAX_LIMIT = 100
    return circleci_fetch(
        f"/project/github/{project_name}/tree/{branch}",
        filter="failed",
        limit=min(builds, MAX_LIMIT),
    )


def fetch_build_artifact(project_name, build_number, artifact_name):
    artifacts = circleci_fetch(f"/project/github/{project_name}/{build_number}/artifacts")
    for artifact in artifacts:
        if fnmatch.fnmatch(artifact["path"], artifact_name):
            yield artifact


def parse_artifact_failures(artifact_content):
    root = xml.etree.ElementTree.fromstring(artifact_content)
    for element in root.findall(".//testcase"):
        if element.findall("failure"):
            classname = element.get('classname')
            name = element.get('name')
            yield f"{classname}.{name}"


def flaky(project_name, branch, builds, top, artifact_name):
    failures = []
    failures_map = collections.defaultdict(list)

    builds = fetch_failed_builds(project_name, branch, builds)
    for build in builds:
        artifacts = fetch_build_artifact(project_name, build["build_num"], artifact_name)
        for artifact in artifacts:
            artifact_content = circleci_fetch_artifact(artifact["url"])
            build_failures = parse_artifact_failures(artifact_content)
            for build_failure in build_failures:
                failures.append(build_failure)
                failures_map[build_failure].append(build)

    counter = collections.Counter(failures)
    for failure, count in counter.most_common(top):
        print(f"{failure} failed {count} times")
        for failed_build in failures_map[failure]:
            print(f"{failed_build['build_url']}")
        print()


def get_parser():
    parser = argparse.ArgumentParser(description='Check a CircleCI project for flaky tests')
    parser.add_argument('project', type=str, help='the project to check')
    parser.add_argument(
        '--branch',
        dest='branch',
        default='master',
        type=str,
        help='branch to check for failures (default: master)',
    )
    parser.add_argument(
        '--builds',
        dest='builds',
        default=30,
        metavar='N',
        type=int,
        help='number of failed builds to check (default: 30)',
    )
    parser.add_argument(
        '--top',
        dest='top',
        metavar='N',
        default=None,
        type=int,
        help='limit results to the top N (default: all)',
    )
    parser.add_argument(
        '--test-artifact-name',
        dest='artifact_name',
        default='*junit.xml',
        metavar='FILE',
        type=str,
        help='the full path to the file where test results are stored; supports wildcards (default: *junit.xml)',
    )
    return parser


def main():
    if not get_token():
        sys.exit(
            "No CIRCLECI_TOKEN environment variable set\n."
            "Visit https://circleci.com/account/api to create a new token.\n"
            "Then invoke this command with CIRCLECI_TOKEN=your_token"
        )
    parser = get_parser()
    args = parser.parse_args()
    flaky(args.project, args.branch, args.builds, args.top, args.artifact_name)


if __name__ == "__main__":
    main()
