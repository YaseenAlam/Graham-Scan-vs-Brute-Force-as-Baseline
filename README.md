# Convex Hull - Brute Force vs Graham Scan

final group project for algorithm design & analysis

## about

we're comparing two ways to find the convex hull of a set of 2D points:
- **brute force** - checks every pair of points, runs in Θ(n³). slow but simple
- **graham scan** - sorts by angle then uses a stack to build the hull, Θ(n log n). way faster

we test both on different input sizes and distributions, make sure they're correct, and generate charts comparing runtimes.

## what you need

- python 3.8 or higher
- matplotlib (`pip install matplotlib`)

thats it

## files

- `brute_force.py` - the brute force algorithm
- `graham_scan.py` - the graham scan algorithm
- `generate_points.py` - generates random point sets (uniform, circle, clustered)
- `run_experiments.py` - benchmarks both algos and saves timing data to a csv
- `plot_results.py` - reads the csv and makes charts
- `test_correctness.py` - tests to make sure both algorithms actually work
- `results/` - where the csv and chart pngs end up (gets created when you run experiments)

## how to run

run the tests first to make sure nothing is broken:
```
python test_correctness.py
```

then run the actual experiments:
```
python run_experiments.py
```
heads up brute force gets really slow past like 2000-3000 points so it might take a few min. the script will skip brute force automatically if its taking too long

then make the charts:
```
python plot_results.py
```

or just do it all at once:
```
python test_correctness.py && python run_experiments.py && python plot_results.py
```

charts get saved as pngs in the `results/` folder

## tweaking the experiments

if brute force is taking forever on your machine open `run_experiments.py` and change the stuff at the top:
```python
SIZES_BOTH = [100, 500, 1000, 2000, 3000]        # sizes where both algos run
SIZES_GRAHAM_ONLY = [5000, 10000, 50000, 100000]  # graham scan only
NUM_TRIALS = 3                                     # how many times to run each
BF_TIMEOUT = 120                                   # seconds before giving up on brute force
```

## team

- [name] - [what they did]
- [name] - [what they did]
- [name] - [what they did]
- [name] - [what they did]
