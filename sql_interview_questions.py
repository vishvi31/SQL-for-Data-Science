"""
================================================================
  SQL Interview Questions & Answers for Data Science Roles
  Author  : Vishvi
  Level   : Easy → Medium → Hard
  Tool    : Python sqlite3 — runs in Jupyter Notebook
  Source  : Patterns from FAANG, product, and analytics roles
================================================================
"""

import sqlite3, pandas as pd

conn = sqlite3.connect(":memory:")
cur  = conn.cursor()

cur.executescript("""
    CREATE TABLE employees (
        emp_id INT, name TEXT, department TEXT,
        salary REAL, manager_id INT, hire_date TEXT
    );
    CREATE TABLE sales (
        sale_id INT, emp_id INT, region TEXT,
        amount REAL, sale_date TEXT
    );
    CREATE TABLE products (
        product_id INT, name TEXT, category TEXT, price REAL
    );
    CREATE TABLE orders (
        order_id INT, customer_id INT, product_id INT,
        quantity INT, order_date TEXT, status TEXT
    );

    INSERT INTO employees VALUES
        (1,'Ananya','Data Science',95000,5,'2021-03-01'),
        (2,'Bharat','Data Science',85000,5,'2022-06-15'),
        (3,'Chetan','Engineering',90000,6,'2020-11-20'),
        (4,'Divya','Engineering',78000,6,'2023-01-10'),
        (5,'Esha','Data Science',120000,NULL,'2019-08-05'),
        (6,'Farhan','Engineering',115000,NULL,'2018-04-22'),
        (7,'Geeta','Marketing',70000,8,'2022-09-30'),
        (8,'Hari','Marketing',105000,NULL,'2017-12-15'),
        (9,'Isha','Data Science',92000,5,'2021-07-18'),
        (9,'Isha','Data Science',92000,5,'2021-07-18');

    INSERT INTO sales VALUES
        (1,1,'North',15000,'2024-01-10'),
        (2,1,'South',22000,'2024-02-15'),
        (3,2,'North',18000,'2024-01-20'),
        (4,3,'East', 9000,'2024-02-05'),
        (5,2,'South',25000,'2024-03-10'),
        (6,4,'West', 5000,'2024-01-30'),
        (7,1,'East', 30000,'2024-03-05'),
        (8,3,'North',12000,'2024-02-28');

    INSERT INTO products VALUES
        (1,'Laptop','Electronics',75000),
        (2,'Phone','Electronics',25000),
        (3,'Desk','Furniture',12000),
        (4,'Chair','Furniture',8000),
        (5,'Notebook','Stationery',500);

    INSERT INTO orders VALUES
        (101,1,1,2,'2024-01-10','Delivered'),
        (102,2,2,1,'2024-01-15','Delivered'),
        (103,2,3,1,'2024-02-01','Pending'),
        (104,3,1,1,'2024-02-10','Delivered'),
        (105,4,5,5,'2024-02-20','Delivered'),
        (106,5,2,2,'2024-03-01','Cancelled'),
        (107,3,4,3,'2024-03-05','Delivered'),
        (108,1,2,1,'2024-03-10','Delivered');
""")
conn.commit()

def q(level, num, question, query, hint=""):
    print(f"\n{'='*60}")
    print(f"  {level} Q{num}: {question}")
    if hint: print(f"  💡 Hint: {hint}")
    print(f"{'='*60}")
    print(f"SQL:\n{query.strip()}\n")
    df = pd.read_sql_query(query, conn)
    print(df.to_string(index=False))

# ────────────────────────────────────────
print("\n🟢 EASY QUESTIONS")
# ────────────────────────────────────────

q("🟢","1","Find all employees in the Data Science department",
"""SELECT name, salary, hire_date
FROM employees
WHERE department = 'Data Science'
ORDER BY salary DESC;""")

q("🟢","2","Count employees in each department",
"""SELECT department, COUNT(*) AS headcount
FROM employees
GROUP BY department
ORDER BY headcount DESC;""",
"GROUP BY + COUNT")

q("🟢","3","Find employees earning more than the company average",
"""SELECT name, department, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees)
ORDER BY salary DESC;""",
"Subquery in WHERE")

q("🟢","4","Get top 3 highest paid employees",
"""SELECT name, department, salary
FROM employees
ORDER BY salary DESC
LIMIT 3;""")

q("🟢","5","Find total sales per employee",
"""SELECT e.name, SUM(s.amount) AS total_sales
FROM employees e
JOIN sales s ON e.emp_id = s.emp_id
GROUP BY e.emp_id
ORDER BY total_sales DESC;""")

# ────────────────────────────────────────
print("\n🟡 MEDIUM QUESTIONS")
# ────────────────────────────────────────

q("🟡","6","Find the second highest salary (classic!)",
"""SELECT MAX(salary) AS second_highest
FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);""",
"Nested MAX with WHERE")

