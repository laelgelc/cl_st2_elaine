# Corpus Linguistics - Study 2 - Elaine

## Phases 1 and 2 - Data Collection

[TED Talks](https://www.ted.com/talks) data extraction considering years within the period from 1984 to 2025 (raw data extracted on 14/03/2025 at 11:38 am Brasilia).

## Phase 3 - Corpus Compilation and Verbal Lexical Multi-Dimensional Analysis (LMDA)

he resulting verbal target corpus contains a sample of selected TED Talks, with `4315` transcript files across 29 years withing the period from 1984 to 2025.

|   Year    | Text Count |
|:---------:|-----------:|
|   1984    |          1 |
|   1990    |          1 |
|   1994    |          1 |
|   1998    |          6 |
|   2001    |          4 |
|   2002    |         25 |
|   2003    |         31 |
|   2004    |         30 |
|   2005    |         61 |
|   2006    |         41 |
|   2007    |        101 |
|   2008    |         74 |
|   2009    |        200 |
|   2010    |        219 |
|   2011    |        235 |
|   2012    |        253 |
|   2013    |        266 |
|   2014    |        237 |
|   2015    |        237 |
|   2016    |        271 |
|   2017    |        342 |
|   2018    |        261 |
|   2019    |        104 |
|   2020    |        281 |
|   2021    |        294 |
|   2022    |        246 |
|   2023    |        284 |
|   2024    |        205 |
|   2025    |          4 |
| **Total** |   **4315** |

The Lexical Multi-dimensional Analysis (LMDA) was processed according to the corresponding procedures.

Note: The following error message occurred during the execution of the `sas` function:

```
--- v000571 ---
Inconsistency detected by ld.so: ../sysdeps/x86_64/dl-machine.h: 503: elf_machine_rela_relative: Assertion `ELFW(R_TYPE) (reloc->r_info) == R_X86_64_RELATIVE' failed!
--- v000572 ---
```

Apparently, this error did not affect the execution of the program.

Add a caution note under **Phase 3**, after the existing SAS execution note:

**Caution**: When rerunning `cl_st2_ph3_elaine.sas` in SAS, make sure the SAS session does not contain stale variables or datasets from an earlier run. A previous run produced an inconsistent `cl_st2_ph3_elaine_scores_only.tsv` file that was missing the `fac6` column, even though `cl_st2_ph3_elaine_scores.tsv` correctly included `fac1` through `fac6`. This caused incorrect factor 6 examples. Before rerunning the script, use a fresh SAS session or clear the relevant WORK library objects, then verify that both output files include the expected factor columns.

## Phase 4 - Verbal Lexical Multi-Dimensional Analysis Reprocessing

The Lexical Multi-dimensional Analysis (LMDA) was reprocessed according to the corresponding procedures using a more recent Python pipeline.

**Important:**

- The document that contains the target corpus metadata is `cl_st2_ph4_elaine/corpus/00_sources/cl_st2_ph3_elaine_tc_3.xlsx`. The `File` column contains the original filename and the `Text ID` column, the ID with which the file was renamed in the target corpus.
- A total of `1056` lexical variables were selected among key lemmas extracted from the yearly strata of the target corpus.
- Statistical processing data is stored in `cl_st2_ph4_elaine/sas`.
- Examples in human-friendly format are in `cl_st2_ph4_elaine/examples_txt`.
- AI-assisted LMDA interpretation can be found in `cl_st2_ph4_elaine/interpretation`.

### Text score versus number of loading words

In a certain factor pole, text score hardly ever matches the corresponding number of loading words.

```
Text ID: t000003
Year: 1994
File:   corpus/01_ted_talks/1994/t002458.txt

Score (f1_pos): 15
Loading words (f1_pos), N=17: evolution, slide, explosion, evolutionary, abstract, powder, transportation, copy, feeding, oil, rock, the, obscure, object, computer, learning, evolve
```

```
Text ID: t003573
Year: 2021
File:   corpus/01_ted_talks/2021/t004082.txt

Score (f6_neg): 1
Loading words (f6_neg), N=0:
```

Based on the `cl_st2_ph4_elaine/sas/cl_st2_ph4_elaine.sas` SAS script and the `cl_st2_ph4_elaine/sas/output_cl_st2_ph4_elaine/cl_st2_ph4_elaine_scores_only.tsv` data, the reason the score does not match the number of loading words (N) is that the overall Factor Score is a composite value that accounts for **both the positive and negative poles** of that factor.

Here is the explanation:

1. **How the score is calculated:** In the SAS script, `proc score` computes the factor score for each text by multiplying the word presence (which is binary: 0 or 1, based on the `v000000` variables) by the `pole` coefficient (which is `1` for positive loading words and `-1` for negative loading words). 
2. **Resulting Formula:** The score for any factor is essentially:
   `Score = (Count of Positive Pole words) - (Count of Negative Pole words)`

**Looking at your examples:**
* **`t000003` (Factor 1):** You have `N=17` positive loading words, but the overall `Score (f1_pos)` is `15`. This indicates that the text also contains **2 negative loading words** for Factor 1 (17 - 2 = 15).
* **`t003573` (Factor 6):** You have `N=0` negative loading words, but the `Score (f6_neg)` is `1`. This means the text contains **1 positive loading word** for Factor 6 (1 - 0 = 1). 

Because the score represents the net balance between both poles, it will rarely perfectly match the raw count (`N`) of words from just one side of the pole.
