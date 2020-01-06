#!/usr/bin/env python3

"""
PANTONE FORMULA GUIDE COATED SCRAPER v.1.0.

Scrape two pieces of colour data for each colour in the Pantone Book
'Formula Guide Coated'.

EXAMPLE COLOUR DATA:

   1. pColorCode - number e.g. 2995C
   2. ctl00_cphContent_ctl00_divHEXValues - hex value e.g. 00A9E0

REFERENCE:

Formula Guide Coated Book:
https://www.pantone.com/color-finder#/pick?pantoneBook=pantoneSolidCoatedV3M2

Formula Guide Coated  - Example Colour:
https://www.pantone.com/color-finder/2995-C

"""

import os
import time

from bs4 import BeautifulSoup
import requests

# Root URL.
COLOUR_FINDER_URL = 'https://www.pantone.com/color-finder'

"""
Regarding Pantone formula guide coated colours (from the Pantone Website):

    The majority of these colors are referred to using a three- or four-digit
    number followed by a C or U. There are also a small number of named colors,
    such as the 18 base colors like PANTONE Reflex Blue C or
    PANTONE Orange 021 U.

For the purposes of this script:

    * Pantone numbered colours are represented as a range in order to catch
      all known codes. The end point was the highest known number at the time
      of writing.
    * Pantone named colours were taken from the index of a physical formula
      guide coated swatchbook, from around 2015-16.
"""

PANTONE_COATED_NUMBERED_COLOURS = range(100, 7772)
PANTONE_COATED_NAMED_COLOURS = [
    'Black C', 'Black 0961 C', 'Black 2 C', 'Black 3 C', 'Black 4 C',
    'Black 5 C', 'Black 6 C', 'Black 7 C', 'Blue 072 C', 'Blue 0821 C',
    'Bright Red C', 'Cool Gray 1 C', 'Cool Gray 2 C', 'Cool Gray 3 C',
    'Cool Gray 4 C', 'Cool Gray 5 C', 'Cool Gray 6 C', 'Cool Gray 7 C',
    'Cool Gray 8 C', 'Cool Gray 9 C', 'Cool Gray 10 C', 'Cool Gray 11 C',
    'Dark Blue C', 'Green C', 'Green 0921 C', 'Magenta 0521 C',
    'Medium Purple C', 'Orange 021 C', 'Pink C', 'Process Blue C', 'Purple C',
    'Red 032 C', 'Red 0331 C', 'Reflex Blue C', 'Rhodamine Red C', 'Violet C',
    'Violet 0631 C', 'Warm Gray 1 C', 'Warm Gray 2 C', 'Warm Gray 3 C',
    'Warm Gray 4 C', 'Warm Gray 5 C', 'Warm Gray 6 C', 'Warm Gray 7 C',
    'Warm Gray 8 C', 'Warm Gray 9 C', 'Warm Gray 10 C', 'Warm Gray 11 C',
    'Warm Red C', 'Yellow C', 'Yellow 012 C', 'Yellow 0131 C'
    ]

# Set output directory to the location of this script.
OUTPUT_DIR = os.path.abspath(os.path.dirname(__file__))
CSV_FILE_NAME = 'pantone_formula_guide_coated.csv'


def get_colour_url_from_name(colour_finder_url, name):
    """
    Build a URL to a named colour in the Pantone Formula Guide Coated.

    Returns:
        str: Usually Alphanumeric

    """
    name = name.replace(' ', '-')
    colour_url = f'{colour_finder_url}/{name}'
    return colour_url


def get_colour_url_from_number(colour_finder_url, number):
    """
    Build a URL to a numbered colour in the Pantone Formula Guide Coated.

    Returns:
        str: Alphanumeric

    """
    number = str(number)
    colour_url = f'{colour_finder_url}/{number}-C'
    return colour_url


def get_colour_code(soup):
    """
    Get the Pantone colour code.

    Returns:
        str: Usually alphanumeric.

    """
    colour_code = soup.find(attrs={'class': 'pColorCode'})
    if colour_code is not None:
        colour_code = colour_code.text.strip()
        return colour_code


def get_colour_hex(soup):
    """
    Get the colour hexadecimal value.

    Returns:
        str: Alphanumeric

    """
    colour_hex = soup.find(attrs={'id': 'ctl00_cphContent_ctl00_divHEXValues'})
    if colour_hex is not None:
        colour_hex = colour_hex.text.strip()
        return colour_hex


def scrape_colour(colour):
    """
    Build a URL based on input colour code & scrape the URL.

    Returns:
        tuple

    """
    # Handle colours passed in as integers or alphanumeric strings.
    try:
        if int(colour):
            colour = str(colour)
            colour_url = get_colour_url_from_number(COLOUR_FINDER_URL, colour)
    except ValueError:
        colour_url = get_colour_url_from_name(COLOUR_FINDER_URL, colour)
    # Scrape the colour URL.
    response = requests.get(colour_url)
    # Test the connection, proceed if successful.
    if response:
        # Parse the html w/BeautifulSoup for a nested data structure.
        soup = BeautifulSoup(response.text, 'html.parser')
        colour_code = get_colour_code(soup)
        colour_hex = get_colour_hex(soup)
        return colour_code, colour_hex


def prepare_csv_file(directory, name):
    """
    Open an existing, or create a new csv file in the specified directory.

    Returns:
        An open csv file in append mode.

    """
    csv_file_path = os.path.join(directory, name)
    if os.path.exists(csv_file_path) and os.path.isfile(csv_file_path):
        csv_file = open(csv_file_path, 'a')
    elif not os.path.exists(csv_file_path):
        csv_file = open(csv_file_path, 'a')
    return csv_file


def main():
    """Run the main program."""
    csv_file = prepare_csv_file(OUTPUT_DIR, CSV_FILE_NAME)
    for i in PANTONE_COATED_NAMED_COLOURS:
        colour_data = scrape_colour(i)
        if colour_data[0] is not None and colour_data[1] is not None:
            colour_code = colour_data[0]
            colour_hex = colour_data[1]
            print(f'Colour data obtained: {colour_code} / {colour_hex}')
            csv_file.write(f'{colour_code}, {colour_hex}, \n')
            print(f'Colour data written to {CSV_FILE_NAME}')
            time.sleep(1)
    for i in PANTONE_COATED_NUMBERED_COLOURS:
        colour_data = scrape_colour(i)
        if colour_data[0] is not None and colour_data[1] is not None:
            colour_code = colour_data[0]
            colour_hex = colour_data[1]
            print(f'Colour data obtained: {colour_code} / {colour_hex}')
            csv_file.write(f'{colour_code}, {colour_hex}, \n')
            print(f'Colour data written to {CSV_FILE_NAME}')
            time.sleep(1)
    print('Scraping is complete.')


if __name__ == "__main__":
    main()
