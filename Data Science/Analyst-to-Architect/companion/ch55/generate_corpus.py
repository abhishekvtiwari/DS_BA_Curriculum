#!/usr/bin/env python3
"""
Analyst to Architect · Chapter 55 · Building AI Applications: RAG, Agents & Evaluation
File: generate_corpus.py - builds Riverstone's document corpus and the question set the chapter measures against.
What: writes, under corpus/:
        docs/*.md          Riverstone's own documents: 8 product spec sheets, 8 policies (one of them an
                           outdated version that is still in the folder, as in every real company),
                           a price list, an escalation contact sheet, and 10 FAQ entries.
        questions.json     65 support questions with the document each one should be answered from.
                           Ten of them are deliberately unanswerable from this corpus, because the most
                           valuable thing a support assistant does is say so.
How:  python3 generate_corpus.py
No randomness: every run writes the same files. Standard library only; nothing is downloaded.
Tested on: Python 3.11 and 3.12.
Riverstone Supplies is fictional; every product, policy and number here is invented.
"""
import json, os, pathlib, textwrap

OUT = pathlib.Path('corpus')
(OUT / 'docs').mkdir(parents=True, exist_ok=True)

PRODUCTS = {
    '101': dict(name='Storage Box 10L', category='Storage', price=430, material='Polypropylene',
                dims='34 x 24 x 18 cm', weight='0.78 kg', colours='Blue, Grey, Translucent',
                load='12 kg stacked', temp='-10 C to 80 C', moq=20, lead=5),
    '102': dict(name='Storage Box 25L', category='Storage', price=750, material='Polypropylene',
                dims='48 x 34 x 22 cm', weight='1.55 kg', colours='Blue, Grey',
                load='25 kg stacked', temp='-10 C to 80 C', moq=20, lead=5),
    '103': dict(name='Water Bottle 1L', category='Kitchen', price=115, material='Food-grade PP',
                dims='8 x 8 x 27 cm', weight='0.11 kg', colours='Clear, Blue, Green',
                load='not stackable', temp='0 C to 60 C', moq=50, lead=3),
    '104': dict(name='Food Container Set', category='Kitchen', price=620, material='Food-grade PP',
                dims='set of 3, largest 22 x 16 x 9 cm', weight='0.46 kg', colours='Clear with red lids',
                load='6 kg stacked', temp='-20 C to 100 C (microwave safe)', moq=25, lead=4),
    '105': dict(name='Industrial Crate', category='Industrial', price=1400, material='HDPE',
                dims='60 x 40 x 32 cm', weight='2.9 kg', colours='Black, Yellow',
                load='60 kg stacked', temp='-25 C to 90 C', moq=10, lead=7),
    '106': dict(name='Garden Chair', category='Furniture', price=1150, material='PP with steel frame',
                dims='55 x 52 x 88 cm', weight='3.4 kg', colours='White, Green',
                load='120 kg user weight', temp='outdoor use, UV stabilised', moq=8, lead=10),
    '107': dict(name='Lunch Box Set', category='Kitchen', price=380, material='Food-grade PP',
                dims='set of 2, 18 x 13 x 7 cm', weight='0.28 kg', colours='Pink, Blue, Green',
                load='not stackable', temp='-20 C to 100 C (microwave safe)', moq=50, lead=3),
    '108': dict(name='Stackable Bin', category='Storage', price=290, material='Polypropylene',
                dims='30 x 20 x 15 cm', weight='0.42 kg', colours='Grey, Red, Blue',
                load='8 kg stacked', temp='-10 C to 80 C', moq=30, lead=5),
}

def write(name, text):
    (OUT / 'docs' / f'{name}.md').write_text(textwrap.dedent(text).strip() + '\n', encoding='utf-8')

questions = []

for code, p in PRODUCTS.items():
    write(f'spec_{code}', f"""
        # {p['name']} (product code {code})

        ## Overview
        The {p['name']} is part of Riverstone's {p['category']} range, moulded at the Taloja plant
        from {p['material']}.

        ## Specification
        - Product code: {code}
        - Material: {p['material']}
        - Dimensions: {p['dims']}
        - Weight: {p['weight']}
        - Colours available: {p['colours']}
        - Load rating: {p['load']}
        - Temperature range: {p['temp']}
        - List price: Rs {p['price']} per unit, excluding GST

        ## Ordering
        - Minimum order quantity: {p['moq']} units
        - Standard lead time: {p['lead']} working days from order confirmation
        - Bulk pricing applies above 500 units; see the bulk discount policy.

        ## Care
        Clean with mild detergent and water. Do not use abrasive cleaners or solvents.
        """)
    questions += [
        dict(question=f"What is the load rating of the {p['name']}?", doc=f'spec_{code}', answer=p['load']),
        dict(question=f"What is the minimum order quantity for product {code}?", doc=f'spec_{code}', answer=str(p['moq'])),
        dict(question=f"How long is the lead time for the {p['name']}?", doc=f'spec_{code}', answer=f"{p['lead']} working days"),
    ]

