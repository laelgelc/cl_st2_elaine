#!/usr/bin/env python3
"""
select_kws_stratified.py

Selects a balanced, year-stratified subset of positive keywords (POSKW)
from key-lemma tables produced by keylemmas.py.

In this project, the strata are years:

    2020
    2021
    2022
    2023
    2024
    2025

The strata are of the same nature, so each year receives the same maximum
keyword quota. There is no human/non-human weighting.

What it does
------------
1) Reads every year key-lemma file in corpus/03_keylemmas/.
   Supported extensions: .tsv and .txt.

2) Extracts lemmas whose final column is POSKW, applying lexical filters
   aligned with the upstream key-lemma extraction stage:
   - keep alphabetic lemmas and valid hyphenated compounds;
   - allow Unicode alphabetic characters, including accented letters;
   - allow hyphens only internally, between alphabetic parts;
   - drop lemmas containing digits;
   - drop lemmas containing uppercase letters;
   - drop lemmas containing punctuation other than valid internal hyphens.

3) Applies the same quota to every year:
   - each year: at most --per-year lemmas.

4) Builds a consolidated list in chronological year order.

5) Optionally truncates the consolidated list to --max-total before
   de-duplication.

6) Writes outputs to corpus/04_kw_selected/:
   - one file per year: <year>.txt
   - one consolidated, de-duplicated list: keywords.txt

Typical usage
-------------
python select_kws_stratified.py \
    --per-year 250 \
    --max-total 1200
"""

import argparse
import glob
import os
import re


INPUT_DIR = "corpus/03_keylemmas"
OUTPUT_DIR = "corpus/04_kw_selected"

YEAR_RE = re.compile(r"^\d{4}$")
SUPPORTED_EXTENSIONS = (".tsv", ".txt")


# -----------------------------------------------------------
# Helpers
# -----------------------------------------------------------

def natural_sort_key(text):
    """Return a natural-sort key that treats digit runs as integers."""
    parts = re.split(r"(\d+)", text)
    return [int(part) if part.isdigit() else part.lower() for part in parts]


def is_valid_lemma_shape(lemma):
    """
    Return True if a lemma has valid lexical shape.

    Valid lemmas must:

    1. contain at least two alphabetic characters overall;
    2. consist of one or more alphabetic parts;
    3. use hyphens only internally, between alphabetic parts.

    This deliberately allows Unicode alphabetic characters, including accented
    letters, because it relies on str.isalpha() rather than an ASCII-only regex.

    Examples kept:
        car
        tv
        built-in
        black-and-white
        close-up
        café
        prêt-à-porter

    Examples rejected:
        a
        1
        .
        tvdays.com
        display**
        build-in.
        built-
        -built
        1950s-style
    """
    parts = lemma.split("-")

    # Reject empty string, leading hyphen, trailing hyphen, and repeated hyphens.
    if any(not part for part in parts):
        return False

    # Reject digits, punctuation, spaces, underscores, apostrophes, etc.
    if any(not all(ch.isalpha() for ch in part) for part in parts):
        return False

    return sum(1 for ch in lemma if ch.isalpha()) >= 2


def is_clean_lemma(lemma):
    """
    Return True if lemma passes lexical filtering rules.

    The filtering is aligned with the upstream key-lemma extraction stage:
    lowercase alphabetic parts are allowed, valid internal hyphens are allowed,
    and Unicode alphabetic characters are supported.
    """
    if any(ch.isupper() for ch in lemma):
        return False

    return is_valid_lemma_shape(lemma)


def discover_keylemma_files(input_dir):
    """Return year-named key-lemma files from the input directory."""
    if not os.path.isdir(input_dir):
        raise FileNotFoundError(f"Input directory does not exist: {input_dir}")

    files = []

    for extension in SUPPORTED_EXTENSIONS:
        files.extend(glob.glob(os.path.join(input_dir, f"*{extension}")))

    year_files = {}

    for filepath in files:
        stem = os.path.splitext(os.path.basename(filepath))[0]

        if not YEAR_RE.match(stem):
            continue

        # Prefer .tsv if both .tsv and .txt exist for the same year.
        existing = year_files.get(stem)
        if existing is None:
            year_files[stem] = filepath
        elif filepath.endswith(".tsv") and existing.endswith(".txt"):
            year_files[stem] = filepath

    if not year_files:
        raise FileNotFoundError(
            f"No year key-lemma files found in {input_dir}. "
            "Expected files such as 2020.tsv, 2021.tsv, etc."
        )

    return [
        (year, year_files[year])
        for year in sorted(year_files, key=natural_sort_key)
    ]


