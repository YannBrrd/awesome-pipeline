-- Auto-generated placeholder for cross-table checks; extend as needed.
-- Payments roughly match items (tolerance 1%)
WITH items AS (
  SELECT order_id, SUM(CAST(price AS DECIMAL(18,2)) + CAST(freight_value AS DECIMAL(18,2))) AS items_total
  FROM order_items
  GROUP BY order_id
),
payments AS (
  SELECT order_id, SUM(CAST(payment_value AS DECIMAL(18,2))) AS payments_total
  FROM order_payments
  GROUP BY order_id
)
SELECT o.order_id, i.items_total, p.payments_total,
       ABS(COALESCE(i.items_total,0) - COALESCE(p.payments_total,0)) AS delta
FROM orders o
LEFT JOIN items i USING(order_id)
LEFT JOIN payments p USING(order_id)
WHERE ABS(COALESCE(i.items_total,0) - COALESCE(p.payments_total,0)) >
      0.01 * GREATEST(COALESCE(i.items_total,0), 1);
