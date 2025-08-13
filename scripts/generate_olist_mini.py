import csv, os, random, uuid
from datetime import datetime, timedelta

random.seed(42)

OUT_DIR = os.path.join("data", "olist_mini")
NUM_CUSTOMERS = 1000
NUM_SELLERS = 120
NUM_PRODUCTS = 800
NUM_ORDERS = 1500
DATE_START = datetime(2024, 1, 1)
DATE_END = datetime(2024, 3, 31)

STATES = ["SP","RJ","MG","RS","PR","SC","BA","PE","CE","DF","GO","ES","PA","AM","RN","MT","MS","PB","MA"]
CITIES = ["sao paulo","rio de janeiro","belo horizonte","curitiba","porto alegre","campinas","salvador","recife","fortaleza","brasilia","goiania","vitoria","manaus","natal","cuiaba","campo grande","joao pessoa","sao bernardo","guarulhos","osasco"]
CATEGORIES = [
    "bed_bath_table","health_beauty","sports_leisure","furniture_decor","computers_accessories",
    "toys","watches_gifts","auto","garden_tools","cool_stuff","stationery","pet_shop","telephony",
    "perfumery","baby","housewares","books_general_interest","consoles_games","luggage_accessories",
    # typos/variants:
    "eletronics","fashon_bags","computers_acessories","garden_toolss","houseware","book_general_interest"
]
PAYMENT_TYPES = ["credit_card","boleto","voucher","debit_card","not_defined"]

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def rid(prefix):
    return prefix + uuid.uuid4().hex[:8]

def rand_date(start, end):
    delta = end - start
    return start + timedelta(seconds=random.randint(0, int(delta.total_seconds())))

def maybe(val, p=0.02):
    return None if random.random() < p else val

def write_csv(path, rows, header):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=header)
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if v is None else v) for k, v in r.items()})

def gen_customers(n):
    rows = []
    for _ in range(n):
        cid = rid("c_")
        zip_prefix = random.randint(10000, 99999)
        city = random.choice(CITIES)
        state = random.choice(STATES)
        rows.append({
            "customer_id": cid,
            "customer_unique_id": rid("cu_"),
            "customer_zip_code_prefix": maybe(zip_prefix, p=0.01),
            "customer_city": maybe(city, p=0.02),
            "customer_state": state
        })
    return rows

def gen_sellers(n):
    rows = []
    for _ in range(n):
        sid = rid("s_")
        rows.append({
            "seller_id": sid,
            "seller_zip_code_prefix": random.randint(10000, 99999),
            "seller_city": random.choice(CITIES),
            "seller_state": random.choice(STATES)
        })
    return rows

def gen_products(n):
    rows = []
    for _ in range(n):
        pid = rid("p_")
        cat = random.choice(CATEGORIES)
        # inject some missing or nonsense measures
        weight = random.choice([random.randint(50, 5000), None]) if random.random() < 0.1 else random.randint(50, 5000)
        length = random.randint(5, 100)
        height = random.randint(1, 50)
        width = random.randint(1, 50)
        rows.append({
            "product_id": pid,
            "product_category_name": maybe(cat, p=0.05),
            "product_weight_g": weight,
            "product_length_cm": length,
            "product_height_cm": height,
            "product_width_cm": width
        })
    return rows

def gen_orders(n, customers):
    statuses = ["delivered","shipped","invoiced","canceled","processing"]
    rows = []
    for _ in range(n):
        oid = rid("o_")
        cust = random.choice(customers)["customer_id"]
        purchase = rand_date(DATE_START, DATE_END)
        status = random.choices(statuses, weights=[0.55,0.15,0.1,0.1,0.1], k=1)[0]

        approved = purchase + timedelta(hours=random.randint(0, 72))
        carrier = approved + timedelta(hours=random.randint(12, 120))
        delivered = carrier + timedelta(hours=random.randint(12, 240))
        estimated = purchase + timedelta(days=random.randint(3, 20))

        # Inject timestamp inconsistencies and nulls based on status
        if status in ("canceled","processing"):
            delivered = None if random.random() < 0.9 else delivered
            carrier = None if random.random() < 0.5 else carrier
        if random.random() < 0.02:
            # make delivered earlier than carrier (bad)
            delivered, carrier = carrier, delivered

        rows.append({
            "order_id": oid,
            "customer_id": cust,
            "order_status": status,
            "order_purchase_timestamp": purchase.isoformat(sep=" "),
            "order_approved_at": maybe(approved.isoformat(sep=" "), p=0.03),
            "order_delivered_carrier_date": maybe(None if carrier is None else carrier.isoformat(sep=" "), p=0.02),
            "order_delivered_customer_date": maybe(None if delivered is None else delivered.isoformat(sep=" "), p=0.02),
            "order_estimated_delivery_date": estimated.isoformat(sep=" ")
        })
    return rows

