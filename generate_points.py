"""
Point Generator
Creates random 2D point sets with different distributions for testing.
"""

import random
import math
import os


def generate_uniform(n, lo=0, hi=100000, seed=None):
    """
    Generate n points with uniform random coordinates in [lo, hi].
    Most points end up interior -> small hull relative to n.
    """
    if seed is not None:
        random.seed(seed)
    points = set()
    while len(points) < n:
        x = random.uniform(lo, hi)
        y = random.uniform(lo, hi)
        points.add((x, y))
    return list(points)


def generate_circle(n, cx=50000, cy=50000, radius=40000, noise=0, seed=None):
    """
    Generate n points on (or near) a circle.
    Near-worst case for hull size since almost every point is a hull vertex.
    
    noise: if > 0, add random perturbation to radius so points aren't exactly on circle
    """
    if seed is not None:
        random.seed(seed)
    points = set()
    while len(points) < n:
        angle = random.uniform(0, 2 * math.pi)
        r = radius + (random.uniform(-noise, noise) if noise > 0 else 0)
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        points.add((x, y))
    return list(points)


def generate_clustered(n, num_clusters=5, spread=5000, lo=10000, hi=90000, seed=None):
    """
    Generate n points in tight clusters.
    Tests how algorithms handle uneven spatial distributions.
    """
    if seed is not None:
        random.seed(seed)

    # pick cluster centers
    centers = []
    for _ in range(num_clusters):
        cx = random.uniform(lo, hi)
        cy = random.uniform(lo, hi)
        centers.append((cx, cy))

    points = set()
    while len(points) < n:
        # pick a random cluster
        cx, cy = random.choice(centers)
        x = random.gauss(cx, spread)
        y = random.gauss(cy, spread)
        points.add((x, y))
    return list(points)


def save_points(points, filepath):
    """Save points to a text file, one point per line: x y"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        for (x, y) in points:
            f.write(f"{x} {y}\n")


def load_points(filepath):
    """Load points from a text file."""
    points = []
    with open(filepath, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 2:
                points.append((float(parts[0]), float(parts[1])))
    return points


if __name__ == "__main__":
    # generate sample data to verify it works
    for dist_name, gen_func in [("uniform", generate_uniform),
                                 ("circle", generate_circle),
                                 ("clustered", generate_clustered)]:
        pts = gen_func(100, seed=42)
        print(f"{dist_name}: generated {len(pts)} points, "
              f"sample: {pts[0]}, {pts[1]}, {pts[2]}")
