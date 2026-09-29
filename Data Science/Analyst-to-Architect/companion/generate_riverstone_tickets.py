"""
Analyst to Architect · Riverstone support tickets (first used in Chapter 41)
generate_riverstone_tickets.py: free-text customer support tickets, 2024-2025.

Run:     python3 generate_riverstone_tickets.py       (writes into companion/tickets/)
Writes:  tickets/tickets.csv
Seed:    20241 (repeat contacts: 20242)
Tested:  Python 3.11.15, NumPy 2.4.6, pandas 3.0.6 (29 September 2026)
Spec:    planning/data/riverstone-tickets.md

Riverstone Supplies is fictional; every name and number is invented. Ticket text is templated and
randomized, not copied from any real support system.
"""
import pathlib
import re
import numpy as np
import pandas as pd

rng = np.random.default_rng(20241)
OUT = pathlib.Path(__file__).resolve().parent / "tickets"
OUT.mkdir(exist_ok=True)
N = 3000

TOPICS = ["Delivery", "Product Defect", "Billing", "Order Change", "General Enquiry"]
TOPIC_P = [0.30, 0.20, 0.18, 0.14, 0.18]
PRODUCTS = ["storage bin", "food container", "industrial crate", "garden chair", "plastic pallet",
            "chopping board", "bulk drum", "stacking tray"]
NAMES = ["Rakesh", "Priya", "Suresh", "Anjali", "Vikram", "Neha", "Farhan", "Divya", "Arjun", "Kavita"]

# ---- templates: (topic, sentiment, list of body templates with {product}/{days}/{order}/{amount} slots) ----
TEMPLATES = {
    ("Delivery", "frustrated"): [
        "This is the {n} time I am writing. My order #{order} was supposed to arrive {days} days ago and there is still no {product}. Very disappointed with this service.",
        "Extremely unhappy. {days} days late and no update from your courier. I need the {product} urgently for my shop, please escalate this now.",
        "Order {order} still not delivered after {days} days!! I called twice and nobody called back. This is not acceptable.",
    ],
    ("Delivery", "neutral"): [
        "Could you please share an update on order #{order}? It has been {days} days since dispatch and I wanted to check the status.",
        "Hi, just checking when order {order} will reach us. The tracking page has not updated in {days} days.",
    ],
    ("Delivery", "positive"): [
        "Order {order} arrived today, a day early actually. Thanks for the quick delivery on the {product}!",
        "Just wanted to say the {product} order came in good condition and on time. Appreciate it.",
    ],
    ("Product Defect", "frustrated"): [
        "The {product} we received is completely broken, there is a crack right down the middle. This is the second defective piece from order {order}, I want a replacement immediately.",
        "Very poor quality control. The {product} lid does not close properly and the whole batch from order #{order} seems faulty.",
        "I am extremely disappointed, the {product} arrived damaged and unusable. Please refund order {order}.",
    ],
    ("Product Defect", "neutral"): [
        "The {product} from order #{order} has a small crack on one side. Is this covered under warranty?",
        "One of the {product} units in order {order} seems to have a manufacturing defect. Can you advise next steps?",
    ],
    ("Product Defect", "positive"): [
        "Noticed a minor scratch on the {product} but wanted to flag it, otherwise the quality is good.",
    ],
    ("Billing", "frustrated"): [
        "I have been charged twice for order #{order}, amount Rs {amount} deducted two times from my account. Please refund immediately, this is unacceptable.",
        "Your invoice for order {order} shows the wrong GST amount, Rs {amount} extra. I have raised this before and nothing has been done.",
    ],
    ("Billing", "neutral"): [
        "Could you clarify the invoice for order #{order}? The amount Rs {amount} does not match what we discussed with the sales rep.",
        "Requesting a copy of the GST invoice for order {order}, amount Rs {amount}, for our accounts team.",
    ],
    ("Billing", "positive"): [
        "Thanks for correcting the invoice for order {order} so quickly, much appreciated.",
    ],
    ("Order Change", "frustrated"): [
        "I asked to change the quantity on order #{order} three days ago and nobody has confirmed it yet. The {product} order needs to go out this week.",
    ],
    ("Order Change", "neutral"): [
        "Can we change the delivery address for order #{order}? We are shifting our {product} godown next week.",
        "Please update order {order} to add 2 more units of {product} before it ships.",
        "We would like to cancel order #{order} for the {product}, our requirement has changed.",
    ],
    ("Order Change", "positive"): [
        "Thanks for updating order {order} so smoothly, the new address is confirmed on your end I hope.",
    ],
    ("General Enquiry", "neutral"): [
        "Do you have the {product} available in bulk quantity? Looking for pricing for around {amount} units.",
        "What is the minimum order quantity for {product}? We are a new hospitality business in setting up phase.",
        "Is there a catalogue with all {product} variants and sizes? Want to compare before placing order #{order}.",
        "Just enquiring about GST details and payment terms for a first-time wholesale order of {product}.",
    ],
    ("General Enquiry", "positive"): [
        "Really impressed with the range of {product} on your website, will place an order soon.",
    ],
}
SENTIMENT_BY_TOPIC = {"Delivery": [0.42, 0.38, 0.20], "Product Defect": [0.55, 0.35, 0.10],
                     "Billing": [0.40, 0.45, 0.15], "Order Change": [0.15, 0.70, 0.15],
                     "General Enquiry": [0.0, 0.75, 0.25]}