write('policy_delivery', """
    # Delivery policy (current, revision 4, effective 1 January 2026)

    Riverstone delivers across India from the Bhiwandi Main warehouse and the Chakan dispatch point.

    - Orders confirmed before 14:00 on a working day are dispatched the same day where stock allows.
    - Standard delivery is 3 to 5 working days for Maharashtra and 5 to 9 working days elsewhere.
    - Delivery is free on orders above Rs 25,000 excluding GST. Below that, freight is charged at actuals.
    - We do not deliver on Sundays or on national holidays.
    - A delivery attempt is made twice. After two failed attempts the consignment returns to the warehouse
      and re-delivery is charged.
    """)
questions += [dict(question="Is delivery free, and above what order value?", doc='policy_delivery', answer='Rs 25,000'),
              dict(question="How many delivery attempts are made before a consignment is returned?", doc='policy_delivery', answer='two'),
              dict(question="What is the standard delivery time outside Maharashtra?", doc='policy_delivery', answer='5 to 9 working days')]

write('policy_delivery_rev3_superseded', """
    # Delivery policy (revision 3, SUPERSEDED on 1 January 2026)

    This revision is retained for reference only. Do not quote it to customers.

    - Delivery was free on orders above Rs 40,000 excluding GST.
    - Standard delivery was 5 to 7 working days for Maharashtra and 7 to 12 working days elsewhere.
    """)

write('policy_returns', """
    # Returns and replacements policy

    - Damage in transit must be reported within 48 hours of delivery, with photographs.
    - Manufacturing defects are replaced free of charge within the warranty period.
    - Goods ordered in error may be returned within 15 days if unused and in original packaging.
      A restocking fee of 10% applies, and freight both ways is charged to the customer.
    - Custom-moulded and printed items cannot be returned.
    - Approved replacements are dispatched within 3 working days of the return being received.
    """)
questions += [dict(question="How soon must transit damage be reported?", doc='policy_returns', answer='48 hours'),
              dict(question="What is the restocking fee on goods ordered in error?", doc='policy_returns', answer='10%'),
              dict(question="Can printed items be returned?", doc='policy_returns', answer='no')]

write('policy_warranty', """
    # Warranty terms

    - All moulded products carry a 12-month warranty against manufacturing defects from the date of invoice.
    - The Industrial Crate (product 105) carries an extended 24-month warranty.
    - The warranty covers cracking, splitting and deformation under the stated load rating.
    - It does not cover damage from misuse, exposure beyond the stated temperature range, or normal wear.
    - Warranty claims require the invoice number and photographs of the defect.
    """)
questions += [dict(question="How long is the standard warranty?", doc='policy_warranty', answer='12 months'),
              dict(question="Which product has a 24-month warranty?", doc='policy_warranty', answer='Industrial Crate (105)'),
              dict(question="What does the warranty not cover?", doc='policy_warranty', answer='misuse, temperature abuse, normal wear')]

write('policy_payment', """
    # Payment terms

    - New customers: 100% advance for the first two orders.
    - Established customers: 30 days from invoice date, subject to an approved credit limit.
    - Key accounts with a signed agreement: 45 days from invoice date.
    - Interest of 1.5% per month is chargeable on overdue amounts.
    - Payment by NEFT, RTGS or cheque. Cash is not accepted for orders above Rs 10,000.
    """)
questions += [dict(question="What are the payment terms for a new customer?", doc='policy_payment', answer='100% advance for the first two orders'),
              dict(question="What interest is charged on overdue invoices?", doc='policy_payment', answer='1.5% per month')]

write('policy_bulk_discount', """
    # Bulk discount policy

    Discounts are applied on the list price, per order, per product code.

    - 500 to 999 units: 5%
    - 1,000 to 4,999 units: 8%
    - 5,000 units and above: 12%
    - Discounts above 12% require the Sales Head's written approval.
    - Bulk discounts do not stack with promotional pricing.
    """)
questions += [dict(question="What discount applies to an order of 2,000 units?", doc='policy_bulk_discount', answer='8%'),
              dict(question="Who approves a discount above 12%?", doc='policy_bulk_discount', answer="the Sales Head")]

write('policy_packaging', """
    # Packaging and labelling

    - Products are packed in corrugated cartons supplied by Deccan Cartons.
    - Standard carton quantities: 10 units for storage boxes, 25 for kitchen items, 4 for garden chairs.
    - Each carton carries the product code, batch number, quantity and the moulding date.
    - Customer-specific labelling is available above 2,000 units at Rs 3 per unit.
    """)
