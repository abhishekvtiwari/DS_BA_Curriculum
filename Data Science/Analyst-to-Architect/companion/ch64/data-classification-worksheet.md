# Data classification worksheet

For any dataset your platform holds, answer these questions. See Chapter 64,
sections 64.4-64.6.

| Question | Answer |
|---|---|
| What is this dataset? | |
| Who owns it (Chapter 62's data-product sense)? | |
| Does it contain personal data of identifiable individuals? | |
| If yes, whose (customers, employees, leads)? | |
| Which regulations plausibly apply (GDPR, DPDP Act, others)? | |
| What's the minimum retention period that's actually needed? | |
| Who currently has access, and does it match least privilege? | |
| Is it anonymized or pseudonymized anywhere it doesn't need identity? | |
| Is it cataloged and discoverable outside the owning team? | |
| When was this classification last reviewed? | |

## Worked example: `leads_scored_2025.csv`

| Question | Answer |
|---|---|
| What is this dataset? | Scored sales leads with company and contact details |
| Who owns it? | Sales operations (business owner); Analytics team (technical owner) |
| Contains personal data? | Yes — contact names and details, not included in the companion CSV's anonymized columns |
| Whose? | Prospective and existing business customers (leads) |
| Applicable regulation | India's DPDP Act (processing personal data of individuals in India) |
| Minimum retention | Duration of active sales relationship, plus a defined window after a lead goes cold |
| Current access | Sales team (read/write on their own leads), Analytics team (read, for scoring) |
| Anonymized where possible? | The companion dataset for this chapter's audit strips all personal identifiers, keeping only region, size band, recency, and score |
| Cataloged? | Yes, as of the Chapter 64 fairness audit — previously undocumented |
