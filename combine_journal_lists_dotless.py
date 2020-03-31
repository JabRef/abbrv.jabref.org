#!/usr/bin/env python3

"""
Python script for combining several journal abbreviation lists
and producing an alphabetically sorted list. If the same journal
names are repeated, only the version found last is retained.

This version of the script specifically combines the lists following the ISO4
standard WITHOUT dots after abbreviated words.

Usage: combine_journal_lists.py
Input: see list of files below
Output: writes file 'journalList_dotless.csv'
"""

import sys

import_order = [
  'journals/journal_abbreviations_entrez.csv',
  'journals/journal_abbreviations_medicus.csv',
]

if len(sys.argv) == 1:
    out_file = 'journalList_dotless.csv'
else:
   out_file = sys.argv[1]
print(f"Writing : {out_file}")

journal_dict = {}

for in_file in import_order:
    count = 0
    f = open(in_file, "r")
    for line in f:
        if ";" in line and line[0] != "#":
            count += 1
            parts = line.partition(";")
            journal_dict[parts[0].strip()] = line.strip()
    f.close()
    print(f"{in_file}: {count}")

print(f"Combined key count: {len(journal_dict)}")

f = open(out_file, "w")
for key in sorted(journal_dict.keys()):
    f.write(journal_dict[key]+"\n")
f.close()
