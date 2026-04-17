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


