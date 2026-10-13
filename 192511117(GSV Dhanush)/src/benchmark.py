"""Run DAA Assignment 1 benchmarks and save CSV, graph images and terminal log."""
import csv, json, os, random, statistics, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from algorithms import linear_search, binary_search, hash_lookup, interpolation_search, jump_search, bst_build, bst_lookup
from dataset_generator import generate_dataset, seed_from_registration

CONFIG = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
NAME = CONFIG.get("student_name", "ENTER YOUR FULL NAME")
REG = CONFIG.get("registration_number", "ENTER YOUR REGISTRATION NUMBER")
GROUP = str(CONFIG.get("assigned_group", "A")).upper()
SIZES = CONFIG.get("dataset_sizes", [1000, 10000, 100000, 1000000])
TASK12_QUERIES = int(CONFIG.get("task12_queries", 50000))
SEED = seed_from_registration(REG, CONFIG.get("demo_seed", 1234))
DEMO = ("ENTER" in str(REG).upper() or not str(REG).strip())

THIRD = {
    "A": ("Hash Table", "hash"),
    "B": ("Interpolation Search", "interpolation"),
    "C": ("Jump Search", "jump"),
    "D": ("Binary Search Tree (BST)", "bst"),
}
if GROUP not in THIRD:
    raise ValueError("assigned_group must be A, B, C, or D in config.json")
third_name, third_kind = THIRD[GROUP]

def timed(fn):
    start = time.perf_counter()
    result = fn()
    return result, (time.perf_counter() - start) * 1000

