from setuptools import find_packages, setup

NAME = "cacher"


def read(filename):
    try:
        with open(filename) as fp:
            content = fp.read().split("\n")
    except FileNotFoundError:
        content = []
    return content


setup(
    author="Quinten Roets",
    author_email="quinten.roets@gmail.com",
    description="function caching",
    name=NAME,
    version="1.0",
    packages=find_packages(),
    install_requires=read("requirements.txt"),
    entry_points={"console_scripts": ["clearcache = cacher.clearing:main"]},
)
