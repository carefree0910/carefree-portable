from setuptools import setup, find_packages

VERSION = "0.1.2"
PACKAGE_NAME = "carefree-portable"

DESCRIPTION = "Create portable (Python 🐍) projects on the fly 🚀 !"
with open("README.md", encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    entry_points={"console_scripts": ["cfport = cfport.cli:main"]},
    install_requires=[
        "click>=8.1.3",
        "carefree-toolkit>=0.3.10",
    ],
    author="carefree0910",
    author_email="syameimaru.saki@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    keywords="python portable",
)
