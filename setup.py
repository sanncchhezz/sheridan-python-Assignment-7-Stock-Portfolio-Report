"""
Package configuration for the stock portfolio report tool.

Running `pip install -e .` from the project root will install the package
in editable mode and register the `portfolio_report` CLI command, which
maps directly to the main() function in portfolio/portfolio_report.py.
"""
from setuptools import setup, find_packages


setup(
    name='portfolio-report',
    version='1.0.0',
    description='Generates up-to-date performance reports for stock portfolios using the IEX Cloud API.',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'portfolio_report=portfolio.portfolio_report:main',
        ],
    },
)
