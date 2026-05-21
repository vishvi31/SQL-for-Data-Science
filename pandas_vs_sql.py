"""
================================================================
  Pandas vs SQL — Side-by-Side Comparison
  Author  : Vishvi
  Why     : Every Data Scientist must know BOTH.
            This file shows identical operations in SQL and
            Pandas so you can switch between them fluently.
================================================================
"""

import sqlite3, pandas as pd, numpy as np

# ── Setup ────────────────────────────────────────────────
conn = sqlite3.connect(":memory:")

df = pd.DataFrame({
    "name":       ["Vishvi","Aditi","Rohan","Priya","Arjun","Sneha"],
    "department": ["DS","DS","Eng","Eng","Marketing","DS"],
    "salary":     [95000, 85000, 90000, 78000, 70000, 92000],
    "city":       ["Delhi","Mumbai","Bangalore","Delhi","Chennai","Mumbai"],
    "experience": [2, 3, 5, 1, 7, 4]
})
df.to_sql("employees", conn, index=False, if_exists="replace")

def show(title, sql_result, pandas_result):
    print(f"\n{'─'*55}")
    print(f"  📌 {title}")
    print(f"{'─'*55}")
    print("SQL result:")
    print(sql_result.to_string(index=False))
    print("\nPandas result:")
    print(pandas_result.to_string(index=False))

# ── 1. SELECT + WHERE ────────────────────────────────────
sql = pd.read_sql("SELECT name, salary FROM employees WHERE salary > 88000", conn)
pan = df[df["salary"] > 88000][["name","salary"]].reset_index(drop=True)
show("Filter rows (WHERE / boolean indexing)", sql, pan)

# ── 2. ORDER BY ──────────────────────────────────────────
sql = pd.read_sql("SELECT name, salary FROM employees ORDER BY salary DESC", conn)
pan = df[["name","salary"]].sort_values("salary", ascending=False).reset_index(drop=True)
show("Sort rows (ORDER BY / sort_values)", sql, pan)

# ── 3. GROUP BY + AGG ────────────────────────────────────
sql = pd.read_sql("""SELECT department,
                            COUNT(*) AS headcount,
                            ROUND(AVG(salary),0) AS avg_salary,
                            MAX(salary) AS max_salary
                     FROM employees GROUP BY department""", conn)
pan = df.groupby("department").agg(
    headcount=("name","count"),
    avg_salary=("salary", lambda x: round(x.mean(),0)),
    max_salary=("salary","max")
).reset_index()
show("Group + Aggregate (GROUP BY / groupby.agg)", sql, pan)

# ── 4. HAVING ────────────────────────────────────────────
sql = pd.read_sql("""SELECT department, AVG(salary) AS avg_sal
                     FROM employees GROUP BY department
                     HAVING avg_sal > 85000""", conn)
pan = (df.groupby("department")["salary"]
         .mean().reset_index()
         .rename(columns={"salary":"avg_sal"})
         .query("avg_sal > 85000"))
show("Filter groups (HAVING / .query after groupby)", sql, pan)

# ── 5. LIMIT ─────────────────────────────────────────────
sql = pd.read_sql("SELECT name, salary FROM employees ORDER BY salary DESC LIMIT 3", conn)
pan = df.nlargest(3, "salary")[["name","salary"]].reset_index(drop=True)
show("Top N rows (LIMIT / nlargest)", sql, pan)

# ── 6. CASE WHEN ─────────────────────────────────────────
sql = pd.read_sql("""SELECT name, salary,
    CASE WHEN salary>=90000 THEN 'Senior'
         WHEN salary>=80000 THEN 'Mid'
         ELSE 'Junior' END AS level
FROM employees""", conn)
pan = df[["name","salary"]].copy()
pan["level"] = pd.cut(df["salary"],
                      bins=[0,79999,89999,999999],
                      labels=["Junior","Mid","Senior"])
show("Conditional column (CASE WHEN / pd.cut)", sql, pan)

# ── 7. NULL handling ─────────────────────────────────────
df_null = df.copy()
df_null.loc[0, "city"] = None
df_null.to_sql("emp_null", conn, index=False, if_exists="replace")

sql = pd.read_sql("SELECT name FROM emp_null WHERE city IS NULL", conn)
pan = df_null[df_null["city"].isna()][["name"]].reset_index(drop=True)
show("Find NULLs (IS NULL / isna)", sql, pan)

# ── 8. String operations ─────────────────────────────────
sql = pd.read_sql("""SELECT name, UPPER(department) AS dept_upper,
                            LENGTH(name) AS name_len
                     FROM employees""", conn)
pan = df[["name","department"]].copy()
pan["dept_upper"] = df["department"].str.upper()
pan["name_len"]   = df["name"].str.len()
show("String ops (UPPER, LENGTH / .str methods)", sql, pan)

# ── 9. Window: Running total ─────────────────────────────
sql = pd.read_sql("""SELECT name, salary,
       SUM(salary) OVER (ORDER BY salary) AS running_total
FROM employees""", conn)
pan = df[["name","salary"]].sort_values("salary").copy()
pan["running_total"] = pan["salary"].cumsum()
show("Running total (SUM OVER / cumsum)", sql, pan)

# ── 10. Window: RANK ─────────────────────────────────────
sql = pd.read_sql("""SELECT name, department, salary,
       RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS rnk
FROM employees""", conn)
pan = df[["name","department","salary"]].copy()
pan["rnk"] = (df.groupby("department")["salary"]
                .rank(method="min", ascending=False)
                .astype(int))
show("Rank within group (RANK OVER PARTITION / groupby rank)", sql, pan)

print("\n" + "="*55)
print("  ✅ Pandas ↔ SQL comparison complete!")
print("  💡 Both tools. One Data Scientist.")
print("="*55)
conn.close()
