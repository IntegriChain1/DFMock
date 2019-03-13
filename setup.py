from setuptools import setup, find_packages
from os import path

package_name = "dfmock"
package_version = "0.0.14"
description = "utility for generating mock data sets as pandas dataframes"

cur_directory = path.abspath(path.dirname(__file__))
with open(path.join(cur_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name=package_name,
    version=package_version,
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Integrichain Innovation Team",
    author_email="engineering@integrichain.com",
    url="https://github.com/integrichain1/dfmock",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7"
        ],
    packages= find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=["pandas"]
    )
