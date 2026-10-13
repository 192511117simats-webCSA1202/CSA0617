# DAA Assignment 1 — GitHub Submission Package

> **Important:** This package currently contains DEMO benchmark outputs generated with seed `1234` and placeholder student details. Do not submit those demo results as your personal experimental evidence. Update `config.json` and rerun the scripts to generate your own dataset, results, graphs, and terminal logs.

## Repository contents
- `config.json` — edit name, registration number and assigned group.
- `src/algorithms.py` — Linear Search, Binary Search, and group-specific third algorithm.
- `src/dataset_generator.py` — reproducible personal dataset generator.
- `src/benchmark.py` — runs 1K, 10K, 100K, 1M tests and the Task 12 benchmark.
- `data/` — generated datasets (large data is generated locally; do not necessarily commit the 1M CSV).
- `results/results.csv` — measured benchmark data.
- `results/task12_summary.txt` — Task 12 benchmark summary.
- `results/graphs/` — plots generated from `results.csv`.
- `screenshots/` — output evidence images; regenerate after personalizing.
- `report/` — place the final PDF report here.

## Third algorithm by group
- A: Hash-table lookup
- B: Interpolation search
- C: Jump search
- D: Binary Search Tree (BST) lookup

Linear Search and Binary Search are included for every group. Check your instructor's group assignment before finalizing.

## Setup
Requires Python 3.10+ and `matplotlib`.

```bash
python -m pip install matplotlib
```

## Personalize before running
Edit `config.json`:
1. Enter your name and registration number.
2. Set `assigned_group` to A, B, C, or D.
3. The personal random seed must be the last four digits of your registration number. The benchmark script derives it automatically when the registration number contains digits.

For a demo run only, `config.json` uses seed `1234`.

## Run
From the repository root:

```bash
python src/benchmark.py
```

This generates the datasets, measured CSV, graph PNGs and terminal log. It tests 1,000, 10,000, 100,000 and 1,000,000 records and performs the Task 12 benchmark of 50,000 searches against 1,000,000 records.

## Notes on fair measurements
- Dataset generation is outside the search-time measurement.
- Binary Search and Interpolation Search require sorted data; sorting time is reported separately.
- Hash table/BST build time is reported separately.
- The script records comparison/key-check counts and elapsed time.
- Timing varies by machine and Python version; use your own run's values in the report.
- Screenshots should show the actual program output and your name/registration number. The PNGs included with this initial package are demo evidence templates generated from the demo run.
- Add at least five meaningful commits over the assignment week. Do not make one final-only commit.

## Suggested commit sequence
1. Add README and config.
2. Add search algorithm implementations.
3. Add dataset generator.
4. Add benchmark script.
5. Add results and graphs after running.
6. Add final PDF and screenshots.

## Submission checklist
- [ ] All 12 report tasks completed.
- [ ] Actual outputs rerun using your own personal seed.
- [ ] Screenshots for all four dataset sizes.
- [ ] Task 12 benchmark (50,000 searches on 1M records).
- [ ] Report PDF saved under `report/`.
- [ ] Code ZIP uploaded to Classroom.
- [ ] GitHub link pasted in PDF and Classroom.
