# ============================================================
# Project pipeline for CL-ST2 Phase 4
#
# Run this script from the project phase directory, e.g.:
#
#   cl_st2_ph4_elaine/
#
# The pipeline prepares the corpus, selects keywords, builds the
# SAS input files, generates post-SAS factor outputs, creates
# visualisations and examples, and finally prepares/interprets
# factor-pole prompts.
# ============================================================


# ------------------------------------------------------------
# 1. Tag the source corpus
#
# Reads the phase corpus and produces token/tag/lemma files
# grouped by year.
# ------------------------------------------------------------

python tag.py
# Output: corpus/02_tagged/<Year>/


# ------------------------------------------------------------
# 2. Extract key lemmas by year
#
# Uses the tagged corpus to identify decade-level key lemmas.
# The cutoff controls the minimum threshold for retaining lemmas.
# ------------------------------------------------------------

python keylemmas.py \
    --input corpus/02_tagged \
    --output corpus/03_keylemmas \
    --cutoff 3
# Output: corpus/08_keylemmas/<Decade>.tsv


# ------------------------------------------------------------
# 3. Select a stratified keyword set
#
# Selects up to 250 keywords per year, with a maximum of 1200
# keywords before final de-duplication. The final keyword list is
# used to construct binary keyword columns for SAS.
# ------------------------------------------------------------

# Run 1 - Considering lowercase alphabetic characters,
# optionally joined by internal hyphens

python select_kws_stratified.py \
    --per-year 40 \
    --max-total 1200
# Output: corpus/04_kw_selected/keywords.txt

"
=== Year Keyword Quotas ===
1984   → 40 keywords max
1990   → 40 keywords max
1994   → 40 keywords max
1998   → 40 keywords max
2001   → 40 keywords max
2002   → 40 keywords max
2003   → 40 keywords max
2004   → 40 keywords max
2005   → 40 keywords max
2006   → 40 keywords max
2007   → 40 keywords max
2008   → 40 keywords max
2009   → 40 keywords max
2010   → 40 keywords max
2011   → 40 keywords max
2012   → 40 keywords max
2013   → 40 keywords max
2014   → 40 keywords max
2015   → 40 keywords max
2016   → 40 keywords max
2017   → 40 keywords max
2018   → 40 keywords max
2019   → 40 keywords max
2020   → 40 keywords max
2021   → 40 keywords max
2022   → 40 keywords max
2023   → 40 keywords max
2024   → 40 keywords max
2025   → 40 keywords max
=============================

1984   → selected 40/40 from 206 available POSKW lemmas
1990   → selected 40/40 from 409 available POSKW lemmas
1994   → selected 40/40 from 116 available POSKW lemmas
1998   → selected 40/40 from 543 available POSKW lemmas
2001   → selected 40/40 from 557 available POSKW lemmas
2002   → selected 40/40 from 1194 available POSKW lemmas
2003   → selected 40/40 from 1169 available POSKW lemmas
2004   → selected 40/40 from 1124 available POSKW lemmas
2005   → selected 40/40 from 1004 available POSKW lemmas
2006   → selected 40/40 from 530 available POSKW lemmas
2007   → selected 40/40 from 452 available POSKW lemmas
2008   → selected 40/40 from 515 available POSKW lemmas
2009   → selected 40/40 from 215 available POSKW lemmas
2010   → selected 40/40 from 281 available POSKW lemmas
2011   → selected 40/40 from 161 available POSKW lemmas
2012   → selected 40/40 from 132 available POSKW lemmas
2013   → selected 40/40 from 95 available POSKW lemmas
2014   → selected 40/40 from 103 available POSKW lemmas
2015   → selected 40/40 from 108 available POSKW lemmas
2016   → selected 40/40 from 154 available POSKW lemmas
2017   → selected 40/40 from 126 available POSKW lemmas
2018   → selected 40/40 from 57 available POSKW lemmas
2019   → selected 40/40 from 122 available POSKW lemmas
2020   → selected 40/40 from 425 available POSKW lemmas
2021   → selected 40/40 from 201 available POSKW lemmas
2022   → selected 40/40 from 244 available POSKW lemmas
2023   → selected 40/40 from 213 available POSKW lemmas
2024   → selected 40/40 from 323 available POSKW lemmas
2025   → selected 40/40 from 513 available POSKW lemmas

