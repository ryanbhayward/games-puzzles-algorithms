from setuptools import setup, find_packages
import warnings

setup(
    name='games_puzzles_algorithms',
    version='0.0.1',
    packages=find_packages(),
    scripts=['bin/games_puzzles_algorithms_gtp.py'],
    install_requires=[
        'future == 0.15.2',
        'setuptools == 20.2.2',
        "cffi >= 1.0.0"
    ],
    tests_require=[
        'pytest'
    ],
    setup_requires=["cffi >= 1.0.0"],
    cffi_modules=["games_puzzles_algorithms/games/dex/hyper_cube_indexer_build.py:ffi"]
)
