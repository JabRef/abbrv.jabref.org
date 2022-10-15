#!/usr/bin/env python3

import os
import itertools

path = "./journals/"

fileNames = next(itertools.islice(os.walk(path), 0, None))[2]

for file in fileNames:
    if (file.endswith(".csv")):
        with open(path + file, "r") as f:
            if ('\&' in f.read()):
                raise ValueError("Found an escaped Ampersand in: " + file)




