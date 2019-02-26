# circleci-flaky

[![PyPI version](https://img.shields.io/pypi/v/circleci-flaky.svg)](https://pypi.org/project/circleci-flaky) [![Python versions](https://img.shields.io/pypi/pyversions/circleci-flaky.svg)](https://pypi.org/project/circleci-flaky)

A command line utility to fetch a list of flaky tests from a CircleCI project.

---

## Features

CircleCI provides an "Insights" section for your workflows, but it's limited in how far back the data goes. `circleci-flaky` allows you to specify up to 100 of the previous failed builds to check for recurring failed tests. It defaults to checking the master branch and displaying all failed tests, but both of these can be customized.

```sh
$ circleci-flaky -h
usage: circleci-flaky [-h] [--branch BRANCH] [--builds N] [--top N] project

Check a CircleCI project for flaky tests

positional arguments:
  project          the project to check

optional arguments:
  -h, --help       show this help message and exit
  --branch BRANCH  branch to check for failures (default: master)
  --builds N       number of failed builds to check (default: 30)
  --top N          limit results to the top N (default: all)
```

## Installation

You can install `circleci-flaky` via pip from [PyPI][pypi].

```sh
# If you run both Python 2 and 3 on your system, use pip3
sudo pip3 install circleci-flaky

# If you only run Python 3, you can just use pip
sudo pip install circleci-flaky
```

## Usage

Because this tool leverages the CircleCI API, you'll need a Personal API Token.
Navigate to https://circleci.com/account/api and create a new token (note it
down).

Run the command like so:

```sh
CIRCLECI_TOKEN=your_token circleci-flaky org/repo
```

If you want to persist the token for multiple runs in your terminal, export it instead:

```sh
export CIRCLECI_TOKEN=your_token
```

then run the command without specifying the token:

```sh
circleci-flaky org/repo
```

## Contributing

Contributors welcome!

## License

Distributed under the terms of the [MIT](/LICENSE) license, `circleci-flaky` is free and open source software.

## Issues

If you encounter any problems, please [file an issue](new-issue) along with a detailed description.

[pypi]: https://pypi.org/project/circleci-flaky/
[new-issue]: https://github.com/ryanwilsonperkin/circleci-flaky/issues/new
