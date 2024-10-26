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

# After generating the summary, write to the GITHUB_STEP_SUMMARY file if available
def write_to_github_summary():
    github_summary_path = os.getenv('GITHUB_STEP_SUMMARY')
    if github_summary_path:
        with open(github_summary_path, 'w', encoding='utf-8') as summary_file:
            summary_file.writelines(summary_output)

# Error tracking
def error(message, error_type):
    errors.append((error_type, f"ERROR: {message}"))
    error_counts[error_type] += 1

# Warning tracking
def warning(message, warning_type):
    warnings.append((warning_type, f"WARN: {message}"))
    warning_counts[warning_type] += 1

# Perform all checks on the file's content
def perform_checks(filepath, rows):
    check_non_utf8_characters(filepath, rows)
    check_wrong_escape(filepath, rows)
    check_wrong_beginning_letters(filepath, rows)
    check_duplicates(filepath, rows)
    check_full_form_identical_to_abbreviation(filepath, rows)
    check_outdated_abbreviations(filepath, rows)

# Load the content of a CSV file into memory once
def load_csv_content(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return list(csv.reader(f))
    except UnicodeDecodeError as e:
        error(f"File {filepath} contains non-UTF-8 characters: {e}", 'ERROR Non-UTF8')
        return []

# Check if non-UTF8 characters are present in the file
def check_non_utf8_characters(filepath, rows):
    for line_number, row in enumerate(rows, start=1):
        try:
            str(row).encode('utf-8')
        except UnicodeEncodeError as e:
            error(f"Non-UTF8 character found in {filepath} at line {line_number}: {e}", 'ERROR Non-UTF8')

# Check if there are wrong escape characters in abbreviation entries
def check_wrong_escape(filepath, rows):
    valid_escapes = {'\\', '\n', '\t', '\r', '\"'}
    for line_number, row in enumerate(rows, start=1):
        for field in row:
            matches = re.findall(r"\\.", field)
            for match in matches:
                if match not in valid_escapes:
                    error(f"Wrong escape in {filepath} line {line_number}: {field}", 'ERROR Wrong Escape')

# Check for wrong beginning letters in journal abbreviations
def check_wrong_beginning_letters(filepath, rows):
    # Words that are typically ignored when creating abbreviations
    ignore_words = {
        'a', 'an', 'and', 'the', 'of', 'or', 'in', 'on', 'at', 'to', 'for', 'with', 'by', 
        'la', 'el', 'le', 'et', 'der', 'die', 'das', 'dem', 'und', 'für'  # Articles in multiple languages
    }
    
    # Special cases for abbreviations
    special_cases = {
        'proceedings': ['p', 'proc'],
        'or': ['or'],
        'spie': ['spie'],
        'notes': ['notes']
    }

    def clean_text(text):
        # Remove special characters except periods (important for compound abbreviations)
        # and normalize spaces
        cleaned = re.sub(r'[^\w\s\.]', ' ', text)
        return ' '.join(filter(None, cleaned.lower().split()))

    def split_compound_abbrev(abbrev):
        # Split abbreviation that might contain compound parts (e.g., "Nat.forsch")
        parts = []
        for part in abbrev.split():
            # Split on periods but keep them with the preceding part
            subparts = [sp for sp in re.split(r'(?<=\.)(?=[^\.])', part) if sp]
            parts.extend(subparts)
        return parts

    def get_significant_words(text):
        # Split text into words and filter out ignore words
        return [w for w in clean_text(text).split() if w.lower() not in ignore_words]

    def is_compound_word_match(full_word, abbrev_part):
        # Handle compound word abbreviations (e.g., "Nat.forsch" matching "Naturforschenden")
        if '.' in abbrev_part:
            # Split the compound abbreviation
            abbrev_subparts = abbrev_part.split('.')
            # Get the first few characters of the full word to match against first part
            word_start = full_word[:len(abbrev_subparts[0])]
            
            # For the second part (if exists), try to find it within the remaining word
            if len(abbrev_subparts) > 1 and abbrev_subparts[1]:
                remaining_word = full_word[len(abbrev_subparts[0]):]
                return (word_start.lower() == abbrev_subparts[0].lower() and 
                       abbrev_subparts[1].lower() in remaining_word.lower())
            
            return word_start.lower() == abbrev_subparts[0].lower()
        return False

    def is_valid_abbreviation(full_name, abbrev):
        # Clean and split both strings
        full_words = get_significant_words(full_name)
        abbrev_parts = split_compound_abbrev(clean_text(abbrev))
        
        # Handle cases where abbreviation is the same as full name
        if clean_text(full_name) == clean_text(abbrev):
            return True

        # Handle special cases
        for special_word, valid_abbrevs in special_cases.items():
            if special_word in full_words:
                if any(va in abbrev_parts for va in valid_abbrevs):
                    return True

        # Track matched parts and their positions
        matched_parts = 0
        used_full_words = set()
        
        for abbrev_part in abbrev_parts:
            found_match = False
            
            # Try matching against each full word
            for i, full_word in enumerate(full_words):
                if i in used_full_words:
                    continue
                
                # Check for compound word match
                if is_compound_word_match(full_word, abbrev_part):
                    found_match = True
                    matched_parts += 1
                    used_full_words.add(i)
                    break
                
                # Check for regular abbreviation patterns
                elif (full_word.lower().startswith(abbrev_part.lower()) or
                      (len(abbrev_part) >= 2 and abbrev_part[0].lower() == full_word[0].lower())):
                    found_match = True
                    matched_parts += 1
                    used_full_words.add(i)
                    break

        # Consider the abbreviation valid if we matched most parts
        min_required_matches = max(1, len(abbrev_parts) * 0.5)
        return matched_parts >= min_required_matches

    for line_number, row in enumerate(rows, start=1):
        if len(row) >= 2:
            full_name = row[0].strip()
            abbreviation = row[1].strip()
            
            if not is_valid_abbreviation(full_name, abbreviation):
                error(
                    f"Wrong abbreviation in {filepath} line {line_number}:"
                    f"\nFull: '{full_name}',"
                    f"\nAbbr: '{abbreviation}'",
                    'ERROR Wrong Starting Letter')


# Check for duplicate entries
def check_duplicates(filepath, rows):
    full_name_entries = {}
    abbreviation_entries = {}

    for line_number, row in enumerate(rows, start=1):
        if len(row) < 2:
            continue

        full_name = row[0].strip()
        abbreviation = row[1].strip()
        
        # Check for duplicate full names or abbreviations
        if full_name in full_name_entries or abbreviation in abbreviation_entries:
            warning(f"Duplicate in {filepath} line {line_number}: Full: '{full_name}', Abbr: '{abbreviation}', first seen in line {full_name_entries.get(full_name) or abbreviation_entries.get(abbreviation)}", 'WARN Duplicate FullName/Abbreviation')
        else:
            full_name_entries[full_name] = line_number
            abbreviation_entries[abbreviation] = line_number

# Check if abbreviation and full form are the same
def check_full_form_identical_to_abbreviation(filepath, rows):
    for line_number, row in enumerate(rows, start=1):
        if len(row) == 2 and row[0].strip() == row[1].strip() and ' ' in row[0].strip():
            warning(f"Abbr same as Full in {filepath} line {line_number}: {row[0]}", 'WARN Same Abbreviation as Full Name')

# Check for outdated abbreviations
def check_outdated_abbreviations(filepath, rows):
    for line_number, row in enumerate(rows, start=1):
        if "Manage." in row and "Manag." not in row:
            warning(f"Outdated abbr in {filepath} line {line_number}: {','.join(row)}", 'WARN Outdated Manage Abbreviation')

# Main entry point
if __name__ == "__main__":
    if not os.path.exists(JOURNALS_FOLDER_PATH):
        print("Journals folder not found. Please make sure the path is correct.")
        sys.exit(1)

    # Iterate through all CSV files in the journals folder
    for filename in os.listdir(JOURNALS_FOLDER_PATH):
        if filename.endswith(".csv"):
            filepath = os.path.join(JOURNALS_FOLDER_PATH, filename)
            
            # Load the CSV content once
            rows = load_csv_content(filepath)

            # Run all checks on the loaded data
            if rows:
                perform_checks(filepath, rows)
    
    # Write the summary to a file
    total_issues = sum(error_counts.values()) + sum(warning_counts.values())
    summary_output = []

    summary_output.append("# Quality Check Summary Report\n")
    summary_output.append("| Status        | Count |\n")
    summary_output.append("| ------------- | ----- |\n")
    summary_output.append(f"| 🔍 Total       | {total_issues}   |\n")
    summary_output.append(f"| ❌ Errors      | {sum(error_counts.values())}    |\n")
    summary_output.append(f"| ⚠️ Warnings    | {sum(warning_counts.values())}   |\n\n")

    # Write detailed errors and warnings
    if errors or warnings:
        summary_output.append("## Errors per Input File\n\n")
        files = set([msg.split(' in ')[1].split(' at ')[0] for _, msg in errors + warnings])
        for file in files:
            summary_output.append(f"### Issues in file `{file}`\n")
            file_errors = [msg for err_type, msg in errors if file in msg]
            file_warnings = [msg for warn_type, msg in warnings if file in msg]
            if file_errors:
                summary_output.append("#### Errors:\n")
                for err in file_errors:
                    summary_output.append(f"- {err.split('ERROR: ')[1]}\n")
            if file_warnings:
                summary_output.append("#### Warnings:\n")
                for warn in file_warnings:
                    summary_output.append(f"- {warn.split('WARN: ')[1]}\n")
            summary_output.append("\n")
    else:
        summary_output.append("Quality check completed with no errors or warnings.\n")

    # Write the summary to a file
    with open(SUMMARY_FILE_PATH, 'w', encoding='utf-8') as summary_file:
        summary_file.writelines(summary_output)

    # Print the summary to console
    for line in summary_output:
        print(line, end='')

    # Write to GitHub Actions summary, if available
    write_to_github_summary()
    
    # Set exit code based on errors
    if sum(error_counts.values()) > 0:
        sys.exit(1)  # Fail with an exit code if errors are found
    else:
        sys.exit(0)  # Exit successfully if no errors