from setuptools import setup, find_packages

setup(
    name='hex-web-ui',
    version='0.0.1',
    license='MIT',
    packages=find_packages(),
    scripts=['application.py'],
    install_requires=[
        'games_puzzles_algorithms >= 0.0.1',
        'flask == 1.1.1',
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License'
    ],
)
