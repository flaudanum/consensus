import os.path
from pathlib import Path
import re
from setuptools import setup, find_packages


def read_version() -> str:
    # Path to my_package_name/__init__.py
    root_init_path = Path(__file__).parent / 'consensus' / '__init__.py'
    with root_init_path.open('r') as fobj:
        for line in fobj.readlines():
            match_obj_dq = re.match(r'__version__\s*=\s*"(.+)"', line)  # double quotes
            match_obj_sq = re.match(r"__version__\s*=\s*'(.+)'", line)  # simple quotes
            match_obj = match_obj_dq or match_obj_sq
            if match_obj:
                return match_obj.group(1)


setup(
    name="consensus",
    version=read_version(),
    packages=find_packages(),

    python_requires='==3.9',

    install_requires=[
        'pandas',
    ],

    # scripts=['./my_script.py', ],

    include_package_data=True,

    # metadata to display on PyPI
    author="Frédéric Laudarin",
    author_email="frederic.laudarin@gmail.com",
    description="Consensus algorithm for making a group rank alternatives to a problem",
    license="MIT",
    keywords="decision making consensus",
    url="https://github.com/flaudanum/consensus",
    project_urls={
        "Bug Tracker": "https://github.com/flaudanum/consensus/issues",
        "Documentation": "https://github.com/flaudanum/consensus/blob/main/README.md",
        "Source Code": "https://github.com/flaudanum/consensus",
    }
)