import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="benchplot",
    version="0.1",
    description="Plotting benchmark results",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/INM-6/benchplot",
    author="Jasper Albers, Anno Kurth, Dennis Terhorst, Jari Pronold",
    author_email="",
    license="GPLv3",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
    ],
    packages=["benchplot"],
    include_package_data=True,
    install_requires=["pandas", "matplotlib", "pyyaml"],
)