SUBJECTS = {"Delivery": ["Where is my order", "Delivery delay", "Order status", "Late shipment"],
           "Product Defect": ["Damaged item received", "Quality issue", "Broken product", "Defective piece"],
           "Billing": ["Invoice query", "Double charge", "GST invoice request", "Billing issue"],
           "Order Change": ["Change order request", "Cancel order", "Update delivery address", "Add items to order"],
           "General Enquiry": ["Bulk pricing enquiry", "Product availability", "New customer question", "Catalogue request"]}

topic = rng.choice(TOPICS, size=N, p=TOPIC_P)
sentiment = np.array([rng.choice(["frustrated", "neutral", "positive"], p=SENTIMENT_BY_TOPIC[t]) for t in topic])
created = pd.Timestamp("2024-01-01") + pd.to_timedelta(rng.integers(0, 730, N), unit="D")
order_ids = rng.integers(100001, 100001 + 12000, N)
days_late = np.clip(rng.poisson(6, N), 1, 30)
amounts = np.round(rng.lognormal(9, 0.9, N), -1).astype(int)

def typo(text, rate=0.03):
    chars = list(text); out = []
    for c in chars:
        r = rng.random()
        if r < rate * 0.4 and c.isalpha():
            continue                                    # drop a letter
        out.append(c)
        if r < rate * 0.3 and c == " ":
            out.append(" ")                              # double space
    return "".join(out)

# templates that say the customer has been in touch before about the same order
REPEAT_PHRASES = ["time I am writing", "called twice", "second defective piece", "raised this before"]

bodies, subjects, products, repeat_wording = [], [], [], []
for i in range(N):
    key = (topic[i], sentiment[i])
    body = rng.choice(TEMPLATES[key])
    repeat_wording.append(any(phrase in body for phrase in REPEAT_PHRASES))
    product = rng.choice(PRODUCTS)
    products.append(product)
    body = body.format(product=product, days=days_late[i], order=order_ids[i],
                       amount=amounts[i], n=rng.choice(["2nd", "3rd", "4th"]))
    if rng.random() < 0.25:
        body = f"Dear team, {body[0].lower()}{body[1:]}"
    if rng.random() < 0.15:
        body += " Kindly do the needful at the earliest."
    if rng.random() < 0.4:
        body = typo(body)
    bodies.append(body)
    subjects.append(rng.choice(SUBJECTS[topic[i]]))

resolution_hours = np.round(np.clip(rng.gamma(2, 8, N) * np.where(sentiment == "frustrated", 0.7, 1.0), 0.5, 200), 1)
satisfaction = np.clip(np.round(rng.normal(np.select([sentiment == "frustrated", sentiment == "neutral", sentiment == "positive"], [2.1, 3.4, 4.6]), 0.8)), 1, 5).astype(int)
customer = np.array([rng.choice(NAMES) for _ in range(N)])

tickets = pd.DataFrame({
    "ticket_id": np.arange(700001, 700001 + N), "created_at": created.strftime("%Y-%m-%d"),
    "customer_name": customer, "subject": subjects, "body": bodies, "topic": topic,
    "sentiment": sentiment, "order_id": order_ids, "resolution_hours": resolution_hours,
    "satisfaction_score": satisfaction,
})
# a handful of genuinely ambiguous / mixed tickets (hard even for a human)
mix_idx = rng.choice(N, 40, replace=False)
mixed = mix_idx[:20]
tickets.loc[mixed, "body"] = ("The " + pd.Series(products)[mixed].values +
                              " was fine but the delivery was late and the invoice amount looks off, please check.")

# repeat contacts: most tickets whose wording says "I've been in touch before" really do follow an
# earlier ticket on the same order (the rest followed a phone call, which the ticket log never saw).
# A separate random stream, so every other column is unchanged.
rng2 = np.random.default_rng(20242)
dates = pd.to_datetime(tickets["created_at"])
is_mixed = np.zeros(N, dtype=bool); is_mixed[mixed] = True
candidates = np.flatnonzero(np.array(repeat_wording) & ~is_mixed)
for i in candidates[np.argsort(dates.values[candidates], kind="stable")]:   # oldest first
    if rng2.random() >= 0.8:
        continue                                        # the earlier contact was a phone call
    earlier = np.flatnonzero((tickets["topic"].values == tickets.at[i, "topic"]) & ~is_mixed &
                             (dates < dates[i]).values & (dates >= dates[i] - pd.Timedelta(days=30)).values)
    if len(earlier) == 0:
        continue
    first = rng2.choice(earlier)
    old, new = str(tickets.at[i, "order_id"]), str(tickets.at[first, "order_id"])
    tickets.at[i, "body"] = re.sub(rf"\b{old}\b", new, tickets.at[i, "body"])
    tickets.at[i, "order_id"] = tickets.at[first, "order_id"]
    tickets.at[i, "customer_name"] = tickets.at[first, "customer_name"]
tickets.to_csv(OUT / "tickets.csv", index=False)
def counts(column):
    return ", ".join(f"{name} {n:,}" for name, n in tickets[column].value_counts().items())

print(f"{N:,} tickets written to tickets/tickets.csv")
print(f"topics: {counts('topic')}")
print(f"sentiment: {counts('sentiment')}")
