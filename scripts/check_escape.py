#!/usr/bin/env python3

"""
Python script for checking if all escape sequences in .csv journal abbreviation files are
valid. This convention is enforced to ensure that abbreviations of journal titles
can be processed without error.

The script will raise a ValueError() in case invalid escape sequences are found, and will
also provide the row and column in which they were found (1-indexed). The script does
NOT automatically fix these errors. This should be done manually.

The script will automatically run whenever there is a push to the main branch of the
abbreviations repo (abbrv.jabref.org) using GitHub Actions.
"""

import os
import itertools
import re

# Get all file names in journal folders
PATH_TO_JOURNALS = "./journals/"
fileNames = next(itertools.islice(os.walk(PATH_TO_JOURNALS), 0, None))[2]

# Store ALL locations of invalid escape sequences so they can all be printed upon failure
errFileNames = []
errRows = []
errCols = []
errSequences = []
errDescriptions = []

# Pattern to find problematic escape sequences
# We're looking for backslashes followed by characters that form invalid escape sequences
# Focus on common problems: incomplete LaTeX commands and malformed escapes

for file in fileNames:
    if (file.endswith(".csv")):
        # For each .csv file in the folder, open in read mode
        with open(PATH_TO_JOURNALS + file, "r", encoding='utf-8', errors='ignore') as f:
            for i, line in enumerate(f):
                # Look for specific problematic patterns
                problematic_patterns = [
                    (r'\\c(?![primeyrd])', 'incomplete LaTeX command - should be \\cyr or \\cprime'),
                    (r'\\p(?!olhk)', 'incomplete LaTeX command - should be \\polhk'),
                    (r'\\l(?!dots|asp)', 'incomplete LaTeX command'),
                    (r'\\-', 'invalid hyphen escape - use regular hyphen'),
                    (r'\\"[^,"]', 'improper quote escaping'),
                    (r'\\(?![\\"/nrt$&]|sp|rm|circledR|cprime|cyr|polhk|cdprime|ldots|lasp)[a-zA-Z]+', 'unknown escape sequence'),
                ]
                
                for pattern, description in problematic_patterns:
                    matches = re.finditer(pattern, line)
                    for match in matches:
                        # Skip if we're inside a mathematical expression (between $ signs)
                        line_before_match = line[:match.start()]
                        line_after_match = line[match.end():]
                        dollar_count_before = line_before_match.count('$')
                        dollar_count_after = line_after_match.count('$')
                        
                        # If we have an odd number of $ before and after, we're inside math - allow it
                        if (dollar_count_before % 2 == 1) and (dollar_count_after % 2 == 1):
                            continue
                            
                        errFileNames.append(file)
                        errRows.append(i + 1)
                        errCols.append(match.start() + 1)
                        errSequences.append(match.group())
                        errDescriptions.append(description)

# In the case where we do find invalid escape sequences, the len() will be non-zero
if (len(errFileNames) > 0):
    err_msg = "["
    # For each file, append every row:col location to the error message
    for i, fname in enumerate(errFileNames):
        err_msg += "(" + fname + ", " + \
            str(errRows[i]) + ":" + str(errCols[i]) + ", '" + errSequences[i] + "' - " + errDescriptions[i] + "), "
    # Format end of string and return as Value Error to 'fail' GitHub Actions process
    err_msg = err_msg[:len(err_msg) - 2]
    err_msg += "]"
    raise ValueError("Found Invalid Escape Sequences at: " + err_msg)
