import setuptools
import os


def read(file_name):
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(file_path, "r") as f:
        return f.read()


setuptools.setup(
    name="circleci-flaky",
    version="1.0.1",
    description="Fetch a list of flaky tests from a CircleCI project.",
    long_description=read("README.md"),
    url="https://github.com/ryanwilsonperkin/circleci-flaky",
    author="Ryan Wilson-Perkin",
    author_email="ryanwilsonperkin@gmail.com",
    license="MIT",
    py_modules=["circleci_flaky"],
    python_requires=">=3.6",
    install_requires=["requests"],
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={
        "console_scripts": ["circleci-flaky=circleci_flaky:main"],
    }
)
