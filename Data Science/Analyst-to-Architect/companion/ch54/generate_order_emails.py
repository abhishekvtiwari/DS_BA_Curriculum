#!/usr/bin/env python3
"""
Analyst to Architect · Chapter 54 · Generative AI & Large Language Models
File: generate_order_emails.py - builds the order emails the chapter's extraction project uses.
What: writes, under order_data/:
        emails/email_001.txt ...      60 purchase-order emails as Riverstone's sales inbox receives them,
                                      in the messy shapes real customers send: tables, prose, forwarded
                                      threads, missing fields, two POs in one mail.
        ground_truth.json             the correct extraction for each email, written by the generator,
                                      so the chapter can measure accuracy instead of claiming it.
How:  python3 generate_order_emails.py [--n 60]
Seed: 54 (fixed). Standard library only; nothing is downloaded and no model is called.
Tested on: Python 3.12.3 (Ubuntu 24.04).
Riverstone Supplies is fictional; every customer, order and number here is invented.
"""
import argparse, json, os, random
from datetime import date, timedelta

ap = argparse.ArgumentParser()
ap.add_argument('--n', type=int, default=60)
ap.add_argument('--out', default='order_data')
a = ap.parse_args()
rng = random.Random(54)
os.makedirs(f'{a.out}/emails', exist_ok=True)

CUSTOMERS = ['Sharma Hardware', 'Patel Kitchenware', 'Green Leaf Hotels', 'Coastal Foods', 'Metro Mart',
             'Sunrise Caterers', 'Harbour Traders', 'Evergreen Mart', 'Kitchen Kraft', 'Deccan Packaging']
PRODUCTS = {'101': 'Storage Box 10L', '102': 'Storage Box 25L', '103': 'Water Bottle 1L',
            '104': 'Food Container Set', '105': 'Industrial Crate', '106': 'Garden Chair',
            '107': 'Lunch Box Set', '108': 'Stackable Bin'}
SENDERS = ['purchase', 'accounts', 'stores', 'admin']

def money(n):
    return f'{n:,}'

emails, truth = [], {}
for i in range(1, a.n + 1):
    customer = rng.choice(CUSTOMERS)
    po_number = f'PO-{rng.randrange(20000, 99999)}'
    order_date = date(2026, 2, 1) + timedelta(days=rng.randrange(28))
    delivery = order_date + timedelta(days=rng.choice([7, 10, 14, 21]))
    items = []
    for code in rng.sample(list(PRODUCTS), rng.choice([1, 1, 2, 2, 3])):
        items.append({'product_code': code, 'product_name': PRODUCTS[code],
                      'quantity': rng.choice([10, 20, 25, 30, 50, 75, 100])})
    style = rng.choice(['table', 'prose', 'forwarded', 'bullets', 'terse'])
    sender = f'{rng.choice(SENDERS)}@{customer.split()[0].lower()}.example'
    lines = [f'From: {sender}', f'To: orders@riverstone.example',
             f'Subject: {rng.choice(["New order", "Purchase order " + po_number, "Order request", "PO attached (details below)"])}',
             f'Date: {order_date:%d %b %Y}', '']
    if style == 'forwarded':
        lines += ['---------- Forwarded message ----------',
                  f'From: {rng.choice(SENDERS)}@{customer.split()[0].lower()}.example',
                  'Please process the below. Thanks.', '']
    greeting = rng.choice(['Dear Riverstone team,', 'Hi,', 'Hello Riverstone,', 'Dear Sir/Madam,'])
    lines.append(greeting)
    lines.append('')
    if style == 'table':
        lines += [f'Please supply against our {po_number}:', '',
                  'Code | Item | Qty', '-----|------|----']
        for item in items:
            lines.append(f"{item['product_code']} | {item['product_name']} | {item['quantity']}")
        lines += ['', f'Delivery required by {delivery:%d %B %Y} at our {rng.choice(["Andheri", "Bhiwandi", "Wakad", "Peenya"])} warehouse.']
    elif style == 'prose':
        wants = ' and '.join(f"{item['quantity']} of the {item['product_name']} (code {item['product_code']})" for item in items)
        lines += [f'We would like to order {wants} against purchase order {po_number}.',
                  f'Kindly deliver by {delivery:%d/%m/%Y}. Our GST details are unchanged.']
    elif style == 'bullets':
        lines.append(f'Order reference: {po_number}')
        lines.append('')
        for item in items:
            lines.append(f"- {item['product_name']} ({item['product_code']}) x {item['quantity']} nos")
        lines += ['', f'Required by: {delivery:%Y-%m-%d}']
    elif style == 'terse':
        lines.append(f'{po_number}')
        for item in items:
            lines.append(f"{item['product_code']} - {item['quantity']}")
        lines.append(f'deliver {delivery:%d-%m-%Y}')
    else:
        lines.append(f'{po_number}: ' + ', '.join(f"{item['product_code']} x {item['quantity']}" for item in items))
        lines.append(f'Delivery {delivery:%d %b}')
    if rng.random() < 0.25:
        lines += ['', rng.choice([
            'Please confirm the freight charges separately.',
            'Note: our earlier enquiry about bulk pricing is still open.',
            'Invoice to the registered address, delivery to the warehouse.',
            'This supersedes our mail of last week.'])]
    lines += ['', rng.choice(['Regards,', 'Thanks and regards,', 'Best regards,']),
              rng.choice(['R. Menon', 'S. Iyer', 'A. Kulkarni', 'P. Shah', 'N. Das']),
              f'{customer}']
    text = '\n'.join(lines) + '\n'
    name = f'email_{i:03d}'
    open(f'{a.out}/emails/{name}.txt', 'w', encoding='utf-8').write(text)
    truth[name] = {'customer': customer, 'po_number': po_number,
                   'delivery_date': delivery.isoformat(),
                   'items': [{'product_code': it['product_code'], 'quantity': it['quantity']} for it in items]}
    emails.append(text)

json.dump(truth, open(f'{a.out}/ground_truth.json', 'w', encoding='utf-8'), indent=2)
styles = len({'table', 'prose', 'forwarded', 'bullets', 'terse'})
print(f'{len(emails)} emails written to {a.out}/emails/ in {styles} shapes')
print(f'ground truth for {len(truth)} emails, {sum(len(v["items"]) for v in truth.values())} order lines in total')
