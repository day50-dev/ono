from setuptools import setup, find_packages

setup(
    name='onorous',
    version='0.1.0',
    description='Ono - Universal AI-Powered Preprocessor',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Ono Team',
    author_email='team@onolang.com',
    url='https://onolang.com',
    packages=find_packages(),
    install_requires=[
        'typer',
        'pyyaml',
        'requests',
        'httpx'
    ],
    entry_points={
        'console_scripts': [
            'onorous=ono.cli:main',
        ],
    },
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
    ],
)