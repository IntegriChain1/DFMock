from setuptools import setup, find_packages

package_name = "dfmock"
package_version = "0.0.1"
description = "utility for generating mock data sets as pandas dataframes"


setup(
    name=package_name,
    version=package_version,
    description=description,
    long_description=description,
    author="Ethan Knox",
    author_email="ethan.m.knox@gmail.com",
    url="https://github.com/norton120/dfmock",
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
