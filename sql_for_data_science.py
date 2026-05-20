"""
================================================================
  SQL for Data Science — Comprehensive Practice File
  Author  : Vishvi
  Tool    : Python (sqlite3) — runs in Jupyter Notebook
  Topics  : SELECT → GROUP BY → JOINs → Subqueries →
            CTEs → Window Functions → Interview Patterns
================================================================
"""

import sqlite3
import pandas as pd

# Connect to in-memory SQLite database
conn = sqlite3.connect(":memory:")
cur  = conn.cursor()

print("=" * 55)
print("  🗄️  SQL for Data Science — Vishvi")
print("=" * 55)

# ──────────────────────────────────────────────────────────
# 🏗️  SETUP: Create sample tables
# ──────────────────────────────────────────────────────────

cur.executescript("""
    CREATE TABLE customers (
        customer_id   INTEGER PRIMARY KEY,
        name          TEXT,
        city          TEXT,
        age           INTEGER,
        signup_date   TEXT
    );

    CREATE TABLE orders (
        order_id      INTEGER PRIMARY KEY,
        customer_id   INTEGER,
        product       TEXT,
        category      TEXT,
        amount        REAL,
        order_date    TEXT,
        status        TEXT
    );

    CREATE TABLE employees (
        emp_id        INTEGER PRIMARY KEY,
        name          TEXT,
        department    TEXT,
        salary        REAL,
        manager_id    INTEGER,
        hire_date     TEXT
    );

    INSERT INTO customers VALUES
        (1,  'Vishvi',   'Delhi',     23, '2023-01-15'),
        (2,  'Aditi',    'Mumbai',    28, '2022-06-20'),
        (3,  'Rohan',    'Bangalore', 32, '2021-03-10'),
        (4,  'Priya',    'Delhi',     25, '2023-08-05'),
        (5,  'Arjun',    'Chennai',   35, '2020-11-30'),
        (6,  'Sneha',    'Mumbai',    27, '2022-09-15'),
        (7,  'Vikram',   'Delhi',     30, '2021-07-22'),
        (8,  'Meera',    'Pune',      29, '2023-02-18');

    INSERT INTO orders VALUES
        (101, 1, 'Laptop',     'Electronics', 75000, '2024-01-10', 'Delivered'),
        (102, 1, 'Phone',      'Electronics', 25000, '2024-02-15', 'Delivered'),
        (103, 2, 'Headphones', 'Electronics',  3500, '2024-01-20', 'Delivered'),
        (104, 3, 'Desk',       'Furniture',   12000, '2024-03-05', 'Pending'),
        (105, 3, 'Chair',      'Furniture',    8000, '2024-03-06', 'Delivered'),
        (106, 4, 'Notebook',   'Stationery',    500, '2024-02-28', 'Delivered'),
        (107, 5, 'Monitor',    'Electronics', 18000, '2024-01-15', 'Cancelled'),
        (108, 6, 'Keyboard',   'Electronics',  2000, '2024-03-10', 'Delivered'),
        (109, 7, 'Laptop',     'Electronics', 80000, '2024-02-05', 'Delivered'),
        (110, 2, 'Mouse',      'Electronics',  1500, '2024-03-01', 'Delivered'),
        (111, 8, 'Lamp',       'Furniture',    2500, '2024-01-30', 'Pending'),
        (112, 5, 'Phone',      'Electronics', 30000, '2024-03-20', 'Delivered');

    INSERT INTO employees VALUES
        (1, 'Ananya',  'Data Science', 95000,  5, '2021-03-01'),
        (2, 'Bharat',  'Data Science', 85000,  5, '2022-06-15'),
        (3, 'Chetan',  'Engineering',  90000,  6, '2020-11-20'),
        (4, 'Divya',   'Engineering',  78000,  6, '2023-01-10'),
        (5, 'Esha',    'Data Science', 120000, NULL,'2019-08-05'),
        (6, 'Farhan',  'Engineering',  115000, NULL,'2018-04-22'),
        (7, 'Geeta',   'Marketing',    70000,  8, '2022-09-30'),
        (8, 'Hari',    'Marketing',    105000, NULL,'2017-12-15'),
        (9, 'Isha',    'Data Science', 92000,  5, '2021-07-18');
""")
conn.commit()

def run(title, query):
    """Run a SQL query and display results as a DataFrame."""
    print(f"\n{'─'*55}")
    print(f"  📌 {title}")
    print(f"{'─'*55}")
    print(f"SQL:\n{query.strip()}")
    print()
    df = pd.read_sql_query(query, conn)
    print(df.to_string(index=False))
    return df


