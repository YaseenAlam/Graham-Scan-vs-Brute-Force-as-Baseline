"""
Plot Results
Reads the CSV from run_experiments.py and generates comparison charts.
Saves charts as PNG files in the results/ folder.
"""

import csv
import os
import matplotlib
matplotlib.use('Agg')  # non-interactive backend so it works without a display
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


RESULTS_CSV = os.path.join("results", "experiment_results.csv")
OUTPUT_DIR = "results"


def load_results(filepath):
    """Load experiment results from CSV into a dict keyed by distribution."""
    data = {}
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            dist = row["distribution"]
            if dist not in data:
                data[dist] = []
            entry = {
                "n": int(row["n"]),
                "bf_avg_time": float(row["bf_avg_time"]) if row["bf_avg_time"] else None,
                "gs_avg_time": float(row["gs_avg_time"]) if row["gs_avg_time"] else None,
                "gs_hull_size": int(row["gs_hull_size"]) if row["gs_hull_size"] else None,
            }
            data[dist].append(entry)
    return data


def plot_bf_vs_gs(data):
    """
    Chart 1: Brute Force vs Graham Scan runtime on uniform data.
    Uses log scale on y-axis so you can see both lines clearly.
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    for dist_name in ["uniform"]:
        if dist_name not in data:
            continue
        entries = data[dist_name]

        # brute force data (skip None entries)
        bf_n = [e["n"] for e in entries if e["bf_avg_time"] is not None]
        bf_t = [e["bf_avg_time"] for e in entries if e["bf_avg_time"] is not None]

        # graham scan data
        gs_n = [e["n"] for e in entries if e["gs_avg_time"] is not None]
        gs_t = [e["gs_avg_time"] for e in entries if e["gs_avg_time"] is not None]

        ax.plot(bf_n, bf_t, 'o-', color='#e74c3c', linewidth=2, markersize=6,
                label=f'Brute Force Θ(n³)')
        ax.plot(gs_n, gs_t, 's-', color='#2ecc71', linewidth=2, markersize=6,
                label=f'Graham Scan Θ(n log n)')

    ax.set_yscale('log')
    ax.set_xlabel('Number of Points (n)', fontsize=13)
    ax.set_ylabel('Average Runtime (seconds, log scale)', fontsize=13)
    ax.set_title('Brute Force vs Graham Scan — Uniform Random Points', fontsize=15, fontweight='bold')
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))

    plt.tight_layout()
    outpath = os.path.join(OUTPUT_DIR, "chart1_bf_vs_gs.png")
    plt.savefig(outpath, dpi=150)
    plt.close()
    print(f"Saved: {outpath}")


def plot_gs_across_distributions(data):
    """
    Chart 2: Graham Scan runtime across all three distributions.
    Shows how distribution affects performance.
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    colors = {"uniform": "#3498db", "circle": "#e67e22", "clustered": "#9b59b6"}
    markers = {"uniform": "o", "circle": "s", "clustered": "^"}

    for dist_name in ["uniform", "circle", "clustered"]:
        if dist_name not in data:
            continue
        entries = data[dist_name]
        gs_n = [e["n"] for e in entries if e["gs_avg_time"] is not None]
        gs_t = [e["gs_avg_time"] for e in entries if e["gs_avg_time"] is not None]

        ax.plot(gs_n, gs_t, f'{markers.get(dist_name, "o")}-',
                color=colors.get(dist_name, "gray"),
                linewidth=2, markersize=6,
                label=f'{dist_name.capitalize()}')

    ax.set_xlabel('Number of Points (n)', fontsize=13)
    ax.set_ylabel('Average Runtime (seconds)', fontsize=13)
    ax.set_title('Graham Scan Runtime Across Distributions', fontsize=15, fontweight='bold')
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))

    plt.tight_layout()
    outpath = os.path.join(OUTPUT_DIR, "chart2_gs_distributions.png")
    plt.savefig(outpath, dpi=150)
    plt.close()
    print(f"Saved: {outpath}")


def plot_hull_size(data):
    """
    Chart 3: Hull size vs n for each distribution.
    Shows how many points end up on the hull — useful for interpreting timing diffs.
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    colors = {"uniform": "#3498db", "circle": "#e67e22", "clustered": "#9b59b6"}

    for dist_name in ["uniform", "circle", "clustered"]:
        if dist_name not in data:
            continue
        entries = data[dist_name]
        ns = [e["n"] for e in entries if e["gs_hull_size"] is not None]
        hs = [e["gs_hull_size"] for e in entries if e["gs_hull_size"] is not None]

        ax.plot(ns, hs, 'o-', color=colors.get(dist_name, "gray"),
                linewidth=2, markersize=6,
                label=f'{dist_name.capitalize()}')

    ax.set_xlabel('Number of Points (n)', fontsize=13)
    ax.set_ylabel('Hull Size (number of hull vertices)', fontsize=13)
    ax.set_title('Convex Hull Size Across Distributions', fontsize=15, fontweight='bold')
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))

    plt.tight_layout()
    outpath = os.path.join(OUTPUT_DIR, "chart3_hull_sizes.png")
    plt.savefig(outpath, dpi=150)
    plt.close()
    print(f"Saved: {outpath}")


def plot_speedup(data):
    """
    Chart 4: Speedup ratio (BF time / GS time) to show how much faster Graham Scan is.
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    for dist_name in ["uniform"]:
        if dist_name not in data:
            continue
        entries = data[dist_name]
        ns = []
        speedups = []
        for e in entries:
            if e["bf_avg_time"] is not None and e["gs_avg_time"] is not None and e["gs_avg_time"] > 0:
                ns.append(e["n"])
                speedups.append(e["bf_avg_time"] / e["gs_avg_time"])

        ax.bar(range(len(ns)), speedups, color='#2ecc71', edgecolor='#27ae60', linewidth=1.2)
        ax.set_xticks(range(len(ns)))
        ax.set_xticklabels([f'{n:,}' for n in ns])

    ax.set_xlabel('Number of Points (n)', fontsize=13)
    ax.set_ylabel('Speedup (BF time / GS time)', fontsize=13)
    ax.set_title('Graham Scan Speedup Over Brute Force', fontsize=15, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    outpath = os.path.join(OUTPUT_DIR, "chart4_speedup.png")
    plt.savefig(outpath, dpi=150)
    plt.close()
    print(f"Saved: {outpath}")


if __name__ == "__main__":
    if not os.path.exists(RESULTS_CSV):
        print(f"ERROR: {RESULTS_CSV} not found.")
        print("Run 'python run_experiments.py' first to generate data.")
        exit(1)

    data = load_results(RESULTS_CSV)
    print(f"Loaded data for distributions: {list(data.keys())}")

    plot_bf_vs_gs(data)
    plot_gs_across_distributions(data)
    plot_hull_size(data)
    plot_speedup(data)

    print("\nAll charts saved to results/ folder.")
