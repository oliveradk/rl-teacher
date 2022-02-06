import sys

from setuptools import setup

if sys.version_info.major != 3:
    print("This module is only compatible with Python 3, but you are running "
          "Python {}. The installation will likely fail.".format(sys.version_info.major))

setup(name='es_augmentenv',
    version='0.0.1',
    install_requires=[
        'gym',
        'mujoco-py',
        'multiprocess ~= 0.70.5',
        'numpy',
        'cma'
    ],
)
