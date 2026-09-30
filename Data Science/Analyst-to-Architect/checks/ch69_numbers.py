"""Chapter 69: recompute every Riverstone number the chapter quotes.

Run from the book folder:  python3 checks/ch69_numbers.py
Needs psql as user postgres and the one-year database riverstone_2025 (Chapter 13, section 13.1).
Each assert is a number printed in the chapter (Moves 2, 7, 8 and answers 1, 3, 10).
"""
import subprocess


def q(sql: str) -> list[list[str]]:
    """Run one query in riverstone_2025 and return its rows as lists of strings."""
    r = subprocess.run(['su', 'postgres', '-c', 'psql -X -q -A -t -F "|" -d riverstone_2025'],
                       input=sql, capture_output=True, text=True, check=True)
    return [line.split('|') for line in r.stdout.strip().splitlines()]


def lakh(n: float) -> str:
    """Indian digit grouping: 4335471 -> '43,35,471'; 439823.5 -> '4,39,823.50'."""
    whole, _, dec = f"{n:.2f}".partition('.')
    if len(whole) > 3:
        head, tail = whole[:-3], whole[-3:]
        whole = ','.join([head[max(0, k - 2):k] for k in range(len(head), 0, -2)][::-1]) + ',' + tail
    return whole if dec == '00' else f"{whole}.{dec}"


LINE = "oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)"

# Move 2 and answer 10: revenue with and without the cancelled orders
allrev, = q(f"SELECT SUM({LINE}) FROM orders o JOIN order_items oi USING (order_id);")[0]
canc = q(f"SELECT COUNT(DISTINCT o.order_id), SUM({LINE}) FROM orders o JOIN order_items oi USING (order_id) "
         "WHERE o.status = 'Cancelled';")[0]
net, = q("SELECT SUM(net_revenue) FROM sales_lines;")[0]
dec, = q("SELECT SUM(net_revenue) FROM sales_lines WHERE order_date >= DATE '2025-12-01';")[0]
print(f"all orders Rs {lakh(float(allrev))}; cancelled {canc[0]} orders Rs {lakh(float(canc[1]))}; "
      f"revenue Rs {lakh(float(net))}; December Rs {lakh(float(dec))}")
assert lakh(float(allrev)) == '43,98,121' and canc[0] == '2' and float(canc[1]) == 62650
assert lakh(float(net)) == '43,35,471' and lakh(float(dec)) == '4,39,823.50'

# Move 7: the three segments add up to the total
segs = q("SELECT c.segment, SUM(s.net_revenue) FROM sales_lines s JOIN customers c USING (customer_id) "
         "GROUP BY 1 ORDER BY 1;")
print('segments:', {s: lakh(float(v)) for s, v in segs})
assert sorted(s for s, _ in segs) == ['Hospitality', 'Retail', 'Wholesale']
assert abs(sum(float(v) for _, v in segs) - float(net)) < 0.005

# Move 8: accounts with no (non-cancelled) order in the 90 days to 31 Dec 2025
lapsed = q("SELECT c.customer_name, MAX(s.order_date) FROM customers c LEFT JOIN sales_lines s USING (customer_id) "
           "GROUP BY 1 HAVING MAX(s.order_date) IS NULL OR MAX(s.order_date) < DATE '2025-12-31' - 90 ORDER BY 2;")
print('lapsed:', lapsed)
went_quiet = [n for n, d in lapsed if d]
never = [n for n, d in lapsed if not d]
assert len(went_quiet) == 3 and never == ['Home Plus']
names = ", ".join(f"'{n}'" for n in went_quiet)
rev3, = q(f"SELECT SUM(s.net_revenue) FROM sales_lines s JOIN customers c USING (customer_id) "
          f"WHERE c.customer_name IN ({names});")[0]
print(f"their 2025 revenue Rs {lakh(float(rev3))} (about Rs {float(rev3) / 1e5:.1f} lakh)")
assert round(float(rev3) / 1e5, 1) == 1.7

# Answer 1: customers with more than ten orders in 2025
many = q("SELECT c.customer_name, COUNT(*) FROM orders o JOIN customers c USING (customer_id) "
         "WHERE o.status <> 'Cancelled' GROUP BY 1 HAVING COUNT(*) > 10 ORDER BY 2 DESC, 1;")
print('more than ten orders:', many)
assert len(many) == 7 and many[0] == ['Green Leaf Hotels', '17']

# Answer 3: mean and median order value, how many orders sit above the mean, the largest order
stats = q("WITH t AS (SELECT order_id, SUM(net_revenue) v FROM sales_lines GROUP BY 1) "
          "SELECT COUNT(*), ROUND(AVG(v)), PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY v), "
          "COUNT(*) FILTER (WHERE v > (SELECT AVG(v) FROM t)), MAX(v) FROM t;")[0]
n, mean, median, above, largest = int(stats[0]), float(stats[1]), float(stats[2]), int(stats[3]), float(stats[4])
print(f"{n} orders, mean Rs {lakh(mean)}, median Rs {lakh(median)}, {above} above the mean, largest Rs {lakh(largest)}")
assert (n, mean, median, above, largest) == (173, 25061, 21375, 70, 100278)

print('Chapter 69: all numbers check.')
