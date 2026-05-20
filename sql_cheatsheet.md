# 🗄️ SQL Cheatsheet for Data Scientists

> Quick-reference for interviews and daily analysis work.

---

## 1. Basic SELECT
```sql
SELECT col1, col2 FROM table WHERE condition ORDER BY col1 DESC LIMIT 10;
```

## 2. Aggregations
```sql
SELECT dept, COUNT(*), SUM(sal), AVG(sal), MIN(sal), MAX(sal)
FROM employees
GROUP BY dept
HAVING AVG(sal) > 80000;
```

## 3. JOINs
```sql
-- INNER: only matching rows
SELECT * FROM a INNER JOIN b ON a.id = b.id;

-- LEFT: all from left, NULL if no match on right
SELECT * FROM a LEFT JOIN b ON a.id = b.id;
```

## 4. Subquery
```sql
SELECT * FROM orders WHERE amount > (SELECT AVG(amount) FROM orders);
```

## 5. CTE
```sql
WITH cte AS (
    SELECT customer_id, SUM(amount) AS total FROM orders GROUP BY customer_id
)
SELECT * FROM cte WHERE total > 50000;
```

## 6. Window Functions
```sql
-- Rank within group
RANK() OVER (PARTITION BY dept ORDER BY salary DESC)

-- Running total
SUM(amount) OVER (ORDER BY order_date)

-- Previous row value
LAG(amount, 1) OVER (ORDER BY order_date)

-- Next row value
LEAD(amount, 1) OVER (ORDER BY order_date)
```

## 7. CASE WHEN
```sql
CASE WHEN salary > 100000 THEN 'Senior'
     WHEN salary > 80000  THEN 'Mid'
     ELSE 'Junior' END AS level
```

## 8. NULL Handling
```sql
WHERE col IS NULL
WHERE col IS NOT NULL
COALESCE(col, 'default_value')
```

## 9. Top N per Group (Classic Interview!)
```sql
WITH ranked AS (
    SELECT *, RANK() OVER (PARTITION BY dept ORDER BY salary DESC) AS rnk
    FROM employees
)
SELECT * FROM ranked WHERE rnk = 1;
```

## 10. Month-over-Month Change (Classic Interview!)
```sql
WITH monthly AS (SELECT SUBSTR(date,1,7) AS month, SUM(amount) AS rev FROM orders GROUP BY month),
prev AS (SELECT month, rev, LAG(rev) OVER (ORDER BY month) AS prev_rev FROM monthly)
SELECT month, ROUND((rev - prev_rev) * 100.0 / prev_rev, 1) AS pct_change FROM prev;
```

---
*Author: Vishvi | github.com/vishvi31*
