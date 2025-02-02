import os
import re
import sys
import itertools
import csv
from collections import defaultdict

# Path to the journals folder (change this path accordingly)
JOURNALS_FOLDER_PATH = "./journals/"
SUMMARY_FILE_PATH = "./check_quality_summary.txt"

class QualityChecker:
    def __init__(self):
        # Use defaultdict to avoid key existence checks
        self.error_counts = defaultdict(int)
        self.warning_counts = defaultdict(int)
        # Store issues by file for more efficient grouping
        self.issues_by_file = defaultdict(lambda: {'errors': [], 'warnings': []})
        
    def error(self, filepath, message, error_type):
        self.error_counts[error_type] += 1
        # Remove filepath from message if it's included
        message = message.replace(f"in {filepath} ", "")
        full_message = f"{error_type}: {message}"
        self.issues_by_file[filepath]['errors'].append(full_message)

    def warning(self, filepath, message, warning_type):
        self.warning_counts[warning_type] += 1
        # Remove filepath from message if it's included
        message = message.replace(f"in {filepath} ", "")
        full_message = f"{warning_type}: {message}"
        self.issues_by_file[filepath]['warnings'].append(full_message)

    def write_summary(self, summary_lines):
        # Write to file in a single operation
        with open(SUMMARY_FILE_PATH, 'w', encoding='utf-8') as summary_file:
            summary_file.writelines(summary_lines)

        # Print to console in chunks
        for line in summary_lines:
            print(line, end='')

        # Write to GitHub Actions summary if available
        github_summary_path = os.getenv('GITHUB_STEP_SUMMARY')
        if github_summary_path:
            with open(github_summary_path, 'w', encoding='utf-8') as summary_file:
                summary_file.writelines(summary_lines)

    def check_non_utf8_characters(self, filepath, rows):
        for line_number, row in enumerate(rows, start=1):
            try:
                str(row).encode('utf-8')
            except UnicodeEncodeError as e:
                self.error(
                    filepath, 
                    f"at line {line_number}: {e}",
                    'ERROR Non-UTF8'
                )

    def check_wrong_escape(self, filepath, rows):
        valid_escapes = {'\\', '\n', '\t', '\r', '\"'}
        for line_number, row in enumerate(rows, start=1):
            for field in row:
                matches = re.findall(r"\\.", field)
                for match in matches:
                    if match not in valid_escapes:
                        self.error(
                            filepath,
                            f"at line {line_number}: {field}",
                            'ERROR Wrong Escape'
                        )

    def check_wrong_beginning_letters(self, filepath, rows):
        # Words that are typically ignored when creating abbreviations
        ignore_words = {
            'a', 'an', 'and', 'the', 'of', 'or', 'in', 'on', 'at', 'to', 'for', 'with', 'by', 
            'la', 'el', 'le', 'et', 'der', 'die', 'das', 'dem', 'und', 'für'
        }
        
        # Special cases for abbreviations
        special_cases = {
            'proceedings': ['p', 'proc'],
            'or': ['or'],
            'spie': ['spie'],
            'notes': ['notes']
        }

        def clean_text(text):
            cleaned = re.sub(r'[^\w\s\.]', ' ', text)
            return ' '.join(filter(None, cleaned.lower().split()))

        def split_compound_abbrev(abbrev):
            parts = []
            for part in abbrev.split():
                subparts = [sp for sp in re.split(r'(?<=\.)(?=[^\.])', part) if sp]
                parts.extend(subparts)
            return parts

        def get_significant_words(text):
            return [w for w in clean_text(text).split() if w.lower() not in ignore_words]

        def is_compound_word_match(full_word, abbrev_part):
            if '.' in abbrev_part:
                abbrev_subparts = abbrev_part.split('.')
                word_start = full_word[:len(abbrev_subparts[0])]
                
                if len(abbrev_subparts) > 1 and abbrev_subparts[1]:
                    remaining_word = full_word[len(abbrev_subparts[0]):]
                    return (word_start.lower() == abbrev_subparts[0].lower() and 
                           abbrev_subparts[1].lower() in remaining_word.lower())
                
                return word_start.lower() == abbrev_subparts[0].lower()
            return False

        def is_valid_abbreviation(full_name, abbrev):
            full_words = get_significant_words(full_name)
            abbrev_parts = split_compound_abbrev(clean_text(abbrev))
            
            if clean_text(full_name) == clean_text(abbrev):
                return True

            for special_word, valid_abbrevs in special_cases.items():
                if special_word in full_words:
                    if any(va in abbrev_parts for va in valid_abbrevs):
                        return True

            matched_parts = 0
            used_full_words = set()
            
            for abbrev_part in abbrev_parts:
                found_match = False
                
                for i, full_word in enumerate(full_words):
                    if i in used_full_words:
                        continue
                    
                    if is_compound_word_match(full_word, abbrev_part):
                        found_match = True
                        matched_parts += 1
                        used_full_words.add(i)
                        break
                    
                    elif (full_word.lower().startswith(abbrev_part.lower()) or
                          (len(abbrev_part) >= 2 and abbrev_part[0].lower() == full_word[0].lower())):
                        found_match = True
                        matched_parts += 1
                        used_full_words.add(i)
                        break

            min_required_matches = max(1, len(abbrev_parts) * 0.5)
            return matched_parts >= min_required_matches

        for line_number, row in enumerate(rows, start=1):
            if len(row) >= 2:
                full_name = row[0].strip()
                abbreviation = row[1].strip()
                
                if not is_valid_abbreviation(full_name, abbreviation):
                    self.error(
                        filepath,
                        f"at line {line_number} Full: '{full_name}', Abbr: '{abbreviation}'",
                        'ERROR Wrong Abbreviation'
                    )

    def check_duplicates(self, filepath, rows):
        full_name_entries = {}
        abbreviation_entries = {}

        for line_number, row in enumerate(rows, start=1):
            if len(row) < 2:
                continue

            full_name = row[0].strip()
            abbreviation = row[1].strip()
            
            if full_name in full_name_entries or abbreviation in abbreviation_entries:
                self.warning(
                    filepath,
                    f"at line {line_number} Full: '{full_name}', Abbr: '{abbreviation}', first seen in line {full_name_entries.get(full_name) or abbreviation_entries.get(abbreviation)}",
                    'WARN Duplicate FullName/Abbreviation'
                )
            else:
                full_name_entries[full_name] = line_number
                abbreviation_entries[abbreviation] = line_number

    def check_full_form_identical_to_abbreviation(self, filepath, rows):
        for line_number, row in enumerate(rows, start=1):
            if len(row) == 2 and row[0].strip() == row[1].strip() and ' ' in row[0].strip():
                self.warning(
                    filepath,
                    f"at line {line_number}: {row[0]}",
                    'WARN Same Abbrev. as Full Name'
                )

    def check_outdated_abbreviations(self, filepath, rows):
        for line_number, row in enumerate(rows, start=1):
            if "Manage." in row and "Manag." not in row:
                self.warning(
                    filepath,
                    f"at line {line_number}: {','.join(row)}",
                    'WARN Outdated Manage Abbreviation'
                )

    def perform_checks(self, filepath, rows):
        self.check_non_utf8_characters(filepath, rows)
        self.check_wrong_escape(filepath, rows)
        self.check_wrong_beginning_letters(filepath, rows)
        self.check_duplicates(filepath, rows)
        self.check_full_form_identical_to_abbreviation(filepath, rows)
        self.check_outdated_abbreviations(filepath, rows)

    def generate_summary(self):
        total_issues = sum(self.error_counts.values()) + sum(self.warning_counts.values())
        
        # Pre-allocate list with estimated size
        summary_lines = []
        summary_lines.extend([
            "# Quality Check Summary Report\n",
            "| Status        | Count |\n",
            "| ------------- | ----- |\n",
            f"| 🔍 Total Issues      | {total_issues}   |\n",
            f"| ❌ Errors Found      | {sum(self.error_counts.values())}    |\n",
            f"| ⚠️ Warnings Found    | {sum(self.warning_counts.values())}   |\n\n"
        ])

        # Add detailed error/warning counts
        if self.error_counts:
            summary_lines.append("## Error Counts\n")
            for error_type, count in sorted(self.error_counts.items()):
                summary_lines.append(f"- {error_type}: {count}\n")
            summary_lines.append("\n")

        if self.warning_counts:
            summary_lines.append("## Warning Counts\n")
            for warning_type, count in sorted(self.warning_counts.items()):
                summary_lines.append(f"- {warning_type}: {count}\n")
            summary_lines.append("\n")

        if self.issues_by_file:
            summary_lines.append("## Issues per Input File\n\n")
            for filepath, issues in sorted(self.issues_by_file.items()):
                summary_lines.append(f"### Issues in file `{filepath}`\n")
                if issues['errors']:
                    summary_lines.append("#### Errors:\n")
                    summary_lines.extend(f"- {err}\n" for err in sorted(issues['errors']))
                
                if issues['warnings']:
                    summary_lines.append("#### Warnings:\n")
                    summary_lines.extend(f"- {warn}\n" for warn in sorted(issues['warnings']))
                
                summary_lines.append("\n")
        else:
            summary_lines.append("Quality check completed with no errors or warnings.\n")

        return summary_lines
def main():
    if not os.path.exists(JOURNALS_FOLDER_PATH):
        print("Journals folder not found. Please make sure the path is correct.")
        sys.exit(1)

    checker = QualityChecker()
    
    # Process all files
    for filename in os.listdir(JOURNALS_FOLDER_PATH):
        if filename.endswith(".csv"):
            filepath = os.path.join(JOURNALS_FOLDER_PATH, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    rows = list(csv.reader(f))
                    checker.perform_checks(filepath, rows)
            except UnicodeDecodeError as e:
                checker.error(filepath, f"File contains non-UTF8 characters: {e}", 'ERROR Non-UTF8')

    # Generate and write summary
    summary_lines = checker.generate_summary()
    checker.write_summary(summary_lines)
    
    # Exit with appropriate code
    sys.exit(1 if sum(checker.error_counts.values()) > 0 else 0)

if __name__ == "__main__":
    main()