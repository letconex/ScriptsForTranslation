#!/usr/bin/env python
# coding: utf-8


"""
This tool converts translation memories from the Trados Studio format (sdltm) to the
tmx format, which can be used by any CAT tool, like OmegaT.
"""


from pathlib import Path
import sqlite3
import sys
import xml.etree.ElementTree as et


def convert_date(date_and_time):
    """
    Converts a date in the sdtlm format (which is, in fact, a SQLite date field with the
    format "2021-02-13 18:11:35") to the tmx one ("20210213T181135Z").
    """
    just_date, just_time = date_and_time.split()
    year, month, day = just_date.split("-")
    hour, minute, second = just_time.split(":")
    return f"{year}{month}{day}T{hour}{minute}{second}Z"


def process(filename):
    """
    Reads the contents of the file with the filename given as an argument and creates a
    tmx file with the same path and filename but with a different extension (".tmx").
    """
    c = sqlite3.connect(filename).cursor()
    sql = "SELECT source_segment FROM translation_units LIMIT 1"
    c.execute(sql)
    source_root = et.fromstring(c.fetchone()[0])
    source_language = source_root.find("CultureName").text
    tmx_filename = filename[:-5] + "tmx"
    tmx_root = et.Element("tmx", {"version": "1.4"})
    tmx_root.append(
        et.Element(
            "header",
            {
                "creationtool": "sdltm2tmx",
                "creationtoolversion": "1.0",
                "segtype": "sentence",
                "o-tmf": "SDLTM",
                "adminlang": "en",
                "srclang": source_language,
                "datatype": "unknown",
            },
        )
    )
    body = et.Element("body")
    sql = """SELECT source_segment,
                    target_segment,
                    creation_date,
                    creation_user,
                    change_date,
                    change_user,
                    last_used_date,
                    usage_counter
             FROM translation_units"""
    for row in c.execute(sql):
        (
            source_segment,
            target_segment,
            creation_date,
            creation_user,
            change_date,
            change_user,
            last_used_date,
            usage_counter,
        ) = row
        source_root = et.fromstring(source_segment)
        target_root = et.fromstring(target_segment)
        tu = et.Element(
            "tu",
            {
                "creationdate": convert_date(creation_date),
                "creationid": creation_user,
                "changedate": convert_date(change_date),
                "changeid": change_user,
                "lastuseddate": convert_date(last_used_date),
                "usagecount": str(usage_counter),
            },
        )
        tuv = et.Element(
            "tuv",
            {
                "xml:lang": source_root.find("CultureName").text,
            },
        )
        seg = et.Element("seg")
        seg.text = source_root.find(".//Value").text
        tuv.append(seg)
        tu.append(tuv)
        tuv = et.Element(
            "tuv",
            {
                "xml:lang": target_root.find("CultureName").text,
            },
        )
        seg = et.Element("seg")
        seg.text = target_root.find(".//Value").text
        tuv.append(seg)
        tu.append(tuv)
        body.append(tu)

    tmx_root.append(body)
    tmx = et.ElementTree(tmx_root)
    tmx.write(tmx_filename, encoding="UTF-8")
    c.close()


if __name__ == "__main__":
    for filename in sys.argv[1:]:
        if Path(filename).exists() and Path(filename).suffix == ".sdltm":
            process(filename)
        else:
            print(f"Invalid file: {filename}")
