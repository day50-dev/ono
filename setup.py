from setuptools import setup, find_packages

setup(
    name='ono-preprocessor',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'typer',
        'pyyaml',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'ono=ono.cli:main',
        ],
    },
)