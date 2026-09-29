# Data classification worksheet

For any dataset your platform holds, answer these questions. See Chapter 64,
sections 64.3 to 64.6.

| Question | Answer |
|---|---|
| What is this dataset? | |
| Who owns it (Chapter 62's data-product sense)? | |
| Classification: public, internal, or confidential/personal? | |
| Does it contain personal data (PII) of identifiable individuals? | |
| If yes, whose (customers' contacts, employees, leads' contacts)? | |
| Which regulations plausibly apply (DPDP Act, GDPR, others)? | |
| What's the minimum retention period that's actually needed? | |
| Who currently has access, and does it match the access-control matrix? | |
| Is it pseudonymized or anonymized anywhere it doesn't need identity? | |
| May it go into an AI assistant? (public: any tool; internal: approved tools only; confidential/personal: never) | |
| Is it cataloged and discoverable outside the owning team? | |
| When was this classification last reviewed? | |

## The three classification levels

- **Public**: already published (price lists, the website). May go into any tool.
- **Internal**: orders, prices, plans, anything not published. Approved tools only, under a contract.
- **Confidential or personal**: customer and employee personal data, credentials, unreleased financials.
  Never into an AI assistant, and never out of the approved systems.

## Worked example: Riverstone's CRM leads (the data behind `leads_scored_2025.csv`)

| Question | Answer |
|---|---|
| What is this dataset? | Scored sales leads with company and contact details |
| Who owns it? | Sales (business owner, Anita Rao); analytics (technical owner) |
| Classification | Confidential/personal in the CRM; the companion CSV, with no contact details, is internal |
| Contains personal data? | Yes: each lead's contact person's name, phone and email (not in the companion CSV) |
| Whose? | Contact persons at prospective and existing business customers |
| Applicable regulation | India's DPDP Act: digital personal data of people in India (main duties from 13 May 2027) |
| Minimum retention | Duration of the active sales relationship, plus a defined window after a lead goes cold |
| Current access | Sales team (read/write on their own leads); analytics (masked, for scoring) |
| Pseudonymized where possible? | The audit dataset keeps only region, size band, recency, industry and score |
| May it go into an AI assistant? | The CRM data: never. The companion CSV: approved tools only |
| Cataloged? | Yes, as of the Chapter 64 fairness audit; previously undocumented |
| Last reviewed | The date of the Chapter 64 audit |
