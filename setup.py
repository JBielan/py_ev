from setuptools import setup
from os import path

DIR = path.dirname(path.abspath(__file__))

with open(path.join(DIR, 'README.md')) as f:
    README = f.read()

setup(
    name='py_ev',
    packages=['py_ev'],
    description="Poker hand evaluator written and tested in Python",
    long_description=README,
    long_description_content_type='text/markdown',
    version='0.0.2',
    url='https://github.com/JBielan/py_ev',
    author='Jakub Bielan',
    author_email='jkbielan@gmail.com',
    keywords=['poker', 'hand-evaluator', 'texas-holdem', 'omaha', '6-plus', 'evaluator'],
    tests_require=[
        'pytest',
        'pytest-cov'
    ],
    python_requires='>=3'
)