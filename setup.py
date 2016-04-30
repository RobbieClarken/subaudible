from setuptools import setup
import re


with open('subaudible/__init__.py') as file:
    version = re.search(r"__version__ = '(.*)'", file.read()).group(1)

with open('README.rst') as file:
    readme = file.read()


setup(
    name='subaudible',
    version=version,
    description='Display subtitles for audio picked up by the system microphone',
    long_description=readme,
    author='Robbie Clarken',
    author_email='robbie.clarken@gmail.com',
    url='https://github.com/RobbieClarken/subaudible',
    license='MIT',
    packages=['subaudible'],
    install_requires=[
        'sounddevice',
        'scipy',
        'numpy',
    ],
)
