#!/usr/bin/env python3

"""
Python script for combining several journal abbreviation lists
and producing an alphabetically sorted list. If the same journal
names are repeated, only the version found last is retained.

Usage: combine_journal_lists.py out_file in_file1 in_file2 ...
"""

import sys

out_file = sys.argv[1]
journal_dict = {}

for in_file in sys.argv[2:]:
    count = 0
    f = open(in_file, "r")
    for line in f:
        if ";" in line and line[0] != "#":
            count = count+1
            parts = line.partition(";")
            journal_dict[parts[0].strip()] = line.strip()
    f.close()
    print(f"{in_file}: {count}")

print(f"Combined key count: {len(journal_dict)}")

f = open(out_file, "w")
for key in sorted(journal_dict.keys()):
    f.write(journal_dict[key]+"\n")
f.close()
