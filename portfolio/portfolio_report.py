"""
Generates performance reports for your stock portfolio.
"""
import argparse
import csv
import os
from collections import OrderedDict
import requests


def main():
    """
    Entrypoint into the portfolio report program.

    Orchestrates the full pipeline in four steps:
      1. Parse --source and --target file paths from the command line.
      2. Read the portfolio CSV from --source into a list of dicts.
      3. Fetch current market data from the IEX API for all symbols.
      4. Calculate performance metrics for each stock.
      5. Save the enriched report to the --target CSV file.
    """
    args = get_args()
    portfolio = read_portfolio(args.source)
    symbols = [row['symbol'] for row in portfolio]
    market_data = get_market_data(symbols)
    report = calculate_metrics(portfolio, market_data)
    save_portfolio(report, args.target)


def read_portfolio(filename):
    """
    Reads a CSV portfolio file and returns its rows as an ordered list of dicts.

    Each row in the CSV becomes an OrderedDict whose keys are the column headers
    (symbol, units, cost) and whose values are strings, preserving the original
    column order defined in the file header.

    Args:
        filename: Path (str or pathlib.Path) to the input CSV file.

    Returns:
        A list of OrderedDict objects, one per data row in the CSV.
    """
    with open(filename, newline='') as file:
        reader = csv.DictReader(file)
        return [OrderedDict(row) for row in reader]


def get_args(args=None):
    """
    Parses and returns command-line arguments for the portfolio report tool.

    Defines two required flags:
      --source  Path to the input CSV file containing the portfolio data.
      --target  Path to the output CSV file where the report will be saved.

    The optional args parameter allows a list of strings to be passed directly
    (e.g. in tests), instead of reading from sys.argv at runtime.

    Args:
        args: List of argument strings, or None to read from sys.argv.

    Returns:
        An argparse.Namespace object with attributes: source, target.
    """
    parser = argparse.ArgumentParser(description='Generate a stock portfolio performance report.')
    parser.add_argument('--source', required=True, help='Path to the input portfolio CSV file.')
    parser.add_argument('--target', required=True, help='Path to the output report CSV file.')
    return parser.parse_args(args)


IEX_BASE_URL = 'https://cloud.iexapis.com/stable/tops'


def get_market_data(stocks_list):
    """
    Fetches the latest market quote data for a list of stock symbols
    from the IEX Cloud API and returns it as a dict keyed by symbol.

    Sends a single batch request to the IEX /tops endpoint with all
    symbols joined by commas. The API token is read from the IEX_TOKEN
    environment variable. Symbols not present in the API response (e.g.
    invalid tickers) are simply absent from the returned dict — no error
    is raised.

    Args:
        stocks_list: List of stock symbol strings (e.g. ['AAPL', 'AMZN']).

    Returns:
        A dict mapping each symbol string to its full market data dict,
        e.g. {'AAPL': {'symbol': 'AAPL', 'price': 186.84, ...}, ...}.
    """
    token = os.environ.get('IEX_TOKEN', '')
    symbols = ','.join(stocks_list)
    response = requests.get(IEX_BASE_URL, params={'token': token, 'symbols': symbols})
    market_data = {item['symbol']: item for item in response.json()}

    for symbol in stocks_list:
        if symbol not in market_data:
            print(f'Warning: symbol "{symbol}" was not found in market data and will be skipped.')

    return market_data


def calculate_metrics(input_file, market_data):
    """
    Calculates performance metrics for each stock in the portfolio.

    For each row in input_file, looks up the stock's current price in
    market_data and computes the following fields:
      latest_price  - current market price from the API
      book_value    - units x cost (total amount originally paid)
      market_value  - units x latest_price (current total value)
      gain_loss     - market_value - book_value (profit or loss)
      change        - gain_loss / book_value (return as a decimal ratio)

    Stocks whose symbol is absent from market_data are skipped silently
    (get_market_data already printed a warning for those).

    Args:
        input_file:  List of dicts with keys symbol, units, cost (strings).
        market_data: Dict keyed by symbol from get_market_data().

    Returns:
        A list of dicts each containing all 8 output columns.
    """
    results = []
    for row in input_file:
        symbol = row['symbol']
        if symbol not in market_data:
            continue
        units = float(row['units'])
        cost = float(row['cost'])
        latest_price = market_data[symbol]['price']
        book_value = units * cost
        market_value = units * latest_price
        gain_loss = market_value - book_value
        change = gain_loss / book_value
        results.append({
            'symbol': symbol,
            'units': row['units'],
            'cost': row['cost'],
            'latest_price': latest_price,
            'book_value': book_value,
            'market_value': market_value,
            'gain_loss': gain_loss,
            'change': change,
        })
    return results


def save_portfolio(output_data, filename):
    """
    Writes a list of dicts to a CSV file with CRLF line endings.

    The column headers are derived from the keys of the first dict in
    output_data, so the column order matches the order of those keys.
    Opening the file with newline='' prevents Python from adding an extra
    carriage return on top of the one the csv module already writes,
    ensuring correct CRLF (\\r\\n) line endings on all platforms.

    Args:
        output_data: List of dicts where each dict represents one CSV row.
        filename: Path (str or pathlib.Path) to the output CSV file.
    """
    fieldnames = output_data[0].keys()
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_data)


if __name__ == '__main__':
    main()