def gen_order_items(orders, products, sellers):
    rows = []
    order_totals = {}  # sums of items price + freight
    for o in orders:
        num_items = random.randint(1, 5)
        total = 0.0
        for item_seq in range(1, num_items + 1):
            product = random.choice(products)
            seller = random.choice(sellers)
            price = max(0.0, round(random.uniform(5, 500), 2))
            # inject zero/negative price or freight
            if random.random() < 0.01: price = 0.0
            freight = round(random.uniform(0, 60), 2)
            if random.random() < 0.005: freight = round(-abs(random.uniform(0, 20)), 2)
            # broken FK for some rows
            prod_id = product["product_id"] if random.random() > 0.005 else "p_broken"
            rows.append({
                "order_id": o["order_id"],
                "order_item_id": item_seq,
                "product_id": prod_id,
                "seller_id": seller["seller_id"],
                "shipping_limit_date": (rand_date(DATE_START, DATE_END) + timedelta(days=3)).isoformat(sep=" "),
                "price": price,
                "freight_value": freight
            })
            total += price + freight
            # duplicate some rows exactly
            if random.random() < 0.003:
                rows.append(rows[-1].copy())
                total += price + freight
        order_totals[o["order_id"]] = round(total, 2)
    return rows, order_totals

def gen_payments(orders, order_totals):
    rows = []
    for o in orders:
        oid = o["order_id"]
        k = random.choices([1,2,3], weights=[0.8,0.15,0.05])[0]
        remaining = order_totals.get(oid, 0.0)
        # inject mismatch in ~8% of orders (under/over payment)
        mismatch = 0.0
        if random.random() < 0.08:
            mismatch = round(random.uniform(-0.1, 0.1) * (remaining if remaining else 100), 2)
            remaining = max(0.0, remaining + mismatch)
        split = [round(remaining / k + random.uniform(-2, 2), 2) for _ in range(k-1)]
        split.append(round(remaining - sum(split), 2))
        seq = 1
        for amount in split:
            rows.append({
                "order_id": oid,
                "payment_sequential": seq,
                "payment_type": random.choice(PAYMENT_TYPES),
                "payment_installments": random.randint(1, 12),
                "payment_value": max(0.0, round(amount, 2))
            })
            seq += 1
        # occasionally zero payments
        if random.random() < 0.01:
            rows.append({
                "order_id": oid,
                "payment_sequential": seq,
                "payment_type": "not_defined",
                "payment_installments": 1,
                "payment_value": 0.0
            })
    return rows

def gen_reviews(orders):
    rows = []
    for o in orders:
        if random.random() < 0.6:
            created = rand_date(DATE_START, DATE_END) + timedelta(days=random.randint(0, 40))
            answered = created + timedelta(days=random.randint(0, 10))
            rows.append({
                "review_id": rid("r_"),
                "order_id": o["order_id"],
                "review_score": random.randint(1, 5),
                "review_comment_title": maybe(None, p=0.6),
                "review_comment_message": maybe(None, p=0.4),
                "review_creation_date": created.isoformat(sep=" "),
                "review_answer_timestamp": maybe(answered.isoformat(sep=" "), p=0.1)
            })
    return rows

def main():
    ensure_dir(OUT_DIR)
    customers = gen_customers(NUM_CUSTOMERS)
    sellers = gen_sellers(NUM_SELLERS)
    products = gen_products(NUM_PRODUCTS)
    orders = gen_orders(NUM_ORDERS, customers)
    order_items, order_totals = gen_order_items(orders, products, sellers)
    payments = gen_payments(orders, order_totals)
    reviews = gen_reviews(orders)

    write_csv(os.path.join(OUT_DIR, "customers.csv"), customers,
              ["customer_id","customer_unique_id","customer_zip_code_prefix","customer_city","customer_state"])
    write_csv(os.path.join(OUT_DIR, "sellers.csv"), sellers,
              ["seller_id","seller_zip_code_prefix","seller_city","seller_state"])
    write_csv(os.path.join(OUT_DIR, "products.csv"), products,
              ["product_id","product_category_name","product_weight_g","product_length_cm","product_height_cm","product_width_cm"])
    write_csv(os.path.join(OUT_DIR, "orders.csv"), orders,
              ["order_id","customer_id","order_status","order_purchase_timestamp","order_approved_at","order_delivered_carrier_date","order_delivered_customer_date","order_estimated_delivery_date"])
    write_csv(os.path.join(OUT_DIR, "order_items.csv"), order_items,
              ["order_id","order_item_id","product_id","seller_id","shipping_limit_date","price","freight_value"])
    write_csv(os.path.join(OUT_DIR, "order_payments.csv"), payments,
              ["order_id","payment_sequential","payment_type","payment_installments","payment_value"])
    write_csv(os.path.join(OUT_DIR, "order_reviews.csv"), reviews,
              ["review_id","order_id","review_score","review_comment_title","review_comment_message","review_creation_date","review_answer_timestamp"])

    print(f"Wrote CSVs to {OUT_DIR}")
    print("Files: customers.csv, sellers.csv, products.csv, orders.csv, order_items.csv, order_payments.csv, order_reviews.csv")

if __name__ == "__main__":
    main()