import os
import re
import sys
import itertools
import csv

# Path to the journals folder (change this path accordingly)
JOURNALS_FOLDER_PATH = "./journals/"

# Error tracking
def error(message):
    print(f"ERROR: {message}")
    sys.exit(1)

# Warning tracking
def warning(message):
    print(f"WARN: {message}")

# Check if non-UTF8 characters are present in the file
def check_non_utf8_characters(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            f.read()
    except UnicodeDecodeError:
        error(f"File {filepath} contains non-UTF8 characters")

# Check if there are wrong escape characters in abbreviation entries
def check_wrong_escape(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for line_number, row in enumerate(reader, start=1):
            for field in row:
                if re.search(r"[a-zA-Z]*\\[,\"]", field):
                    error(f"Wrong escape character found in file {filepath} at line {line_number}: {field}")

# Check for wrong beginning letters in journal abbreviations
def check_wrong_beginning_letters(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for line_number, row in enumerate(reader, start=1):
            if row[0].startswith("\""):
                error(f"Wrong beginning letter found in file {filepath} at line {line_number}: {row[0]}")

# Check for duplicate entries
def check_duplicates(filepath):
    entries = set()
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for line_number, row in enumerate(reader, start=1):
            line = ','.join(row)
            if line in entries:
                warning(f"Duplicate entry found in file {filepath} at line {line_number}: {line}")
            else:
                entries.add(line)

# Check if abbreviation and full form are the same
def check_full_form_identical_to_abbreviation(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for line_number, row in enumerate(reader, start=1):
            if len(row) == 2 and row[0].strip() == row[1].strip():
                warning(f"Abbreviation is the same as full form in file {filepath} at line {line_number}: {row[0]}")

# Check for outdated abbreviations
def check_outdated_abbreviations(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for line_number, row in enumerate(reader, start=1):
            if "Manage." in row and "Manag." not in row:
                warning(f"Outdated abbreviation used in file {filepath} at line {line_number}: {','.join(row)}")

if __name__ == "__main__":
    if not os.path.exists(JOURNALS_FOLDER_PATH):
        print("Journals folder not found. Please make sure the path is correct.")
        sys.exit(1)
    
    # Iterate through all CSV files in the journals folder
    for filename in os.listdir(JOURNALS_FOLDER_PATH):
        if filename.endswith(".csv"):
            filepath = os.path.join(JOURNALS_FOLDER_PATH, filename)
            
            # Run the checks
            check_non_utf8_characters(filepath)
            check_wrong_escape(filepath)
            check_wrong_beginning_letters(filepath)
            check_duplicates(filepath)
            check_full_form_identical_to_abbreviation(filepath)
            check_outdated_abbreviations(filepath)
    
    print("Quality check completed.")