# ──────────────────────────────────────────────────────────
# 1️⃣  BASIC SELECT
# ──────────────────────────────────────────────────────────

run("All customers", "SELECT * FROM customers;")

run("Select specific columns",
"""SELECT name, city, age
FROM customers
ORDER BY age DESC;""")

run("Filter with WHERE",
"""SELECT name, city
FROM customers
WHERE city = 'Delhi';""")

run("Multiple conditions (AND / OR)",
"""SELECT name, city, age
FROM customers
WHERE city = 'Mumbai' OR age < 26;""")


# ──────────────────────────────────────────────────────────
# 2️⃣  AGGREGATIONS & GROUP BY
# ──────────────────────────────────────────────────────────

run("Total revenue",
"""SELECT SUM(amount) AS total_revenue
FROM orders
WHERE status = 'Delivered';""")

run("Orders per customer",
"""SELECT customer_id,
       COUNT(*)        AS total_orders,
       SUM(amount)     AS total_spent,
       AVG(amount)     AS avg_order_value,
       MAX(amount)     AS biggest_order
FROM orders
GROUP BY customer_id
ORDER BY total_spent DESC;""")

run("Revenue by category",
"""SELECT category,
       COUNT(*)    AS num_orders,
       SUM(amount) AS revenue
FROM orders
GROUP BY category
ORDER BY revenue DESC;""")

run("HAVING — customers who spent over 20,000",
"""SELECT customer_id, SUM(amount) AS total_spent
FROM orders
GROUP BY customer_id
HAVING total_spent > 20000
ORDER BY total_spent DESC;""")


# ──────────────────────────────────────────────────────────
# 3️⃣  JOINS
# ──────────────────────────────────────────────────────────

run("INNER JOIN — orders with customer names",
"""SELECT c.name, o.product, o.amount, o.status
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
ORDER BY o.amount DESC;""")

run("LEFT JOIN — all customers, even with no orders",
"""SELECT c.name, c.city, COUNT(o.order_id) AS num_orders
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id
ORDER BY num_orders DESC;""")

run("JOIN + GROUP BY — top spending customers",
"""SELECT c.name, c.city, SUM(o.amount) AS total_spent
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
WHERE o.status = 'Delivered'
GROUP BY c.customer_id
ORDER BY total_spent DESC
LIMIT 5;""")


# ──────────────────────────────────────────────────────────
# 4️⃣  SUBQUERIES
# ──────────────────────────────────────────────────────────

run("Subquery — customers who placed orders",
"""SELECT name, city
FROM customers
WHERE customer_id IN (
    SELECT DISTINCT customer_id FROM orders
);""")

run("Subquery — orders above average amount",
"""SELECT product, amount
FROM orders
WHERE amount > (SELECT AVG(amount) FROM orders)
ORDER BY amount DESC;""")

run("Correlated subquery — each customer vs avg",
"""SELECT c.name,
       o.product,
       o.amount,
       ROUND((SELECT AVG(amount) FROM orders), 2) AS avg_all_orders
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.amount > (SELECT AVG(amount) FROM orders);""")


# ──────────────────────────────────────────────────────────
# 5️⃣  CTEs (Common Table Expressions)
# ──────────────────────────────────────────────────────────

run("CTE — high-value customers (spent > 50,000)",
"""WITH high_value AS (
    SELECT customer_id, SUM(amount) AS total_spent
    FROM orders
    WHERE status = 'Delivered'
    GROUP BY customer_id
    HAVING total_spent > 50000
)
SELECT c.name, c.city, hv.total_spent
FROM customers c
JOIN high_value hv ON c.customer_id = hv.customer_id
ORDER BY hv.total_spent DESC;""")

run("CTE — monthly revenue trend",
"""WITH monthly AS (
    SELECT SUBSTR(order_date, 1, 7) AS month,
           SUM(amount)              AS revenue,
           COUNT(*)                 AS num_orders
    FROM orders
    WHERE status = 'Delivered'
    GROUP BY month
)
SELECT month, revenue, num_orders
FROM monthly
ORDER BY month;""")


# ──────────────────────────────────────────────────────────
# 6️⃣  WINDOW FUNCTIONS
# ──────────────────────────────────────────────────────────

run("ROW_NUMBER — rank orders by amount",
"""SELECT product, amount,
       ROW_NUMBER() OVER (ORDER BY amount DESC) AS rank
FROM orders
WHERE status = 'Delivered';""")

