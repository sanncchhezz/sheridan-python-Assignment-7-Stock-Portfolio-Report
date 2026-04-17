"""
Generates performance reports for your stock portfolio.
"""
import argparse
import csv
from collections import OrderedDict
import requests


def main():
    """
    Entrypoint into program.
    """
  


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


def get_market_data(stocks_list):
    """
    Get the latest market data for the given stock symbols
    """
    


def calculate_metrics(input_file, market_data):
    """
    Calculates the various metrics of each of the stocks
    """
    


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
