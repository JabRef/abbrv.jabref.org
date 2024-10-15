#!/usr/bin/env python3

import pandas as pd
import csv
import requests
from io import StringIO
import os
print(os.getcwd())

file_in = "https://mathscinet.ams.org/msnhtml/annser.csv"
file_out = "../journals/journal_abbreviations_mathematics.csv"

# set user agent to mimic browser request
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
response = requests.get(file_in, headers=headers)

if response.status_code == 200:
    df_new = pd.read_csv(StringIO(response.text), usecols=[0, 1]).dropna()[["Full Title", "Abbrev"]]
else:
    raise Exception(f"Failed to fetch the file. Status code: {response.status_code}")

# Get our last mathematics data file
df_old = pd.read_csv(file_out, sep=",", escapechar="\\",
                     header=None, names=["Full Title", "Abbrev"])

# Concatenate, remove duplicates and sort by journal name
df = pd.concat([df_new, df_old], axis=0).drop_duplicates(
).sort_values(by=["Full Title", "Abbrev"])

# Remove values where journal name is equal to abbreviation
df = df[df["Full Title"].str.lower() != df["Abbrev"].str.lower()]

# Save the end file in the same path as the old one
df.to_csv(file_out, sep=",", escapechar="\\", index=False, header=False, quoting=csv.QUOTE_ALL)
