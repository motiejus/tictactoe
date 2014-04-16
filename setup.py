import os
import sys

from setuptools import setup, find_packages

HERE = os.path.dirname(__file__)
install_reqs = [r.strip() for r in open(os.path.join(HERE, "requirements.txt"))]

if sys.version_info < (3, 3):
    install_reqs.append("mock==1.0.1")

setup(
    name='tictactoe',
    version='0.0.2a1',
    author="Motiejus Jakštys",
    author_email="desired.mta@gmail.com",
    description="Ultimate Tic-Tac-Toe tictactoe front-end",
    long_description=open('README.rst').read(),
    url="https://github.com/Motiejus/tictactoe",
    packages=find_packages(),
    install_requires=install_reqs,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            "tictactoe = tictactoe.manage:main"
        ]
    },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Education",
        "Topic :: Games/Entertainment :: Puzzle Games",
        "License :: OSI Approved :: MIT License",
    ],
)
