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


