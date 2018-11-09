import os
import urllib.request
import csv

csv_file_path = 'mathscinet.csv'
urllib.request.urlretrieve('https://mathscinet.ams.org/msnhtml/annser.csv', csv_file_path)

with open(csv_file_path, mode='r') as csv_file, open('journal_abbreviations_mathematics.txt', mode='w') as abbreviations_file:
    abbreviations_file = csv.writer(abbreviations_file, delimiter='=', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            # print(f'Column names are {", ".join(row)}')
            line_count += 1

        abbreviations_file.writerow([row["Full Title"], row["Abbrev"]])
        # print(f'\t{row["Full Title"]} abbreviated {row["Abbrev"]}')
        line_count += 1

    print(f'Processed {line_count} lines.')
