# Microsoft deployment guide

**Not deployed:** these steps require access to a configured Microsoft tenant. The repository contains a local reference and implementation specification, not a ready-to-import managed solution.

## Preflight

1. Select a development Power Platform environment and a synthetic-data-only SharePoint site. Confirm ownership, maker rights and DLP policy.
2. Confirm capacity and licensing for Copilot Studio, Teams, SharePoint, Power Automate. Confirm any paid action with your organization before enabling it.
3. Create a named solution, environment variables and service connection references. Restrict makers and reviewers to the test group.
4. Create the lists/tables in [data contract](data-contract.md). Enforce unique keys at the datastore, not only in flow conditions.
5. Define the approver group, recipient allowlist, retention and failure recovery owner. Use a secure connector or Key Vault for secrets.

## Build the workflow

### 1. When an agent calls the flow

Inputs: RequestKey, category, description, confirmed. Resolve requester identity from a trusted authenticated context.

### 2. Validate request

Reject blank fields, unsupported category, description over 2000 characters, missing caller, or unconfirmed submissions.

### 3. Reserve key

Use a unique RequestKey column. Serialize demo trigger or use an atomic Dataverse alternate-key reservation for scale.

### 4. Create ticket

Create SharePoint item with caller identity and New status. On unique-key conflict load existing and compare immutable payload.

### 5. Respond to agent

Return ticket ID and status. Never echo raw connector exceptions.

### 6. Failure scope

Run after failed or timed-out actions. Log correlation ID, error code and stage; return retriable failure.

## Validate and release

1. Run the local suite and walkthrough for expected behavior; do not treat it as cloud validation.
2. Repeat all PRD acceptance rows in the tenant. Capture run IDs, input versions, expected/actual results and timestamps.
3. Use at least an ordinary employee/test user and a restricted reviewer/admin to test access. Verify unauthorized input fails before any write.
4. Inject invalid inputs, a duplicate submission, connector permission denial and a timeout after a write. Reconcile the remote system before retrying uncertain writes.
5. Inspect all artifacts for secrets and real data. Export the actual unmanaged solution via Power Platform tooling; bind connection references when importing into another environment.
6. Record a 2-4 minute demo from the actual Microsoft UI, including one success and one refusal/review case. Add sanitized screenshots and tenant test results.
7. Update docs/evidence-status.md only for verified capabilities. Keep prototype, pilot and production claims separate.

## Rollback

Disable triggers and distribution first. Preserve the audit ledger and remote references. Revert to the prior solution version in the dev environment; reconcile pending deliveries rather than replaying them blindly. Do not delete source records or logs as part of rollback. Remove only explicitly disposable synthetic records after the test owner agrees.

## References

- [SharePoint knowledge](https://learn.microsoft.com/microsoft-copilot-studio/knowledge-add-sharepoint)
