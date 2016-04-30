from setuptools import setup
import re

with open('subaudible/__init__.py') as file:
    version = re.search(r"__version__ = '(.*)'", file.read()).group(1)

setup(
    name='subaudible',
    version=version,
    packages=['subaudible'],
    install_requires=[
        'sounddevice',
        'scipy',
        'numpy',
    ],
)
