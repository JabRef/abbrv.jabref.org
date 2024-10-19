import os
import re
import sys
import itertools
import csv

# Path to the journals folder (change this path accordingly)
JOURNALS_FOLDER_PATH = "./journals/"
SUMMARY_FILE_PATH = "./check_quality_summary.txt"
errors = []
warnings = []

# Error and Warning Counts
error_counts = {
    'ERROR Wrong Escape': 0,
    'ERROR Wrong Starting Letter': 0,
    'ERROR Non-UTF8': 0
}
warning_counts = {
    'WARN Duplicate FullName/Abbreviation': 0,
    'WARN Same Abbreviation as Full Name': 0,
    'WARN Outdated Manage Abbreviation': 0
}
# Error tracking
def error(message, error_type):
    errors.append((error_type, f"ERROR: {message}"))
    error_counts[error_type] += 1

# Warning tracking
def warning(message, warning_type):
    warnings.append((warning_type, f"WARN: {message}"))
    warning_counts[warning_type] += 1

# Check if non-UTF8 characters are present in the file
def check_non_utf8_characters(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            f.read()
    except UnicodeDecodeError:
        error(f"File {filepath} contains non-UTF8 characters", 'ERROR Non-UTF8')

# Check if there are wrong escape characters in abbreviation entries
def check_wrong_escape(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for line_number, row in enumerate(reader, start=1):
            for field in row:
                if re.search(r"[a-zA-Z]*\\[,\"]", field):
                    error(f"Wrong escape character found in {filepath} at line {line_number}: {field}", 'ERROR Wrong Escape')

# Check for wrong beginning letters in journal abbreviations
def check_wrong_beginning_letters(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for line_number, row in enumerate(reader, start=1):
            if row[0].startswith("\""):
                error(f"Wrong beginning letter found in {filepath} at line {line_number}: {row[0]}", 'ERROR Wrong Starting Letter')

# Check for duplicate entries
def check_duplicates(filepath):
    entries = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for line_number, row in enumerate(reader, start=1):
            line = ','.join(row)
            if line in entries:
                warning(f"Duplicate found in {filepath} at line {line_number}: {line}, first instance seen at line {entries[line]}", 'WARN Duplicate FullName/Abbreviation')
            else:
                entries[line] = line_number

# Check if abbreviation and full form are the same
def check_full_form_identical_to_abbreviation(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for line_number, row in enumerate(reader, start=1):
            if len(row) == 2 and row[0].strip() == row[1].strip() and ' ' in row[0].strip():
                warning(f"Abbreviation is the same as full form in {filepath} at line {line_number}: {row[0]}", 'WARN Same Abbreviation as Full Name')

# Check for outdated abbreviations
def check_outdated_abbreviations(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for line_number, row in enumerate(reader, start=1):
            if "Manage." in row and "Manag." not in row:
                warning(f"Outdated abbreviation used in {filepath} at line {line_number}: {','.join(row)}", 'WARN Outdated Manage Abbreviation')

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
    
    # Write the summary to a file
    total_issues = sum(error_counts.values()) + sum(warning_counts.values())
    with open(SUMMARY_FILE_PATH, 'w') as summary_file:
        # Write summary table with vertical headers
        summary_file.write(f"Total: {total_issues}\n")
        summary_file.write(f"ERROR Wrong Escape: {error_counts['ERROR Wrong Escape']}\n")
        summary_file.write(f"ERROR Wrong Starting Letter: {error_counts['ERROR Wrong Starting Letter']}\n")
        summary_file.write(f"ERROR Non-UTF8: {error_counts['ERROR Non-UTF8']}\n")
        summary_file.write(f"WARN Duplicate FullName/Abbreviation: {warning_counts['WARN Duplicate FullName/Abbreviation']}\n")
        summary_file.write(f"WARN Same Abbreviation as Full Name: {warning_counts['WARN Same Abbreviation as Full Name']}\n")
        summary_file.write(f"WARN Outdated Manage Abbreviation: {warning_counts['WARN Outdated Manage Abbreviation']}\n")

        # Write detailed errors and warnings
        if errors or warnings:
            summary_file.write("\nQuality Check Summary:\n")
            for subtitle in [
                'ERROR Wrong Escape', 
                'ERROR Wrong Starting Letter', 
                'ERROR Non-UTF8',
                'WARN Duplicate FullName/Abbreviation',
                'WARN Same Abbreviation as Full Name',
                'WARN Outdated Manage Abbreviation'
            ]:
                # Write subtitle and corresponding messages
                filtered_errors = [err for err_type, err in errors if err_type == subtitle]
                filtered_warnings = [warn for warn_type, warn in warnings if warn_type == subtitle]
                if filtered_errors or filtered_warnings:
                    count = len(filtered_errors) + len(filtered_warnings)
                    summary_file.write(f"\n{subtitle}: with {count} instances\n")
                    for err in filtered_errors:
                        summary_file.write(f"{err}\n")
                    for warn in filtered_warnings:
                        summary_file.write(f"{warn}\n")
        else:
            summary_file.write("\nQuality check completed with no errors or warnings.\n")

    # Print summary and set exit code
    if errors:
        sys.exit(1)
    else:
        print("Quality check completed with no errors.")