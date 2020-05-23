# -*- coding: utf-8 -*-

from setuptools import find_namespace_packages, setup

with open("README.md", "r") as r:
    README = r.read()

TEST_REQUIRES = ["pytest-cov"]


setup(
    author="Pierre Sassoulas",
    author_email="pierre.sassoulas@gmail.com",
    long_description=README,
    long_description_content_type="text/markdown",
    name="centralized-pre-commit-conf",
    version="0.1.1",
    description="Makes it possible to easily install and update pre-commit hooks, and to centralize the configuration"
    " files of your tools.",
    packages=find_namespace_packages(),
    entry_points={"console_scripts": ["pre-commit-conf=centralized_pre_commit_conf.main:run"]},
    package_dir={},
    classifiers=[
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Development Status :: 4 - Beta",
    ],
    package_data={"centralized_pre_commit_conf": ["*.cfg", "*.yaml", "*.pylintrc", "*.flake8"]},
    install_requires=["setuptools>=45.1", "wheel>=0.34", "colorama", "pre-commit==1.14.0"],
    tests_require=TEST_REQUIRES,
    extras_require={"test": TEST_REQUIRES},
    url="https://github.com/Pierre-Sassoulas/centralized-pre-commit-conf",
    zip_safe=True,
)
