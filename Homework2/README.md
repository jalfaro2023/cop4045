# Python Programming Homework 2

Jorge Alfaro | FAU ID: Z23697022

Solutions for Problems 1-5, including the Problem 3 extra-credit tests.
Use Python 3.10 or newer; no third-party packages are required.

From this directory:

```text
python p1_Alfaro_Jorge.py
python p2_Alfaro_Jorge.py
python p3_Alfaro_Jorge.py
python p4_Alfaro_Jorge.py
cd p5
python p5_Alfaro_Jorge.py observations.csv statistics.csv
python -m unittest -v test_p5.py
```

Problem 1 creates a numbered copy of its own source. Keep the supplied
`testif.py` next to Problem 3 and the three supplied IMDB CSV files next to
Problem 4. Problem 4 prints the first ten entries of each ranking.

The PDF and Word-compatible RTF are drafts. Required output screenshots for
Problems 1-4 and screenshots of each VSCode agent prompt and answer for
Problem 5 must still be inserted. Open the RTF in Word, save as `h2.doc`, and
export an updated `h2.pdf` after completing the evidence.

These drafts were prepared with Codex desktop. They do not establish the
professor's required VSCode coding-agent workflow for Problem 5. The included
`VSCode_prompt.txt` provides a starting prompt for that work.

All code checks passed, including 20 social-network `testif` checks and 11
weather unittest methods. Every IMDB collaboration count and actor box-office
total was independently checked against the supplied CSV files.

The `Homework2` capitalization follows this repository's `Homework1` convention
and the handout's explicit `Homework2/p5/` path. Problem 4 uses `p4` because
the handout's `p3` filename would overwrite Problem 3.

Weather input is headerless CSV with dates in `%I:%M:%S %p %m/%d/%Y` format.
Observations are sorted chronologically using `datetime`. Statistics output
has columns `station,min,max,mean`, sorted by station, with one decimal place.