run("RANK — salary rank within department",
"""SELECT name, department, salary,
       RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS dept_rank
FROM employees;""")

run("Running total — cumulative revenue over time",
"""SELECT order_date, amount,
       SUM(amount) OVER (ORDER BY order_date) AS running_total
FROM orders
WHERE status = 'Delivered'
ORDER BY order_date;""")

run("LAG — compare each order to previous order amount",
"""SELECT product, order_date, amount,
       LAG(amount) OVER (ORDER BY order_date)              AS prev_amount,
       amount - LAG(amount) OVER (ORDER BY order_date)     AS change
FROM orders
WHERE status = 'Delivered'
ORDER BY order_date;""")

run("LEAD — look ahead to next order",
"""SELECT product, order_date, amount,
       LEAD(amount) OVER (ORDER BY order_date) AS next_order_amount
FROM orders
WHERE status = 'Delivered'
ORDER BY order_date;""")


# ──────────────────────────────────────────────────────────
# 7️⃣  CASE WHEN
# ──────────────────────────────────────────────────────────

run("CASE WHEN — segment customers by spend",
"""SELECT c.name,
       SUM(o.amount) AS total_spent,
       CASE
           WHEN SUM(o.amount) >= 50000 THEN 'Premium'
           WHEN SUM(o.amount) >= 10000 THEN 'Regular'
           ELSE 'Occasional'
       END AS customer_segment
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id
ORDER BY total_spent DESC;""")

run("CASE WHEN — salary band classification",
"""SELECT name, department, salary,
       CASE
           WHEN salary >= 100000 THEN 'Senior'
           WHEN salary >= 85000  THEN 'Mid-level'
           ELSE 'Junior'
       END AS level
FROM employees
ORDER BY salary DESC;""")


# ──────────────────────────────────────────────────────────
# 8️⃣  NULL HANDLING
# ──────────────────────────────────────────────────────────

run("IS NULL — employees with no manager (leaders)",
"""SELECT name, department, salary
FROM employees
WHERE manager_id IS NULL;""")

run("COALESCE — replace NULL with a default",
"""SELECT name,
       COALESCE(CAST(manager_id AS TEXT), 'No Manager') AS manager
FROM employees;""")


# ──────────────────────────────────────────────────────────
# 9️⃣  STRING & DATE FUNCTIONS
# ──────────────────────────────────────────────────────────

run("String functions — UPPER, LENGTH, SUBSTR",
"""SELECT name,
       UPPER(city)         AS city_upper,
       LENGTH(name)        AS name_length,
       SUBSTR(name, 1, 3)  AS name_prefix
FROM customers;""")

run("Date functions — extract year from signup",
"""SELECT name,
       signup_date,
       SUBSTR(signup_date, 1, 4) AS signup_year,
       SUBSTR(signup_date, 6, 2) AS signup_month
FROM customers
ORDER BY signup_date;""")


# ──────────────────────────────────────────────────────────
# 🔟  INTERVIEW PATTERNS
# ──────────────────────────────────────────────────────────

run("Interview: Find duplicate products in orders",
"""SELECT product, COUNT(*) AS times_ordered
FROM orders
GROUP BY product
HAVING times_ordered > 1
ORDER BY times_ordered DESC;""")

run("Interview: Top N per group (top earner per dept)",
"""WITH ranked AS (
    SELECT name, department, salary,
           RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS rnk
    FROM employees
)
SELECT name, department, salary
FROM ranked
WHERE rnk = 1;""")

run("Interview: Month-over-month revenue change",
"""WITH monthly AS (
    SELECT SUBSTR(order_date, 1, 7) AS month,
           SUM(amount)              AS revenue
    FROM orders
    WHERE status = 'Delivered'
    GROUP BY month
),
with_prev AS (
    SELECT month, revenue,
           LAG(revenue) OVER (ORDER BY month) AS prev_revenue
    FROM monthly
)
SELECT month,
       revenue,
       prev_revenue,
       ROUND(((revenue - prev_revenue) * 100.0 / prev_revenue), 1) AS pct_change
FROM with_prev;""")

run("Interview: Customers with no orders (churn candidates)",
"""SELECT c.name, c.city, c.signup_date
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;""")

run("Interview: Second highest salary",
"""SELECT MAX(salary) AS second_highest_salary
FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);""")

print("\n" + "="*55)
print("  ✅ All SQL queries executed successfully!")
print("  🟩 Push this file to GitHub for today's green square!")
print("="*55)

conn.close()
