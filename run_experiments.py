"""
Experiment Runner
Benchmarks brute force and Graham Scan across multiple input sizes and distributions.
Outputs results to a CSV file.
"""

import time
import csv
import os
import sys

from brute_force import brute_force_hull
from graham_scan import graham_scan
from generate_points import generate_uniform, generate_circle, generate_clustered

# ============================================================
# CONFIG — adjust these to your needs
# ============================================================

# input sizes to test
# brute force gets really slow above ~5000, so we cap it
SIZES_BOTH = [100, 500, 1000, 2000, 3000]
SIZES_GRAHAM_ONLY = [5000, 10000, 50000, 100000]

# how many trials per (size, distribution) combo — we average them
NUM_TRIALS = 3

# max seconds before we skip brute force for a given size
BF_TIMEOUT = 120  # 2 minutes

# distributions to test
DISTRIBUTIONS = {
    "uniform": generate_uniform,
    "circle": generate_circle,
    "clustered": generate_clustered,
}

OUTPUT_DIR = "results"
OUTPUT_CSV = os.path.join(OUTPUT_DIR, "experiment_results.csv")


def time_algorithm(algo_func, points):
    """Run an algorithm and return (elapsed_seconds, hull_size)."""
    start = time.perf_counter()
    hull = algo_func(points)
    elapsed = time.perf_counter() - start
    return elapsed, len(hull)


def run_experiments():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    results = []
    all_sizes = sorted(set(SIZES_BOTH + SIZES_GRAHAM_ONLY))

    print("=" * 70)
    print("CONVEX HULL EXPERIMENT RUNNER")
    print(f"Trials per config: {NUM_TRIALS}")
    print(f"Brute force timeout: {BF_TIMEOUT}s")
    print(f"Sizes (both): {SIZES_BOTH}")
    print(f"Sizes (Graham only): {SIZES_GRAHAM_ONLY}")
    print(f"Distributions: {list(DISTRIBUTIONS.keys())}")
    print("=" * 70)

    for dist_name, gen_func in DISTRIBUTIONS.items():
        print(f"\n--- Distribution: {dist_name} ---")

        # track if brute force has timed out so we skip bigger sizes
        bf_timed_out = False

        for n in all_sizes:
            run_bf = (n in SIZES_BOTH) and (not bf_timed_out)
            run_gs = True

            bf_times = []
            gs_times = []
            bf_hull_size = 0
            gs_hull_size = 0

            for trial in range(NUM_TRIALS):
                # generate fresh points each trial with different seed
                seed = n * 1000 + trial
                points = gen_func(n, seed=seed)

                # --- Graham Scan ---
                gs_elapsed, gs_hull_size = time_algorithm(graham_scan, points)
                gs_times.append(gs_elapsed)

                # --- Brute Force ---
                if run_bf:
                    bf_elapsed, bf_hull_size = time_algorithm(brute_force_hull, points)
                    bf_times.append(bf_elapsed)

                    # if this trial exceeded timeout, skip brute force for remaining
                    if bf_elapsed > BF_TIMEOUT:
                        print(f"  n={n}, trial {trial+1}: BF took {bf_elapsed:.2f}s — "
                              f"skipping BF for larger sizes")
                        bf_timed_out = True
                        run_bf = False

            # compute averages
            avg_gs = sum(gs_times) / len(gs_times)

            if bf_times:
                avg_bf = sum(bf_times) / len(bf_times)
                speedup = avg_bf / avg_gs if avg_gs > 0 else float('inf')
                bf_str = f"{avg_bf:.6f}"
                speedup_str = f"{speedup:.1f}x"
            else:
                avg_bf = None
                bf_str = "N/A"
                speedup_str = "—"

            row = {
                "distribution": dist_name,
                "n": n,
                "bf_avg_time": avg_bf,
                "gs_avg_time": avg_gs,
                "bf_hull_size": bf_hull_size if bf_times else None,
                "gs_hull_size": gs_hull_size,
                "speedup": speedup_str,
            }
            results.append(row)

            print(f"  n={n:>7} | BF: {bf_str:>12}s | GS: {avg_gs:.6f}s | "
                  f"hull: {gs_hull_size:>5} | speedup: {speedup_str}")

    # write CSV
    fieldnames = ["distribution", "n", "bf_avg_time", "gs_avg_time",
                  "bf_hull_size", "gs_hull_size", "speedup"]
    with open(OUTPUT_CSV, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)

    print(f"\nResults saved to {OUTPUT_CSV}")
    return results


if __name__ == "__main__":
    run_experiments()
