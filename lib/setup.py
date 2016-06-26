from setuptools import setup, find_packages
import warnings

setup(
    name='games_puzzles_algorithms',
    version='0.0.1',
    packages=find_packages(),
    scripts=['bin/games_puzzles_algorithms_gtp.py'],
    install_requires=[
        'future == 0.15.2',
        'setuptools == 20.2.2'
    ],
    tests_require=['pytest'],
    setup_requires=['pytest-runner']
)