q("🟡","7","Find duplicate rows in employees table",
"""SELECT name, department, salary, COUNT(*) AS duplicates
FROM employees
GROUP BY name, department, salary
HAVING duplicates > 1;""",
"GROUP BY all columns + HAVING COUNT > 1")

q("🟡","8","Get the highest paid employee per department",
"""WITH ranked AS (
    SELECT name, department, salary,
           RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS rnk
    FROM employees
)
SELECT name, department, salary
FROM ranked WHERE rnk = 1;""",
"Window function RANK() OVER PARTITION BY")

q("🟡","9","Find employees with no sales (LEFT JOIN + NULL)",
"""SELECT e.name, e.department
FROM employees e
LEFT JOIN sales s ON e.emp_id = s.emp_id
WHERE s.sale_id IS NULL;""",
"LEFT JOIN — NULL means no match")

q("🟡","10","Monthly sales trend",
"""SELECT SUBSTR(sale_date,1,7) AS month,
       COUNT(*)              AS num_sales,
       SUM(amount)           AS total_revenue
FROM sales
GROUP BY month
ORDER BY month;""")

q("🟡","11","Rank employees by salary within department",
"""SELECT name, department, salary,
       RANK()       OVER (PARTITION BY department ORDER BY salary DESC) AS rank_in_dept,
       DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS dense_rank,
       ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS row_num
FROM employees;""",
"RANK vs DENSE_RANK vs ROW_NUMBER — know the difference!")

q("🟡","12","Running total of sales over time",
"""SELECT sale_date, amount,
       SUM(amount) OVER (ORDER BY sale_date) AS running_total
FROM sales
ORDER BY sale_date;""",
"SUM() OVER (ORDER BY ...) = cumulative/running total")

# ────────────────────────────────────────
print("\n🔴 HARD QUESTIONS")
# ────────────────────────────────────────

q("🔴","13","Month-over-month revenue growth %",
"""WITH monthly AS (
    SELECT SUBSTR(sale_date,1,7) AS month,
           SUM(amount)           AS revenue
    FROM sales GROUP BY month
),
with_prev AS (
    SELECT month, revenue,
           LAG(revenue) OVER (ORDER BY month) AS prev_revenue
    FROM monthly
)
SELECT month, revenue, prev_revenue,
       ROUND((revenue - prev_revenue) * 100.0 / prev_revenue, 1) AS pct_growth
FROM with_prev;""",
"CTE + LAG() window function + percentage calculation")

q("🔴","14","Find employees earning more than their manager",
"""SELECT e.name      AS employee,
       e.salary     AS emp_salary,
       m.name       AS manager,
       m.salary     AS mgr_salary
FROM employees e
JOIN employees m ON e.manager_id = m.emp_id
WHERE e.salary > m.salary;""",
"Self JOIN — join a table to itself!")

q("🔴","15","Pivot: total sales by employee per region",
"""SELECT e.name,
       SUM(CASE WHEN s.region='North' THEN s.amount ELSE 0 END) AS North,
       SUM(CASE WHEN s.region='South' THEN s.amount ELSE 0 END) AS South,
       SUM(CASE WHEN s.region='East'  THEN s.amount ELSE 0 END) AS East,
       SUM(CASE WHEN s.region='West'  THEN s.amount ELSE 0 END) AS West
FROM employees e
JOIN sales s ON e.emp_id = s.emp_id
GROUP BY e.emp_id;""",
"PIVOT using CASE WHEN — very common in analytics interviews!")

q("🔴","16","Find customers who ordered in Jan but NOT in Feb (retention)",
"""WITH jan AS (SELECT DISTINCT customer_id FROM orders WHERE SUBSTR(order_date,6,2)='01'),
     feb AS (SELECT DISTINCT customer_id FROM orders WHERE SUBSTR(order_date,6,2)='02')
SELECT j.customer_id AS churned_in_feb
FROM jan j
LEFT JOIN feb f ON j.customer_id = f.customer_id
WHERE f.customer_id IS NULL;""",
"Set difference using LEFT JOIN + NULL — classic retention analysis!")

q("🔴","17","Consecutive days with sales (streak detection)",
"""WITH daily AS (
    SELECT DISTINCT sale_date FROM sales
),
with_grp AS (
    SELECT sale_date,
           DATE(sale_date, '-' || ROW_NUMBER() OVER (ORDER BY sale_date) || ' days') AS grp
    FROM daily
)
SELECT grp, COUNT(*) AS streak_days,
       MIN(sale_date) AS streak_start,
       MAX(sale_date) AS streak_end
FROM with_grp
GROUP BY grp
HAVING streak_days > 1;""",
"Advanced: island-and-gaps problem — senior DS interview question")

print("\n" + "="*60)
print("  ✅ All 17 interview questions solved!")
print("  🟩 Great practice — push this to GitHub!")
print("="*60)

conn.close()
