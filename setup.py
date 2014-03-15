from setuptools import setup, find_packages

from pip.req import parse_requirements

install_reqs = list(parse_requirements("requirements.txt"))

setup(
    name='tictactoe',
    version='0.0.1',
    author="Motiejus Jakštys",
    author_email="desired.mta@gmail.com",
    description="Ultimate Tic-Tac-Toe challenge front-end",
    long_description=open('README.rst').read(),
    url="https://github.com/Motiejus/ultimate-tic-tac-toe",
    packages=find_packages(),
    install_requires=[str(ir.req) for ir in install_reqs],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            "challenge = challenge.manage:main"
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
