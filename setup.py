# made with claude code; i dont know jacksh*t

from setuptools import setup, find_packages
import pathlib

HERE = pathlib.Path(__file__).parent

LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding="utf-8") if (HERE / "README.md").exists() else ""

setup(
    name="maxl",
    version="0.0.1",
    description="MaxL - An interactive shell/interpreter with simulated filesystem",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Filip",  # TODO: Update
    url="https://github.com/filips0108/maxl",  # TODO: Update
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "prompt_toolkit>=3.0",
        "rich>=10.0",
    ],
    entry_points={
        "console_scripts": [
            "maxl=modules.std:load",
        ],
    },
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Environment :: Console",
    ],
)