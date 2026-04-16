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
    Parse and return command line argument values
    """
    


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
    Saves data to a CSV file
    """
    


if __name__ == '__main__':
    main()
