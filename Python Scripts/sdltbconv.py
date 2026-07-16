#!/usr/bin/env python
# coding: utf-8
"""
This tool converts glossaries from the Trados Studio format (sdltb) to other formats.
"""

from meza import io
from pathlib import Path
import sys
import re

def process(filename):
    tsv_filename = filename[:-5] + "txt"
    tsv = open(tsv_filename, "w")
    try:
        for row in io.read_mdb(filename, table="mtConcepts"):
            source, destination = re.findall("<t>(.+?)<\/t>", row["text"])
            tsv.write(f"{source}\t{destination}\n")
    except ValueError:
        pass
    tsv.close()

def processxml(filename):
    import xml.etree.ElementTree as et
    tsv_filename = filename[:-5] + "txt"
    tsv = open(tsv_filename, "w")
    try:
        for row in io.read_mdb(filename, table="mtConcepts"):
            root = et.fromstring(row["text"])
            source, destination = [term.text for term in root.findall(".//t")]
            tsv.write(f"{source}\t{destination}\n")
    except RuntimeError:
        pass
    tsv.close()


if __name__ == "__main__":
    for filename in sys.argv[1:]:
        if Path(filename).exists() and Path(filename).suffix == ".sdltb":
            process(filename)
        else:
            print(f"Invalid file: {filename}")
