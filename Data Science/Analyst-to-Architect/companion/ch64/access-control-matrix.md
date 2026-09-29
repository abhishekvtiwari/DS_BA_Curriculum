# Riverstone platform access-control matrix

Companion to Chapter 64, Figure 64.1 and section 64.3. Closes the open risk from Chapter 60's
design document. Least privilege, stated as a specific, checkable table.

| Role | Own-branch orders | All-branch revenue | Customer PII | Model training data | Credential vault |
|---|---|---|---|---|---|
| Branch staff | Full (own branch only) | None | None | None | None |
| Regional manager | Full (own region's branches) | Read | Masked | None | None |
| Analytics team | Read | Read | Masked | Read | None |
| Data platform team | Read | Read | Break-glass | Full | Admin, logged |
| Pipelines (service accounts) | Load | Load | Load | Load | Read own secret |
| External auditor | Audit only | Audit only | Audit only | None | None |

## What each level means

- **Full**: create, change and delete. For branch staff, row-level security narrows it to their own
  branch's rows (section 64.3, step 5).
- **Read**: view only, no changes.
- **Masked**: customers appear only as a salted code (`customer_key`) with their branch; no name,
  contact person, phone or email (section 64.3, step 4).
- **Break-glass**: nobody holds it day to day. A named person gets it for a few hours, with an
  approval and a log, for a specific incident (Chapter 52, section 52.1).
- **Load**: a pipeline's service account copies the data in. It has no login a person can use, and its
  secret lives in the vault.
- **Admin, logged**: manage the vault (add, rotate and revoke secrets); every action is recorded.
- **Read own secret**: each pipeline can fetch only the one credential it needs, through a logged call.
- **Audit only**: view access logs and configuration, never the underlying data itself.
- **None**: no access of any kind.

## Checking it against Chapter 60's requirement

"No credential can read another branch's customer data":

- Branch staff: no customer PII; orders limited to their own branch by row-level security.
- Regional managers and the analytics team: customers only masked.
- External auditor: logs and settings, never the data.
- Data platform team: raw customer PII only through logged, approved break-glass access.
- Pipelines: the load service accounts do read every branch's customer data, because copying it into the
  warehouse is their job. They have no interactive login, and they are covered by the quarterly access
  review. The design document records the requirement as amended: "No person's credential can read
  another branch's customer data; the load pipelines' service accounts can, have no interactive login,
  and are covered by the quarterly access review."

## The quarterly access review

1. The platform team exports the grants the systems actually hold (section 64.3, step 6, and the same
   list from the cloud account and the BI tool).
2. They compare it, line by line, with this matrix.
3. Each resource's owner signs off every grant that matches and revokes every one that doesn't.
4. The dated record (who reviewed, what was revoked, who signed) is kept with the design document.

Review this matrix whenever a new role or resource category is added to the platform, not just each
quarter. See Chapter 63's automation inventory for the same principle applied to automations.