questions += [dict(question="How many garden chairs are in a standard carton?", doc='policy_packaging', answer='4'),
              dict(question="What does custom labelling cost?", doc='policy_packaging', answer='Rs 3 per unit above 2,000 units')]

write('policy_gst_invoicing', """
    # GST and invoicing

    - All prices are quoted excluding GST. Moulded plastic goods attract 18% GST.
    - Invoices are raised on dispatch and emailed to the address on the purchase order.
    - A customer GSTIN is required before the first invoice.
    - Credit notes for approved returns are issued within 7 working days.
    """)
questions += [dict(question="What GST rate applies to Riverstone products?", doc='policy_gst_invoicing', answer='18%'),
              dict(question="When are invoices raised?", doc='policy_gst_invoicing', answer='on dispatch')]

write('price_list', """
    # Price list (effective 1 February 2026, excluding GST)

    | Code | Product | List price (Rs) |
    |---|---|---|
    | 101 | Storage Box 10L | 430 |
    | 102 | Storage Box 25L | 750 |
    | 103 | Water Bottle 1L | 115 |
    | 104 | Food Container Set | 620 |
    | 105 | Industrial Crate | 1400 |
    | 106 | Garden Chair | 1150 |
    | 107 | Lunch Box Set | 380 |
    | 108 | Stackable Bin | 290 |

    Prices are reviewed quarterly. Regional pricing differences may apply; confirm with your sales contact.
    """)
questions += [dict(question="What is the list price of the Industrial Crate?", doc='price_list', answer='Rs 1,400'),
              dict(question="How often are prices reviewed?", doc='price_list', answer='quarterly')]

write('contacts_escalation', """
    # Who to contact

    - Order status and dispatch: the customer support desk, support@riverstone.example.
    - Pricing and discounts beyond policy: your regional sales manager.
    - Quality complaints and warranty claims: quality@riverstone.example, with the invoice number.
    - Anything unresolved after 3 working days: escalate to the Customer Support Lead.
    """)
questions += [dict(question="Who should a warranty claim be sent to?", doc='contacts_escalation', answer='quality@riverstone.example'),
              dict(question="When should a customer escalate to the Support Lead?", doc='contacts_escalation', answer='after 3 working days unresolved')]

FAQ = [
    ('Are the storage boxes food safe?', 'Only the Kitchen range (codes 103, 104, 107) is made from food-grade PP. Storage boxes are not certified for food contact.'),
    ('Can the crates be used in a freezer?', 'The Industrial Crate is rated to -25 C and is suitable for freezer use. Storage boxes are rated to -10 C.'),
    ('Do you supply in custom colours?', 'Custom colours are available above 5,000 units per colour, with a 15 working day lead time and a one-time masterbatch charge.'),
    ('Is there a showroom?', 'Samples are couriered on request; there is no public showroom. Sample charges are adjusted against the first order.'),
    ('Do you export?', 'Riverstone supplies within India only at present.'),
    ('Can I collect the goods myself?', 'Self-collection is available from Bhiwandi Main between 10:00 and 17:00 on working days, with 24 hours notice.'),
    ('What is the shelf life of the products?', 'Moulded products have no shelf life if stored away from direct sunlight. UV exposure over years causes fading.'),
    ('Are the lids interchangeable between box sizes?', 'No. Each box size has its own lid; the 10L and 25L lids are not interchangeable.'),
    ('Do you offer a rental option for crates?', 'No. Crates are sold outright.'),
    ('Can I change an order after confirmation?', 'Changes are possible before dispatch. Contact the support desk with the PO number; changes after dispatch are treated as a return.'),
]
for i, (q, a) in enumerate(FAQ, start=1):
    write(f'faq_{i:02d}', f"""
        # FAQ: {q}

        {a}
        """)
    questions.append(dict(question=q, doc=f'faq_{i:02d}', answer=a))

UNANSWERABLE = [
    'What is Riverstone\'s turnover this year?',
    'Do you supply to Sri Lanka?',
    'Can I get a 30% discount on 100 units?',
    'Who is the Managing Director\'s personal assistant?',
    'What is the salary of a machine operator at Taloja?',
    'Is the Garden Chair available in purple?',
    'Do you accept cryptocurrency?',
    'What is the recycled content percentage of the Stackable Bin?',
    'Can I visit the Chakan plant next week?',
    'What is the warranty on a competitor\'s crate?',
]
for q in UNANSWERABLE:
    questions.append(dict(question=q, doc=None, answer=None))

json.dump(questions, open(OUT / 'questions.json', 'w', encoding='utf-8'), indent=2)
docs = sorted((OUT / 'docs').glob('*.md'))
answerable = sum(1 for q in questions if q['doc'])
print(f'{len(docs)} documents, {sum(len(d.read_text(encoding="utf-8").split()) for d in docs):,} words')
print(f'{len(questions)} questions: {answerable} answerable, {len(questions) - answerable} deliberately not')
