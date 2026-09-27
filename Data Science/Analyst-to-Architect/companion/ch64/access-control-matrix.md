# Riverstone platform access-control matrix

Companion to Chapter 64, Figure 64.1. Closes the open risk from Chapter 60's
design document. Least privilege, stated as a specific, checkable table.

| Role | Own branch orders | All-branch revenue | Customer PII | Model training data | Credential vault |
|---|---|---|---|---|---|
| Branch staff | Full | None | None | None | None |
| Regional manager | Full | Read | None | None | None |
| Analytics team | Read | Read | Read | Read | None |
| Data platform team | Read | Read | Read | Full | Read |
| External auditor | Audit only | Audit only | Audit only | None | None |

**Full** = create, modify, delete. **Read** = view only, no changes.
**Audit only** = view access logs and configuration, never the underlying data itself.
**None** = no access of any kind.

## Notes

- Customer PII is read-only above branch-staff level, including for the data
  platform team — nobody needs write access to a customer's personal details
  to build or operate the platform.
- Credential vault access is itself logged; even the data platform team's
  "read" access here means retrieving a credential through an audited call,
  not viewing raw secret values in a dashboard.
- This matrix should be reviewed whenever a new role or resource category is
  added to the platform — not just annually. See Chapter 63's automation
  inventory review cadence for the same principle applied to automations.
