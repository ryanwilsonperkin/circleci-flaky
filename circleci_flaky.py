#!/usr/local/bin/python3
"""
Fetch a list of flaky tests from a CircleCI project.

Searches the last 30 builds that have failed on the master branch and reports
the tests that have failed.

Branch name, number of builds, and number of results are all customizable.
"""
import argparse
import collections
import os
import sys

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


def fetch_failed_builds(project_name, branch, builds):
    MAX_LIMIT = 100
    return circleci_fetch(
        f"/project/github/{project_name}/tree/{branch}",
        filter="failed",
        limit=min(builds, MAX_LIMIT),
    )


def fetch_test_failures(project_name, build_number):
    test_results = circleci_fetch(f"/project/github/{project_name}/{build_number}/tests")
    for test_result in test_results["tests"]:
        if test_result["result"] == "failure":
            classname = test_result["classname"]
            name = test_result["name"]
            yield f"{classname}.{name}"


def flaky(project_name, branch, builds, top):
    failures = []
    failures_map = collections.defaultdict(list)

    builds = fetch_failed_builds(project_name, branch, builds)
    for build in builds:
        for failure in fetch_test_failures(project_name, build["build_num"]):
            failures.append(failure)
            failures_map[failure].append(build)

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
    flaky(args.project, args.branch, args.builds, args.top)


if __name__ == "__main__":
    main()
