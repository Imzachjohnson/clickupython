import setuptools
from typing import List
import distutils.text_file
from pathlib import Path


cmdclass = {'build_sphinx': BuildDoc}

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()


def _parse_requirements(filename: str) -> List[str]:
    """Return requirements from requirements file."""
    # Ref: https://stackoverflow.com/a/42033122/
    return distutils.text_file.TextFile(filename=str(Path(__file__).with_name(filename))).readlines()


setuptools.setup(
    name='clickupy',
    author='Zach Johnson & Robert Mullis',
    author_email='imzachjohnson@gmail.com',
    description='Clickupy: A Python client for the ClickUp API',
    keywords='clickup, clickup api, python, clickupy',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Imzachjohnson/clickupy',
    
    project_urls={
        'Documentation': 'https://clickupy.readthedocs.io/en/latest/',
        'Bug Reports':
        'https://github.com/Imzachjohnson/clickupy/issues',
        'Source Code': 'https://github.com/Imzachjohnson/clickupy',
        # 'Funding': '',
        # 'Say Thanks!': '',
    },
    
    packages=setuptools.find_packages(),
    python_requires='>=3.9',
    install_requires=['pydantic==1.8.2','typing-extensions==3.10.0.2'],
    #extras_require='requirements.txt',
    # entry_points={
    #     'console_scripts': [  # This can provide executable scripts
    #         'run=examplepy:main',
    # You can execute `run` in bash to run `main()` in src/examplepy/__init__.py
    #     ],
    # },
)
