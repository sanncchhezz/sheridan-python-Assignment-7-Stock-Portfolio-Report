"""
Tests I/O disk operations.
"""
from collections import OrderedDict

from portfolio import portfolio_report


# Note: the portfolio_csv argument found in the tests below
#       is a pytest "fixture". It is defined in conftest.py

# DO NOT edit the provided tests. Make them pass.

def test_read_portfolio(portfolio_csv):
    """
    Given that the read_portfolio is called, assert that
    the data the expected data is returned.
    """
    expected = [
        OrderedDict([
            ('symbol', 'APPL'),
            ('units', '100'),
            ('cost', '154.23'),
        ]),
        OrderedDict([
            ('symbol', 'AMZN'),
            ('units', '600'),
            ('cost', '1223.43')
        ])
    ]

    assert portfolio_report.read_portfolio(portfolio_csv) == expected, (
        'Expecting to get the data stored in the portfolio_csv '
        'fixture as a Python data structure.'
    )


def test_save_portfolio(portfolio_csv):
    """
    Given that the save portfolio method is called with the following
    data, assert that a CSV file is written in the expected format.

    The portfolio
    """
    data = [{'symbol': 'MSFT', 'units': 10, 'cost': 99.66}]
    portfolio_report.save_portfolio(data, filename=portfolio_csv)

    expected = 'symbol,units,cost\r\nMSFT,10,99.66\r\n'
    with open(portfolio_csv, 'r', newline='') as file:
        result = file.read()
        assert result == expected, (
            f'Expecting the file to contain: \n{result}'
        )


def test_get_args():
    """
    Given that get_args is called with --source and --target flags,
    assert that the parsed values are correctly assigned to the
    corresponding attributes on the returned Namespace object.
    """
    args = portfolio_report.get_args(['--source', 'portfolio.csv', '--target', 'report.csv'])

    assert args.source == 'portfolio.csv', (
        'Expecting args.source to equal the value passed to --source.'
    )
    assert args.target == 'report.csv', (
        'Expecting args.target to equal the value passed to --target.'
    )