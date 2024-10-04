#!/usr/bin/env python3

"""
Python script for combining several journal abbreviation lists
and producing an alphabetically sorted list. If the same journal
names are repeated, only the version found first is retained.

This version of the script specifically combines the lists following the ISO4
standard WITHOUT dots after abbreviated words.

Usage: combine_journal_lists.py
Input: see list of files below
Output: writes file 'journalList_dotless.csv'
"""

import csv
import json
from pathlib import Path
import re
import sys

# Define the list of CSV files
import_order = [
    "journals/journal_abbreviations_entrez.csv",
    "journals/journal_abbreviations_medicus.csv",
    "journals/journal_abbreviations_webofscience-dotless.csv",
]


def load_data(file_paths):
    """Load and combine data from CSV files."""
    journal_dict = {}
    normalized_keys = set()
    for path in file_paths:
        with open(path, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                name = row[0].strip()
                abbr = row[1].strip()

                # Discard entries where name or abbr is missing
                if not (name and abbr):
                    continue
                # Discard entries that are too long or too short
                if len(name) >= 80 or len(name) <= 3:
                    continue
                # Discard names that start with non-alphanumeric characters
                if not name[0].isalnum():
                    continue
                # Discard names that consist only of numbers
                if name.replace(" ", "").isnumeric():
                    continue
                # Discard names containing \
                if name.count("\\"):
                    continue
                # Discard entries where the first letters of name and abbr do not match
                if abbr[0] != name.replace("The", "").replace("A ", "")[0]:
                    continue
                # Only keep the first occurrence
                if name in journal_dict:
                    continue
                # Generate normalizedKey, keeping only the first match
                normalized_key = normalize_name(name)
                if normalized_key in normalized_keys:
                    continue

                journal_dict[name] = abbr
                normalized_keys.add(normalized_key)  # Add to the set of used keys
    return journal_dict


def normalize_name(name):
    """
    Normalize the journal name by removing specified characters using regex.
    See src/utils/str.ts -> normalizeKey()
    """
    return re.sub(r"\b(the|and)\b|[&\-:, ()]", "", name, flags=re.IGNORECASE).lower()


def save_to_json(data, output_file):
    """Save the data to a JSON file."""
    with open(output_file, mode="w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=2, ensure_ascii=False)


def save_to_csv(data, output_file):
    """Save the data to a CSV file."""
    with open(output_file, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file, quoting=1)
        for name, abbr in data.items():
            writer.writerow([name, abbr])


def main(filename):
    base_path = Path().cwd()
    output_filename = base_path / filename
    import_paths = [base_path / file for file in import_order]

    journal_data = load_data(import_paths)
    sorted_journal_data = dict(sorted(journal_data.items()))  # Sort alphabetically
    save_to_csv(sorted_journal_data, output_filename)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "journalList_dotless.csv"

    main(filename)