Total consolidated keywords before de-duplication: 1160
Unique keywords after de-duplication: 1056
Duplicates removed: 104

Final unique keywords written to: corpus/04_kw_selected/keywords.txt
Final unique keyword count: 1056
"


# ------------------------------------------------------------
# 4. Build binary keyword columns
#
# Remove previous generated column folders before rebuilding them.
# This keeps the keyword matrix consistent with the latest selected
# keyword list.
# ------------------------------------------------------------

rm -rf columns columns_clean

python columns.py
# Outputs:
#   columns/
#   columns_clean/
#   file_ids.txt
#   index_keywords.txt


# ------------------------------------------------------------
# 5. Merge columns into the SAS counts matrix
#
# Combines the per-text keyword columns into the space-separated
# counts file expected by the SAS LMDA workflow.
# ------------------------------------------------------------

python merge_columns.py
# Output: sas/counts.txt


# ------------------------------------------------------------
# 6. Generate SAS format files
#
# Creates SAS label/format files that map keyword variable IDs
# such as v000001 to readable word labels.
# ------------------------------------------------------------

python sas_formats.py
# Outputs:
#   sas/word_labels_format.sas
#   sas/word_labels_full_format.sas
#   other SAS helper format files


# ------------------------------------------------------------
# Run SAS
# ------------------------------------------------------------


# ------------------------------------------------------------
# 8. Build factor loading lists
#
# Reads SAS factor outputs and produces readable positive/negative
# loading lists for each factor.
# ------------------------------------------------------------

python factor_lists.py
# Output: factors/


# ------------------------------------------------------------
# 9. Calculate corpus size summaries
#
# Produces corpus-size metadata for reporting and checking balance
# across decades.
# ------------------------------------------------------------

python corpus_size.py
# Output: corpus_size/corpus_size.tsv


# ------------------------------------------------------------
# 10. Generate LaTeX/TikZ boxplots
#
# Creates one boxplot per factor dimension and a combined mosaic
# for use in slides or reports.
# ------------------------------------------------------------

cd latex_boxplots

python latex_boxplots.py
# Output: latex_boxplots/slides/

cd ..


# ------------------------------------------------------------
# 11. Generate LaTeX ANOVA table
#
# Summarises year effects for each factor using F, p, R², and
# percent R².
# ------------------------------------------------------------

python latex_anova_table.py
# Output: latex_tables/anova_year.tex


# ------------------------------------------------------------
# 12. Generate LaTeX example extracts
#
# Selects representative high-scoring texts by factor pole and
# decade, then writes LaTeX examples with factor-loading lemmas
# highlighted.
# ------------------------------------------------------------

python examples.py
# Output: examples/


# ------------------------------------------------------------
# 13. Generate score-details report
#
# Sanity-check report showing, for each text and factor, which
# positive- and negative-pole loading words are present.
# ------------------------------------------------------------

python score_details.py
# Output: examples/score_details.txt


# ------------------------------------------------------------
# 14. Generate plaintext example extracts
#
# Produces plain `.txt` versions of the selected examples, including
# score metadata and loading words. These are useful for manual review
# and for building interpretation prompts.
# ------------------------------------------------------------

python examples_txt.py
# Output: examples_txt/


# ------------------------------------------------------------
# 15. Build interpretation prompts
#
# Combines factor loadings, mean decade scores, plaintext examples,
# and score-details information into one prompt per factor pole.
# ------------------------------------------------------------

python interpretation_prompts.py
# Output: interpretation/input/


# ------------------------------------------------------------
# 16. Submit interpretation prompts to GPT
#
# Sends each prompt file to the configured GPT model and writes one
# response file per factor pole. Requires OPENAI_API_KEY in the
# environment or in env/.env.
# ------------------------------------------------------------

python generate_interpretation_gpt.py \
    --input interpretation/input \
    --output interpretation/output \
    --model gpt-5.5 \
    --workers 4
# Output: interpretation/output/