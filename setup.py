import sys
import os
from setuptools import setup


sys.path.append(os.getcwd())
setup(
    setup_requires=[
        'pytest',
        'matplotlib',
        'numpy',
    ],
    tests_require=[
        'pytest',
    ],
)
