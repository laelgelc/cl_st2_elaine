# Corpus Linguistics - Study 2 - Elaine

## Phases 1 and 2

- [TED Talks](https://www.ted.com/talks) data extraction considering the period 2020 to 2025 (raw data extracted on 14/03/2025 at 11:38 am Brasilia).

## Phase 3

- Textual Lexical Multi-Dimensional Analysis

Note: The following error message occurred during the execution of the `sas` function:

```
--- v000571 ---
Inconsistency detected by ld.so: ../sysdeps/x86_64/dl-machine.h: 503: elf_machine_rela_relative: Assertion `ELFW(R_TYPE) (reloc->r_info) == R_X86_64_RELATIVE' failed!
--- v000572 ---
```

Apparently, this error did not affect the execution of the program.

Add a caution note under **Phase 3**, after the existing SAS execution note:

**Caution**: When rerunning `cl_st2_ph3_elaine.sas` in SAS, make sure the SAS session does not contain stale variables or datasets from an earlier run. A previous run produced an inconsistent `cl_st2_ph3_elaine_scores_only.tsv` file that was missing the `fac6` column, even though `cl_st2_ph3_elaine_scores.tsv` correctly included `fac1` through `fac6`. This caused incorrect factor 6 examples. Before rerunning the script, use a fresh SAS session or clear the relevant WORK library objects, then verify that both output files include the expected factor columns.
