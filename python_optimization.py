"""
================================================================
  Python Optimization for Data Scientists
  Author     : Vishvi
  Topics     : Vectorization, List Comprehensions, Generators,
               Efficient Pandas, Memory Profiling, Caching,
               Multiprocessing, NumPy tricks
  Why        : Real DS code must be FAST, not just correct.
  Environment: Jupyter Notebook
================================================================
"""

import time
import numpy as np
import pandas as pd
from functools import lru_cache
from memory_profiler import memory_usage  # pip install memory-profiler

print("=" * 58)
print("  ⚡ Python Optimization for Data Scientists — Vishvi")
print("=" * 58)

def timer(func):
    """Decorator to measure function execution time."""
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"  ⏱️  {func.__name__}: {elapsed:.2f} ms")
        return result
    return wrapper


# ──────────────────────────────────────────────────────────
# 1️⃣  LOOPS vs VECTORIZATION (NumPy)
# ──────────────────────────────────────────────────────────
print("\n" + "=" * 58)
print("1️⃣  LOOPS vs VECTORIZATION")
print("=" * 58)

data = list(range(1_000_000))
arr  = np.array(data)

@timer
def slow_loop(data):
    return [x ** 2 for x in data]

@timer
def fast_numpy(arr):
    return arr ** 2

print("\nSquaring 1 million numbers:")
slow_loop(data)
fast_numpy(arr)
print("  → NumPy is 10-100x faster for numerical operations!")


# ──────────────────────────────────────────────────────────
# 2️⃣  LIST COMPREHENSION vs APPEND LOOP
# ──────────────────────────────────────────────────────────
print("\n" + "=" * 58)
print("2️⃣  LIST COMPREHENSION vs APPEND LOOP")
print("=" * 58)

@timer
def slow_append():
    result = []
    for i in range(100_000):
        if i % 2 == 0:
            result.append(i * 2)
    return result

@timer
def fast_comprehension():
    return [i * 2 for i in range(100_000) if i % 2 == 0]

print("\nFiltering and transforming 100K numbers:")
slow_append()
fast_comprehension()
print("  → List comprehensions are 30-50% faster than append loops!")


# ──────────────────────────────────────────────────────────
# 3️⃣  GENERATORS — memory efficient pipelines
# ──────────────────────────────────────────────────────────
print("\n" + "=" * 58)
print("3️⃣  GENERATORS vs LISTS — Memory Efficiency")
print("=" * 58)

import sys

list_result = [x ** 2 for x in range(100_000)]
gen_result  = (x ** 2 for x in range(100_000))

print(f"\nList size  : {sys.getsizeof(list_result):,} bytes")
print(f"Generator  : {sys.getsizeof(gen_result):,} bytes")
print("  → Generator uses ~800KB LESS memory for same data!")
print("  → Use generators when you only iterate ONCE.")

# Generator pipeline example
def read_data(n):
    """Simulate reading rows from a large file."""
    for i in range(n):
        yield {"id": i, "value": i * 1.5, "category": "A" if i % 2 == 0 else "B"}

def filter_category(rows, cat):
    return (r for r in rows if r["category"] == cat)

def extract_values(rows):
    return (r["value"] for r in rows)

# Pipeline — processes 1M rows without loading all into memory!
pipeline = extract_values(filter_category(read_data(1_000_000), "A"))
total = sum(pipeline)
print(f"\nGenerator pipeline sum (1M rows, category A): {total:,.1f}")
print("  → Entire pipeline used minimal memory!")


# ──────────────────────────────────────────────────────────
# 4️⃣  EFFICIENT PANDAS
# ──────────────────────────────────────────────────────────
print("\n" + "=" * 58)
print("4️⃣  EFFICIENT PANDAS")
print("=" * 58)

# Create sample DataFrame
df = pd.DataFrame({
    "salary":     np.random.randint(50000, 150000, 100_000),
    "department": np.random.choice(["DS", "Eng", "Marketing"], 100_000),
    "experience": np.random.randint(1, 20, 100_000),
    "score":      np.random.uniform(0, 100, 100_000)
})

print(f"\nDataFrame shape: {df.shape}")
print(f"Memory usage   : {df.memory_usage(deep=True).sum() / 1024:.1f} KB")

# 4a. iterrows() vs vectorized
@timer
def slow_iterrows(df):
    bonuses = []
    for _, row in df.iterrows():
        bonuses.append(row["salary"] * 0.1 if row["score"] > 80 else 0)
    return bonuses

@timer
def fast_vectorized(df):
    return np.where(df["score"] > 80, df["salary"] * 0.1, 0)

print("\nCalculating bonuses (100K rows):")
_ = slow_iterrows(df.head(1000))   # only 1K for iterrows (it's very slow!)
_ = fast_vectorized(df)
print("  → NEVER use iterrows() on large DataFrames!")
print("  → Use np.where, .apply with vectorized funcs, or boolean indexing.")

