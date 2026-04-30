"""
Correctness Tests
Verifies that both brute force and Graham Scan produce correct convex hulls
on known inputs. Also checks that both algorithms agree on random inputs.
"""

import sys
import math
import random

from brute_force import brute_force_hull
from graham_scan import graham_scan
from generate_points import generate_uniform, generate_circle, generate_clustered


def normalize_hull(hull):
    """
    Normalize a hull so we can compare two hulls regardless of starting point or direction.
    We rotate the list so the point with the lowest (y, x) is first,
    then ensure counterclockwise order.
    """
    if len(hull) <= 1:
        return hull

    # find index of the bottom-most, left-most point
    min_idx = 0
    for i in range(1, len(hull)):
        if (hull[i][1], hull[i][0]) < (hull[min_idx][1], hull[min_idx][0]):
            min_idx = i

    # rotate so that point is first
    hull = hull[min_idx:] + hull[:min_idx]

    # check if the hull is clockwise; if so, reverse it (but keep first element in place)
    if len(hull) >= 3:
        cross = ((hull[1][0] - hull[0][0]) * (hull[2][1] - hull[0][1]) -
                 (hull[1][1] - hull[0][1]) * (hull[2][0] - hull[0][0]))
        if cross < 0:
            hull = [hull[0]] + hull[1:][::-1]

    return hull


def hulls_equal(h1, h2, tol=1e-9):
    """Check if two normalized hulls have the same vertices."""
    n1 = normalize_hull(list(h1))
    n2 = normalize_hull(list(h2))

    if len(n1) != len(n2):
        return False

    for (a, b) in zip(n1, n2):
        if abs(a[0] - b[0]) > tol or abs(a[1] - b[1]) > tol:
            return False
    return True


def is_convex(hull):
    """Verify that a polygon is convex by checking all cross products have the same sign."""
    n = len(hull)
    if n < 3:
        return True

    sign = None
    for i in range(n):
        o = hull[i]
        a = hull[(i + 1) % n]
        b = hull[(i + 2) % n]
        cross = (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

        if abs(cross) < 1e-10:
            continue  # collinear is ok

        if sign is None:
            sign = cross > 0
        elif (cross > 0) != sign:
            return False
    return True


def all_points_inside(hull, points, tol=1e-9):
    """Check that every point in 'points' is on or inside the convex hull."""
    n = len(hull)
    for p in points:
        inside = True
        for i in range(n):
            a = hull[i]
            b = hull[(i + 1) % n]
            cross = (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])
            if cross < -tol:
                inside = False
                break
        if not inside:
            return False
    return True


def run_tests():
    passed = 0
    failed = 0

    def check(name, condition):
        nonlocal passed, failed
        if condition:
            passed += 1
            print(f"  PASS: {name}")
        else:
            failed += 1
            print(f"  FAIL: {name}")

    # ============================
    # TEST 1: Simple square
    # ============================
    print("\nTest 1: Square with interior point")
    pts = [(0, 0), (10, 0), (10, 10), (0, 10), (5, 5)]
    expected_hull = [(0, 0), (10, 0), (10, 10), (0, 10)]

    bf_hull = brute_force_hull(pts)
    gs_hull = graham_scan(pts)

    check("BF returns 4 hull vertices", len(bf_hull) == 4)
    check("GS returns 4 hull vertices", len(gs_hull) == 4)
    check("BF hull is convex", is_convex(bf_hull))
    check("GS hull is convex", is_convex(gs_hull))
    check("BF and GS agree", hulls_equal(bf_hull, gs_hull))

    # ============================
    # TEST 2: Triangle
    # ============================
    print("\nTest 2: Triangle (all points on hull)")
    pts = [(0, 0), (5, 10), (10, 0)]
    bf_hull = brute_force_hull(pts)
    gs_hull = graham_scan(pts)

    check("BF returns 3 vertices", len(bf_hull) == 3)
    check("GS returns 3 vertices", len(gs_hull) == 3)
    check("BF and GS agree", hulls_equal(bf_hull, gs_hull))

    # ============================
    # TEST 3: Collinear points
    # ============================
    print("\nTest 3: Points with collinear edges")
    pts = [(0, 0), (5, 0), (10, 0), (10, 10), (0, 10)]
    gs_hull = graham_scan(pts)

    check("GS hull is convex", is_convex(gs_hull))
    check("All points inside GS hull", all_points_inside(gs_hull, pts))

    # ============================
    # TEST 4: Random agreement test
    # ============================
    print("\nTest 4: BF and GS agree on small random inputs (n=50, 10 trials)")
    all_agree = True
    for trial in range(10):
        pts = generate_uniform(50, seed=trial * 77)
        bf_hull = brute_force_hull(pts)
        gs_hull = graham_scan(pts)

        if not hulls_equal(bf_hull, gs_hull):
            all_agree = False
            print(f"    Disagreement on trial {trial}!")
            break

        if not is_convex(gs_hull):
            all_agree = False
            print(f"    GS hull not convex on trial {trial}!")
            break

    check("All 10 random trials agree", all_agree)

    # ============================
    # TEST 5: Circle points (near worst case for hull size)
    # ============================
    print("\nTest 5: Points on a circle (n=100)")
    pts = generate_circle(100, seed=42)
    gs_hull = graham_scan(pts)

    check("GS hull is convex", is_convex(gs_hull))
    check("All points inside GS hull", all_points_inside(gs_hull, pts))
    check("Most points are hull vertices (>80)", len(gs_hull) > 80)

    # ============================
    # TEST 6: Larger random input — verify GS hull properties
    # ============================
    print("\nTest 6: Larger input (n=1000) — GS hull properties")
    pts = generate_uniform(1000, seed=123)
    gs_hull = graham_scan(pts)

    check("GS hull is convex", is_convex(gs_hull))
    check("All 1000 points inside hull", all_points_inside(gs_hull, pts))
    check("Hull size < n", len(gs_hull) < 1000)

    # ============================
    # SUMMARY
    # ============================
    print("\n" + "=" * 50)
    print(f"RESULTS: {passed} passed, {failed} failed out of {passed + failed} tests")
    print("=" * 50)

    return failed == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