def main():
    outdir = ROOT / "results"
    graphdir = outdir / "graphs"
    datadir = ROOT / "data"
    screenshotdir = ROOT / "screenshots"
    for d in [outdir, graphdir, datadir, screenshotdir]:
        d.mkdir(parents=True, exist_ok=True)
    lines = []
    lines.append("DAA Assignment 1 — Benchmark Output")
    lines.append(f"Name: {NAME} | Reg No: {REG} | Group: {GROUP}")
    lines.append(f"Seed used: {SEED}" + (" (DEMO SEED — personalize config before submission)" if DEMO else " (derived from last four registration-number digits)"))
    lines.append(f"Run date/time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"Third algorithm selected: {third_name}")
    rows = []
    for n in SIZES:
        data, gen_ms = timed(lambda: generate_dataset(n, SEED + n, REG))
        # Save only smaller data as CSV; regenerate 1M from the seed to avoid huge repository bloat.
        if n <= 100000:
            with open(datadir / f"students_{n}.csv", "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f); w.writerow(["registration_number"]); w.writerows((x,) for x in data)
        sorted_data = data  # generator returns sorted unique IDs
        target_found = None
        if REG and "ENTER" not in str(REG).upper():
            try:
                target_found = int("".join(ch for ch in str(REG) if ch.isdigit()))
                if target_found not in data: target_found = data[0]
            except Exception:
                target_found = data[n // 2]
        else:
            target_found = data[n // 2]
        target_absent = target_found + 1
        while target_absent in set(data):
            target_absent += 1
        # Use absent key for worst-case linear comparison evidence.
        idx, ms = timed(lambda: linear_search(data, target_absent))
        rows.append([n, "Linear Search", "absent", idx, ms, n, 0.0, 0.0])
        idx, ms = timed(lambda: binary_search(sorted_data, target_found))
        _, absent_ms = timed(lambda: binary_search(sorted_data, target_absent))
        _, comps = binary_search(sorted_data, target_found)
        rows.append([n, "Binary Search", "found", idx, ms, comps, 0.0, 0.0])
        build_ms = 0.0
        if third_kind == "hash":
            table, build_ms = timed(lambda: {x: x for x in data})
            found, checks = hash_lookup(table, target_found)
            _, ms = timed(lambda: hash_lookup(table, target_found))
        elif third_kind == "interpolation":
            found_idx, checks = interpolation_search(sorted_data, target_found)
            _, ms = timed(lambda: interpolation_search(sorted_data, target_found))
            build_ms = 0.0  # data already sorted
            found = found_idx >= 0
        elif third_kind == "jump":
            found_idx, checks = jump_search(sorted_data, target_found)
            _, ms = timed(lambda: jump_search(sorted_data, target_found))
            found = found_idx >= 0
        else:
            root, build_ms = timed(lambda: bst_build(data))
            found, checks = bst_lookup(root, target_found)
            _, ms = timed(lambda: bst_lookup(root, target_found))
        rows.append([n, third_name, "found", int(found), ms, checks, build_ms, 0.0])
        lines.append(f"\nn={n:,} | generation={gen_ms:.3f} ms")
        lines.append(f"  Linear Search: absent target -> NOT FOUND; comparisons={n:,}; elapsed={rows[-3][4]:.6f} ms")
        lines.append(f"  Binary Search: found target -> FOUND; comparisons={comps}; elapsed={rows[-2][4]:.6f} ms")
        lines.append(f"  {third_name}: found target -> {'FOUND' if found else 'NOT FOUND'}; key checks={checks}; build={build_ms:.3f} ms; elapsed={ms:.6f} ms")
        # Save a console-style evidence image after each size.
        try:
            import matplotlib.pyplot as plt
            fig = plt.figure(figsize=(13, 5.5))
            fig.patch.set_facecolor("#101820")
            ax = fig.add_subplot(111); ax.set_facecolor("#101820"); ax.axis("off")
            ax.text(0.03, 0.95, "\n".join(lines[-5:]), va="top", ha="left",
                    color="white", family="monospace", fontsize=11, linespacing=1.7)
            ax.text(0.03, 0.08, "DEMO OUTPUT — rerun after entering personal details in config.json" if DEMO else f"{NAME} | {REG}",
                    color="#ffcc66", fontsize=10)
            fig.savefig(screenshotdir / f"task08_output_{n}.png", dpi=130, bbox_inches="tight")
            plt.close(fig)
        except Exception:
            pass
    # Save results
    with open(outdir / "results.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["dataset_size","algorithm","target_case","result","search_time_ms","comparisons_or_key_checks","preprocessing_build_time_ms","sorting_time_ms"])
        w.writerows(rows)
    # Task 12: 50,000 searches on 1M records, with prebuilt third-approach index
    n = 1_000_000
    data = generate_dataset(n, SEED + n, REG)
    rng = random.Random(SEED + 99)
    queries = [data[rng.randrange(n)] for _ in range(TASK12_QUERIES)]
    # Benchmark binary searches; also benchmark group-specific index/lookups.
    start = time.perf_counter()
    bin_checks = 0
    for q in queries:
        _, c = binary_search(data, q); bin_checks += c
    binary_total_ms = (time.perf_counter() - start) * 1000
    if third_kind == "hash":
        index, build_ms = timed(lambda: {x: x for x in data})
        start = time.perf_counter(); checks = 0
        for q in queries:
            _, c = hash_lookup(index, q); checks += c
        third_total_ms = (time.perf_counter() - start) * 1000
    elif third_kind == "interpolation":
        index = data; build_ms = 0.0
        start = time.perf_counter(); checks = 0
        for q in queries:
            _, c = interpolation_search(index, q); checks += c
        third_total_ms = (time.perf_counter() - start) * 1000
    elif third_kind == "jump":
        index = data; build_ms = 0.0
        start = time.perf_counter(); checks = 0
        for q in queries:
            _, c = jump_search(index, q); checks += c
        third_total_ms = (time.perf_counter() - start) * 1000
    else:
        index, build_ms = timed(lambda: bst_build(data))
        start = time.perf_counter(); checks = 0
        for q in queries:
            _, c = bst_lookup(index, q); checks += c
        third_total_ms = (time.perf_counter() - start) * 1000
    task12 = [
        "TASK 12 — 50,000 searches on 1,000,000 records",
        f"Name: {NAME} | Reg No: {REG} | Group: {GROUP}",
        f"Run date/time: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"Seed: {SEED}" + (" (DEMO)" if DEMO else ""),
        f"Queries: {TASK12_QUERIES:,}; database records: {n:,}",
        f"Binary Search: total={binary_total_ms:.3f} ms; avg={binary_total_ms/TASK12_QUERIES:.6f} ms/query; comparisons={bin_checks:,}",
        f"{third_name}: build/index time={build_ms:.3f} ms; total lookup={third_total_ms:.3f} ms; avg={third_total_ms/TASK12_QUERIES:.6f} ms/query; key checks={checks:,}",
        "Note: timings are machine-specific; report the values from your own run."
    ]
    (outdir / "task12_summary.txt").write_text("\n".join(task12), encoding="utf-8")
    lines.extend(["", *task12])
    (outdir / "terminal_output.txt").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    # Generate graphs from actual CSV
    try:
        import matplotlib.pyplot as plt
        with open(outdir / "results.csv", newline="", encoding="utf-8") as f:
            rr = list(csv.DictReader(f))
        algos = sorted(set(r["algorithm"] for r in rr))
        for metric, ylabel, filename in [
            ("search_time_ms", "Measured search time (ms)", "execution_time.png"),
            ("comparisons_or_key_checks", "Comparisons / key checks", "comparisons.png")
        ]:
            fig, ax = plt.subplots(figsize=(9, 5.5))
            for algo in algos:
                subset = [r for r in rr if r["algorithm"] == algo]
                subset.sort(key=lambda r: int(r["dataset_size"]))
                ax.plot([int(r["dataset_size"]) for r in subset], [float(r[metric]) for r in subset], marker="o", label=algo)
            ax.set_xscale("log"); ax.set_xlabel("Dataset size (records; log scale)"); ax.set_ylabel(ylabel)
            ax.set_title(f"DAA Assignment 1: {ylabel}"); ax.grid(True, alpha=0.3); ax.legend()
            fig.tight_layout(); fig.savefig(graphdir / filename, dpi=160); plt.close(fig)
        # theoretical vs observed comparison counts, indicative curves
        fig, ax = plt.subplots(figsize=(9,5.5))
        ns = [int(r["dataset_size"]) for r in rr if r["algorithm"] == "Linear Search"]
        ax.plot(ns, ns, marker="o", label="Linear worst-case theoretical n")
        ax.plot(ns, [max(1, int(__import__("math").ceil(__import__("math").log2(x+1)))) for x in ns], marker="o", label="Binary approximate log2(n)")
        ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlabel("Dataset size (records; log scale)")
        ax.set_ylabel("Operation count (log scale)"); ax.set_title("Theoretical growth reference (not measured series)")
        ax.grid(True, which="both", alpha=0.3); ax.legend(); fig.tight_layout()
        fig.savefig(graphdir / "theory_growth_reference.png", dpi=160); plt.close(fig)
    except Exception as e:
        print("Graph generation warning:", e)

if __name__ == "__main__":
    main()
