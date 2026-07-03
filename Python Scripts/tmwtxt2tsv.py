import re
import csv
import sys
import os

if len(sys.argv) < 2:
    print("Usage: python extract_pairs.py <inputfile>")
    sys.exit(1)

input_file = sys.argv[1]
split_tup = input_file.split(".")
file_name = split_tup[0]
file_extension = split_tup[1]

# Regex to capture segments:
seg_pattern = re.compile(r'<Seg L=([A-Z]{2}-[A-Z]{2})>(.*?)\n', re.DOTALL)

pairs = []
current = {}
langs_detected = set()

with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        match = seg_pattern.search(line)
        if match:
            lang = match.group(1)
            text = match.group(2).strip()

            langs_detected.add(lang)

            # store temporarily
            current[lang] = text

            # when we have exactly two languages in a block → save pair
            if len(current) == 2:
                # sort languages alphabetically for consistent ordering
                sorted_langs = sorted(current.keys())
                pairs.append((sorted_langs[0], current[sorted_langs[0]],
                              sorted_langs[1], current[sorted_langs[1]]))
                current = {}

# Build output filename automatically
sorted_langs = sorted(list(langs_detected))
if len(sorted_langs) >= 2:
    output_file = f"{file_name} {sorted_langs[0].split('-')[0]}-{sorted_langs[1].split('-')[0]}.tsv"
else:
    output_file = f"{file_name}.tsv"

# Write TSV
with open(output_file, "w", encoding="utf-8", newline="") as tsv:
    writer = csv.writer(tsv, delimiter="\t")
    # header: language codes
    if len(sorted_langs) >= 2:
        writer.writerow([sorted_langs[0], sorted_langs[1]])
    else:
        writer.writerow(["Lang1", "Lang2"])

    for lang1, text1, lang2, text2 in pairs:
        writer.writerow([text1, text2])

print(f"Extracted {len(pairs)} bilingual pairs → saved to {output_file}")
