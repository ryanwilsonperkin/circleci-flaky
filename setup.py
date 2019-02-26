import setuptools

setuptools.setup(
    name="circleci-flaky",
    version="1.0.0",
    description="Fetch a list of flaky tests from a CircleCI project.",
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
