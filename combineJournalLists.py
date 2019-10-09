#!/usr/bin/python

# Python script for combining several journal abbreviation lists
# and producing an alphabetically sorted list. If the same journal
# names are repeated, only the version found last is retained.
#
# Usage: combineJournalLists.py outfile infile1 infile2 ...

import sys

outFile = sys.argv[1]
journal_dict = {}

for i in range(2,len(sys.argv)):
    count = 0
    f = open(sys.argv[i], "r")
    for line in f:
        if "=" in line and line[0] != "#":
            count = count+1
            parts = line.partition("=")
            journal_dict[parts[0].strip()] = line.strip()
    f.close()
    print(sys.argv[i]+": "+str(count))

print("Combined key count: "+str(len(journal_dict)))

f = open(outFile, "w")
for key in sorted(journal_dict.keys()):
    f.write(journal_dict[key]+"\n")
f.close()
