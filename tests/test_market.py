"""
Tests for market data retrieval and portfolio metrics calculations.
"""
import os
import pytest
import requests_mock as requests_mock_module

from portfolio import portfolio_report


IEX_BASE_URL = 'https://cloud.iexapis.com/stable/tops'


def test_get_market_data(requests_mock):
    """
    Given that get_market_data is called with a list of stock symbols,
    assert that it returns a dict keyed by symbol containing the market
    data for each stock, using a mocked IEX Cloud API response.

    requests_mock is a pytest fixture provided by the requests-mock library
    that intercepts outgoing HTTP requests and returns controlled responses,
    so no real network connection or API key is needed in tests.
    """
    fake_response = [
        {'symbol': 'AAPL', 'price': 186.84, 'size': 100, 'time': 1234567890},
        {'symbol': 'AMZN', 'price': 3500.00, 'size': 50, 'time': 1234567890},
    ]
    requests_mock.get(IEX_BASE_URL, json=fake_response)

    result = portfolio_report.get_market_data(['AAPL', 'AMZN'])

    assert result == {
        'AAPL': {'symbol': 'AAPL', 'price': 186.84, 'size': 100, 'time': 1234567890},
        'AMZN': {'symbol': 'AMZN', 'price': 3500.00, 'size': 50, 'time': 1234567890},
    }, 'Expecting a dict keyed by symbol with the full market data entry for each stock.'


def test_get_market_data_missing_symbol(requests_mock):
    """
    Given that the IEX API omits a requested symbol from its response
    (which happens when the symbol is invalid or not traded), assert that
    get_market_data returns data only for the symbols that were found and
    prints a warning for the missing one, without raising an error.
    """
    fake_response = [
        {'symbol': 'AAPL', 'price': 186.84, 'size': 100, 'time': 1234567890},
    ]
    requests_mock.get(IEX_BASE_URL, json=fake_response)

    result = portfolio_report.get_market_data(['AAPL', 'INVALID'])

    assert 'AAPL' in result, 'Expecting AAPL to be present in the result.'
    assert 'INVALID' not in result, 'Expecting missing symbol to be absent from the result.'


def test_get_market_data_missing_symbol_warning(requests_mock, capsys):
    """
    Given that the IEX API omits a requested symbol from its response,
    assert that get_market_data prints a warning message to stdout that
    includes the name of the missing symbol.

    capsys is a built-in pytest fixture that captures text written to
    stdout and stderr during the test, allowing us to assert on printed
    output without needing to change the function's return value.
    """
    fake_response = [
        {'symbol': 'AAPL', 'price': 186.84, 'size': 100, 'time': 1234567890},
    ]
    requests_mock.get(IEX_BASE_URL, json=fake_response)

    portfolio_report.get_market_data(['AAPL', 'INVALID'])

    captured = capsys.readouterr()
    assert 'INVALID' in captured.out, (
        'Expecting a warning printed to stdout containing the missing symbol name.'
    )


def test_calculate_metrics():
    """
    Given a portfolio row and its matching market data entry, assert that
    calculate_metrics correctly computes book_value, market_value, gain_loss,
    and change, and returns a list of dicts containing all 8 output columns.

    book_value  = units x cost
    market_value = units x latest_price
    gain_loss   = market_value - book_value
    change      = gain_loss / book_value
    """
    portfolio = [
        {'symbol': 'AAPL', 'units': '10', 'cost': '100.00'},
    ]
    market_data = {
        'AAPL': {'symbol': 'AAPL', 'price': 150.00, 'size': 100, 'time': 1234567890},
    }

    result = portfolio_report.calculate_metrics(portfolio, market_data)

    assert len(result) == 1, 'Expecting one row in the result.'

    row = result[0]
    assert row['symbol'] == 'AAPL'
    assert row['units'] == '10'
    assert row['cost'] == '100.00'
    assert row['latest_price'] == 150.00
    assert row['book_value'] == 1000.00,  'book_value = 10 x 100.00'
    assert row['market_value'] == 1500.00, 'market_value = 10 x 150.00'
    assert row['gain_loss'] == 500.00,    'gain_loss = 1500.00 - 1000.00'
    assert row['change'] == 0.50,         'change = 500.00 / 1000.00'


