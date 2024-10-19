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
            for line_number, line in enumerate(f, start=1):
                try:
                    line.encode('utf-8')
                except UnicodeEncodeError as e:
                    error(f"Non-UTF8 character found in {filepath} at line {line_number}: {e}", 'ERROR Non-UTF8')
    except UnicodeDecodeError as e:
        error(f"File {filepath} contains non-UTF-8 characters: {e}", 'ERROR Non-UTF8')

# Check if there are wrong escape characters in abbreviation entries
def check_wrong_escape(filepath):
    valid_escapes = {'\\', '\n', '\t', '\r', '\"'}
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for line_number, row in enumerate(reader, start=1):
            for field in row:
                matches = re.findall(r"\\.", field)
                for match in matches:
                    if match not in valid_escapes:
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
    full_name_entries = {}
    abbreviation_entries = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for line_number, row in enumerate(reader, start=1):
            if len(row) < 2:
                continue

            full_name = row[0].strip()
            abbreviation = row[1].strip()
            
            # Check for duplicate full names or abbreviations
            if full_name in full_name_entries or abbreviation in abbreviation_entries:
                warning(f"Duplicate found in {filepath} at line {line_number}: Full Name: '{full_name}', Abbreviation: '{abbreviation}', first instance seen at line {full_name_entries.get(full_name) or abbreviation_entries.get(abbreviation)}", 'WARN Duplicate FullName/Abbreviation')
            else:
                full_name_entries[full_name] = line_number
                abbreviation_entries[abbreviation] = line_number

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
    with open(SUMMARY_FILE_PATH, 'w', encoding='utf-8') as summary_file:
        # Write summary table with visual symbols
        summary_file.write("# Quality Check Summary Report\n\n")
        summary_file.write("| Status        | Count |\n")
        summary_file.write("| ------------- | ----- |\n")
        summary_file.write(f"| 🔍 Total Issues      | {total_issues}   |\n")
        summary_file.write(f"| ❌ Errors Found      | {sum(error_counts.values())}    |\n")
        summary_file.write(f"| ⚠️ Warnings Found    | {sum(warning_counts.values())}   |\n\n")

        # Write detailed errors and warnings
        if errors or warnings:
            summary_file.write("## Errors per Input File\n\n")
            files = set([msg.split(' in ')[1].split(' at ')[0] for _, msg in errors + warnings])
            for file in files:
                summary_file.write(f"### Issues in file `{file}`\n")
                file_errors = [msg for err_type, msg in errors if file in msg]
                file_warnings = [msg for warn_type, msg in warnings if file in msg]
                if file_errors:
                    summary_file.write("#### Errors:\n")
                    for err in file_errors:
                        summary_file.write(f"- {err.split('ERROR: ')[1]}\n")
                if file_warnings:
                    summary_file.write("#### Warnings:\n")
                    for warn in file_warnings:
                        summary_file.write(f"- {warn.split('WARN: ')[1]}\n")
                summary_file.write("\n")
        else:
            summary_file.write("Quality check completed with no errors or warnings.\n")

    # Print summary and set exit code
    if sum(error_counts.values()) > 0:
        sys.exit(1)  # Fail with an exit code if errors are found
    else:
        sys.exit(0)  # Exit successfully if no errors