def load_poskw(filepath):
    """
    Load POSKW lemmas from a key-lemma file.

    The file may be tab-separated or whitespace-separated.
    The first column is assumed to be the lemma.
    The final column is assumed to be the status.
    """
    lemmas = []

    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if not lines:
        return lemmas

    for line in lines[1:]:  # skip header
        line = line.strip()

        if not line:
            continue

        if "\t" in line:
            parts = line.split("\t")
        else:
            parts = line.split()

        if len(parts) < 2:
            continue

        lemma = parts[0].strip()
        status = parts[-1].strip()

        if status != "POSKW":
            continue

        if not is_clean_lemma(lemma):
            continue

        lemmas.append(lemma)

    return lemmas


def write_word_list(path, words):
    """Write one word per line."""
    with open(path, "w", encoding="utf-8") as fout:
        for word in words:
            fout.write(word + "\n")


# -----------------------------------------------------------
# Main
# -----------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Select balanced POSKW keyword lists across year strata."
    )
    parser.add_argument(
        "--input",
        default=INPUT_DIR,
        help="Input directory containing year key-lemma files.",
    )
    parser.add_argument(
        "--output",
        default=OUTPUT_DIR,
        help="Output directory for selected keyword lists.",
    )
    parser.add_argument(
        "--per-year",
        type=int,
        required=True,
        help="Maximum number of POSKW lemmas to select from each year.",
    )
    parser.add_argument(
        "--max-total",
        type=int,
        default=0,
        help=(
            "Optional maximum consolidated keyword count before de-duplication. "
            "Use 0 for no maximum."
        ),
    )

    args = parser.parse_args()

    if args.per_year <= 0:
        raise ValueError("--per-year must be greater than 0")

    if args.max_total < 0:
        raise ValueError("--max-total must be non-negative")

    os.makedirs(args.output, exist_ok=True)

    keylemma_files = discover_keylemma_files(args.input)

    # Load all year strata.
    strata = {}

    for year, filepath in keylemma_files:
        strata[year] = load_poskw(filepath)

    print("=== Year Keyword Quotas ===")
    for year in sorted(strata, key=natural_sort_key):
        print(f"{year:<6} → {args.per_year} keywords max")
    print("=============================\n")

    # Per-year selection.
    selected_by_year = {}

    for year in sorted(strata, key=natural_sort_key):
        lemmas = strata[year]
        chosen = lemmas[:args.per_year]
        selected_by_year[year] = chosen

        print(
            f"{year:<6} → selected {len(chosen)}/{args.per_year} "
            f"from {len(lemmas)} available POSKW lemmas"
        )

    # Build consolidated list in chronological year order.
    consolidated = []

    for year in sorted(selected_by_year, key=natural_sort_key):
        consolidated.extend(selected_by_year[year])

    # Enforce optional max_total before de-duplication.
    if args.max_total and len(consolidated) > args.max_total:
        consolidated = consolidated[:args.max_total]

    unique_lemmas = sorted(set(consolidated))

    total_count = len(consolidated)
    unique_count = len(unique_lemmas)

    print(f"\nTotal consolidated keywords before de-duplication: {total_count}")
    print(f"Unique keywords after de-duplication: {unique_count}")
    print(f"Duplicates removed: {total_count - unique_count}")

    # Write per-year outputs.
    for year, words in selected_by_year.items():
        outpath = os.path.join(args.output, f"{year}.txt")
        write_word_list(outpath, words)

    # Write consolidated deduplicated output.
    cons_path = os.path.join(args.output, "keywords.txt")
    write_word_list(cons_path, unique_lemmas)

    print(f"\nFinal unique keywords written to: {cons_path}")
    print(f"Final unique keyword count: {len(unique_lemmas)}")


if __name__ == "__main__":
    main()