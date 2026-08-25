#!/usr/bin/env python3
"""
Compute top lemmas for the tagged TED Talks corpus.

Expected input structure:
    corpus/02_tagged/
        text1.txt
        text2.txt
        ...

Typical usage:

    python keylemmas.py \
        --input corpus/02_tagged \
        --output-top corpus/03_toplemmas \
        --output-kw corpus/04_kw_selected \
        --max-total 1000
"""

import argparse
import os
import re
from collections import defaultdict


# POS tags to keep: nouns, proper nouns, main verbs, adjectives.
VALID_TAG_PREFIXES = ("NN", "NP", "VB", "JJ")

# Lemmas to exclude after lowercasing.
STOPWORDS = {
    "be",
    "have",
    "do",
}

def is_valid_lemma_shape(lemma):
    """
    Return True if a lowercased lemma has valid lexical shape.

    Valid lemmas must:

    1. contain at least two alphabetic characters overall;
    2. consist of one or more alphabetic parts;
    3. use hyphens only internally, between alphabetic parts.
    """
    parts = lemma.split("-")

    # Reject empty string, leading hyphen, trailing hyphen, and repeated hyphens.
    if any(not part for part in parts):
        return False

    # Reject digits, punctuation, spaces, underscores, apostrophes, etc.
    if any(not all(ch.isalpha() for ch in part) for part in parts):
        return False

    return sum(1 for ch in lemma if ch.isalpha()) >= 2


def load_lemma_counts(base_dir):
    """
    Load overall lemma counts for the corpus.

    Returns:
        dict: lemma -> count
    """
    counts = defaultdict(int)

    for root, dirs, files in os.walk(base_dir):
        for filename in files:
            if not filename.endswith(".txt"):
                continue

            path = os.path.join(root, filename)

            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.rstrip("\n").split("\t")

                    if len(parts) < 3:
                        continue

                    word, tag, lemma = parts[:3]

                    # Keep only nouns, proper nouns, main verbs, and adjectives.
                    if not tag.startswith(VALID_TAG_PREFIXES):
                        continue

                    # If lemma is <unknown>, use the wordform.
                    lemma = lemma.strip()
                    if lemma == "<unknown>" or not lemma:
                        lemma = word.strip()

                    lemma_lc = lemma.lower()

                    # Lemma must have valid lexical shape.
                    if not is_valid_lemma_shape(lemma_lc):
                        continue

                    if lemma_lc in STOPWORDS:
                        continue

                    counts[lemma_lc] += 1

    return counts


def main():
    parser = argparse.ArgumentParser(
        description="Compute top lemmas for the TED Talks corpus."
    )
    parser.add_argument(
        "--input",
        default="corpus/02_tagged",
        help="Directory containing tagged text files.",
    )
    parser.add_argument(
        "--output-top",
        default="corpus/03_toplemmas",
        help="Output directory for the top lemmas TSV list.",
    )
    parser.add_argument(
        "--output-kw",
        default="corpus/04_kw_selected",
        help="Output directory for the keywords text file.",
    )
    parser.add_argument(
        "--max-total",
        default=1000,
        type=int,
        help="Maximum number of top keywords to select.",
    )

    args = parser.parse_args()

    base_dir = args.input
    output_top_dir = args.output_top
    output_kw_dir = args.output_kw
    max_total = args.max_total

    if max_total <= 0:
        raise ValueError("--max-total must be positive")

    if not os.path.isdir(base_dir):
        raise FileNotFoundError(f"Input directory does not exist: {base_dir}")

    os.makedirs(output_top_dir, exist_ok=True)
    os.makedirs(output_kw_dir, exist_ok=True)

    print(f"Processing texts in {base_dir}...")

    counts = load_lemma_counts(base_dir)

    # Sort lemmas by frequency descending
    sorted_lemmas = sorted(counts.items(), key=lambda x: x[1], reverse=True)

    # 1. Save toplemmas.tsv
    outpath_tsv = os.path.join(output_top_dir, "toplemmas.tsv")
    with open(outpath_tsv, "w", encoding="utf-8") as f:
        f.write("lemma\tcount\n")
        for lemma, count in sorted_lemmas:
            f.write(f"{lemma}\t{count}\n")

    print(f"Saved {outpath_tsv} with {len(sorted_lemmas)} distinct valid lemmas.")

    # 2. Save keywords.txt
    selected_lemmas = sorted_lemmas[:max_total]
    outpath_kw = os.path.join(output_kw_dir, "keywords.txt")
    with open(outpath_kw, "w", encoding="utf-8") as f:
        for lemma, _ in selected_lemmas:
            f.write(f"{lemma}\n")

    print(f"Saved {outpath_kw} with the top {len(selected_lemmas)} lemmas.")


if __name__ == "__main__":
    main()