# 4b. Memory optimisation with downcasting
print("\nMemory optimisation via downcasting:")
df_opt = df.copy()
df_opt["salary"]     = pd.to_numeric(df_opt["salary"],     downcast="integer")
df_opt["experience"] = pd.to_numeric(df_opt["experience"], downcast="integer")
df_opt["department"] = df_opt["department"].astype("category")

before = df.memory_usage(deep=True).sum() / 1024
after  = df_opt.memory_usage(deep=True).sum() / 1024
print(f"  Before: {before:.1f} KB")
print(f"  After : {after:.1f} KB")
print(f"  Saved : {before - after:.1f} KB ({(before-after)/before*100:.1f}% reduction)")


# ──────────────────────────────────────────────────────────
# 5️⃣  CACHING with lru_cache
# ──────────────────────────────────────────────────────────
print("\n" + "=" * 58)
print("5️⃣  CACHING — lru_cache for Repeated Computations")
print("=" * 58)

def slow_fibonacci(n):
    """Recursive Fibonacci without cache — exponential time!"""
    if n < 2: return n
    return slow_fibonacci(n-1) + slow_fibonacci(n-2)

@lru_cache(maxsize=None)
def fast_fibonacci(n):
    """Recursive Fibonacci WITH cache — linear time."""
    if n < 2: return n
    return fast_fibonacci(n-1) + fast_fibonacci(n-2)

print("\nFibonacci(35):")
start = time.perf_counter()
slow_fibonacci(35)
print(f"  Without cache : {(time.perf_counter()-start)*1000:.1f} ms")

start = time.perf_counter()
fast_fibonacci(35)
print(f"  With lru_cache: {(time.perf_counter()-start)*1000:.3f} ms")
print("  → lru_cache is 1000x+ faster for repeated recursive calls!")


# ──────────────────────────────────────────────────────────
# 6️⃣  STRING OPERATIONS — avoid + concatenation
# ──────────────────────────────────────────────────────────
print("\n" + "=" * 58)
print("6️⃣  STRING CONCATENATION — The Right Way")
print("=" * 58)

words = ["Data", "Science", "is", "powerful"] * 10_000

@timer
def slow_concat(words):
    result = ""
    for w in words:
        result += w + " "
    return result

@timer
def fast_join(words):
    return " ".join(words)

print("\nConcatenating 40K words:")
slow_concat(words)
fast_join(words)
print("  → str.join() is 3-10x faster than += concatenation!")
print("  → += creates a new string object every iteration.")


# ──────────────────────────────────────────────────────────
# 7️⃣  SET vs LIST for membership testing
# ──────────────────────────────────────────────────────────
print("\n" + "=" * 58)
print("7️⃣  SET vs LIST — Membership Testing O(1) vs O(n)")
print("=" * 58)

large_list = list(range(1_000_000))
large_set  = set(large_list)
target     = 999_999

@timer
def search_list():
    return target in large_list

@timer
def search_set():
    return target in large_set

print("\nSearching for element in 1M items:")
search_list()
search_set()
print("  → Set lookup is O(1), List lookup is O(n).")
print("  → Always convert to set when doing repeated membership tests!")


# ──────────────────────────────────────────────────────────
# 8️⃣  NUMPY TRICKS for Data Science
# ──────────────────────────────────────────────────────────
print("\n" + "=" * 58)
print("8️⃣  NUMPY TRICKS every Data Scientist should know")
print("=" * 58)

arr = np.array([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5])

print(f"\nArray          : {arr}")
print(f"Unique values  : {np.unique(arr)}")
print(f"Value counts   : {dict(zip(*np.unique(arr, return_counts=True)))}")
print(f"Percentiles    : 25th={np.percentile(arr,25)}, 75th={np.percentile(arr,75)}")
print(f"Clip [2,6]     : {np.clip(arr, 2, 6)}")
print(f"Normalised     : {np.round((arr - arr.min()) / (arr.max() - arr.min()), 2)}")
print(f"Sorted indices : {np.argsort(arr)}")
print(f"Top 3 indices  : {np.argpartition(arr, -3)[-3:]}")

# Broadcasting
matrix = np.random.randint(1, 10, (4, 4))
row_means = matrix.mean(axis=1, keepdims=True)
normalised = matrix - row_means   # broadcasting — no loop needed!
print(f"\nBroadcasting: row-normalised 4x4 matrix (no loop):")
print(normalised)


print("\n" + "=" * 58)
print("  ✅ Python Optimization techniques complete!")
print("  ⚡ Fast code = better Data Science!")
print("  🟩 Push to GitHub for today's green square!")
print("=" * 58)
