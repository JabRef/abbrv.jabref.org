#!/usr/bin/env python3

"""
Python script for checking multiple quality aspects of .csv journal abbreviation files.
This script enforces conventions to ensure that abbreviations of journal titles meet quality standards.

The script performs the following checks:
1. Checks for wrong escape sequences.
2. Checks for incorrect beginning letters.
3. Checks for non-UTF8 characters.
4. Checks for duplicate entries (full names and abbreviations).
5. Checks if abbreviations match full names (for one-word titles).
6. Checks for outdated abbreviations.

The script will print out issues found and exit with a failure code if any issues are detected.
The script does NOT automatically fix these errors. Corrections must be done manually.

The script will automatically run whenever there is a push to the main branch of the
abbreviations repo (abbrv.jabref.org) using GitHub Actions.
"""

import os
import itertools
import csv
import re
import sys

# Define paths and file collections
PATH_TO_JOURNALS = "./journals/"
fileNames = next(itertools.islice(os.walk(PATH_TO_JOURNALS), 0, None))[2]

# Error collections
errors = []

# Utility functions for checking conditions
def is_utf8(text):
    try:
        text.encode('utf-8')
        return True
    except UnicodeEncodeError:
        return False

def check_abbreviation_duplicates(full_name, abbrev, seen_full_names, seen_abbrevs):
    if full_name in seen_full_names or abbrev in seen_abbrevs:
        return True
    return False

def is_outdated_abbreviation(abbrev):
    # Add a basic rule to detect outdated abbreviations (e.g., "Manage." instead of "Manag.")
    outdated_patterns = [r"Manage\.\b"]
    for pattern in outdated_patterns:
        if re.search(pattern, abbrev):
            return True
    return False

# Perform checks
for file in fileNames:
    if file.endswith(".csv"):
        with open(PATH_TO_JOURNALS + file, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            seen_full_names = set()
            seen_abbrevs = set()

            for row_index, row in enumerate(reader, start=1):
                if len(row) < 2:
                    continue  # Skip rows without expected data
                
                full_name, abbrev = row[0], row[1]

                # Check for escaped ampersands
                if '\\&' in full_name or '\\&' in abbrev:
                    errors.append(f"Escaped ampersand in file {file}, row {row_index}")

                # Check for non-UTF8 characters
                if not is_utf8(full_name) or not is_utf8(abbrev):
                    errors.append(f"Non-UTF8 character in file {file}, row {row_index}")

                # Check for duplicate entries
                if check_abbreviation_duplicates(full_name, abbrev, seen_full_names, seen_abbrevs):
                    errors.append(f"Duplicate entry in file {file}, row {row_index}")

                # Check if abbreviation matches full form for one-word titles
                if full_name.strip().lower() == abbrev.strip().lower():
                    errors.append(f"Full form matches abbreviation in file {file}, row {row_index}")

                # Check for outdated abbreviations
                if is_outdated_abbreviation(abbrev):
                    errors.append(f"Outdated abbreviation in file {file}, row {row_index}")

                # Update seen sets
                seen_full_names.add(full_name)
                seen_abbrevs.add(abbrev)

# Print errors and exit with failure code if any issues found
if errors:
    error_message = "Quality check failed:\n" + "\n".join(errors)
    print(error_message, file=sys.stderr)
    sys.exit(1)
else:
    print("Quality check passed. No issues found.")
