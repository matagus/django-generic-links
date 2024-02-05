#!/usr/bin/env python
from __future__ import annotations

import os
import re
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_version(*file_paths):
    """Retrieves the version from generic_links/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


version = get_version("generic_links", "__init__.py")


if sys.argv[-1] == "publish":
    try:
        import wheel

        print("Wheel version: ", wheel.__version__)
    except ImportError:
        print('Wheel library missing. Please run "pip install wheel"')
        sys.exit()
    os.system("python setup.py sdist upload")
    os.system("python setup.py bdist_wheel upload")
    sys.exit()

if sys.argv[-1] == "tag":
    print("Tagging the version on git:")
    os.system(f"git tag -a {version} -m 'version {version}'")
    os.system("git push --tags")
    sys.exit()

readme = open("README.md").read()

setup(
    name="django-generic-links",
    version=version,
    description=""" Simple and generic application for Django projects to attach and handle links for any object""",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Matias Agustin Mendez",
    author_email="matagus@gmail.com",
    url="https://github.com/matagus/django-generic-links",
    packages=[
        "generic_links",
    ],
    include_package_data=True,
    install_requires=["Django>=4.0"],
    license="BSD",
    zip_safe=False,
    keywords="generic_links",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.1",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
