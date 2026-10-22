# Product requirements: Enterprise AI Employee Support Agent

Version 1.0 • October 22, 2026 • Product owner: Richard Parr

## Problem and users

Employees repeatedly search HR and IT policies, while support teams handle duplicate requests.

Users: Employees, HR knowledge owners, IT support agents, tenant administrators.

## Outcome and success definition

Deliver a reviewable automation with source traceability, deterministic validation, explicit approvals and replay protection. The local reference must pass its supplied positive and negative tests. Cloud completion requires the same scenarios executed in the Microsoft environment, an authorized pilot and an exported solution or report evidence.

No adoption, hours saved, accuracy percentage or financial return is claimed by this PRD. Any target below is a proposed pilot criterion rather than a measured result.

## MVP scope

1. Ground policy responses in permission-filtered SharePoint knowledge with visible citations.
2. Provide IT, HR, software access and escalation paths; abstain when sources are absent.
3. Collect category and description, show a confirmation card, then create one ticket per request.
4. Return a ticket reference; restrict ticket-status access to the requester and authorized support staff.

## Explicit exclusions and reference limits

- Keyword retrieval is a deterministic local reference, not Copilot Studio generative answers.
- CLI group names simulate permission contexts. They do not authenticate the caller.
- The reference lists ticket IDs and categories locally; real requester-specific status lookup belongs in the authenticated cloud flow.
- No production rollout, financial transactions or unsolicited external messages.
- No real employee, meeting or financial records in the public repository.
- No guarantee that local approval or identity simulation enforces tenant security.

## Functional requirements and traceability

| ID | Required behavior | Local test evidence |
|---|---|---|
| SUP-01 | Authorized policy answers include a document citation; unsupported policy questions escalate. | test_authorized_grounded_answer; test_unknown_policy_not_invented |
| SUP-02 | Restricted knowledge is never returned to the employee test role. | test_restricted_document_hidden |
| SUP-03 | Tickets require explicit confirmation and validated category and description. | test_ticket_confirmation; test_invalid_inputs |
| SUP-04 | Identical retries return one ticket; conflicting reuse fails. | test_ticket_retry_and_payload_conflict |
| SUP-05 | Storage errors surface instead of returning a false success. | test_storage_failure_surfaces |

Cloud acceptance must separately validate connector semantics, end-user permissions, approver identity, retries and delivery reconciliation. Local test names do not imply those cloud tests were performed.

## User journey

1. An authorized user or scheduled trigger submits a source reference and unique version key.
2. The workflow validates inputs and reserves the processing key before expensive work.
3. The automation retrieves permitted source data and produces the proposed response or structured result.
4. Validation checks required fields, provenance and business rules. Uncertainty goes to review.
5. A verified reviewer approves the exact version before any external action.
6. The workflow persists action references, audit status and a user-visible outcome.
7. Retries use the existing version ledger; changed content requires a new version.

## Data model

### SupportTickets

| Field | Definition |
|---|---|
| RequestKey | Text; required; unique |
| Title | Text; description summary |
| RequesterObjectId | Text; derived from authenticated identity |
| Category | Choice: IT, HR, Access, Other |
| Description | Multiline text; max 2000 characters |
| Status | Choice: New, InProgress, Resolved |
| CorrelationId | Text |
| Created | System timestamp |

### SupportAudit

| Field | Definition |
|---|---|
| CorrelationId | Text |
| Stage | Text |
| Outcome | Choice |
| ErrorCode | Text; no raw document data |

## State and failure model

Use Pending/Received, Validated, PendingReview, Approved, Completed, Rejected and Failed as the conceptual lifecycle; project-specific state names are defined in the data contract. Keep processing status distinct from remote delivery status. Retry network failures only when replay is safe. Do not retry validation errors. A timeout after a remote write may have succeeded: enter reconciliation instead of blindly creating another remote record.

Corrected inputs receive a new version key, linked to the original for audit. Never mutate an approved payload silently. Local SQLite transactions guard local state; they cannot make external Microsoft API writes atomic.

## Nonfunctional requirements

- Identity: Entra authentication; resolve roles from trusted identity claims and enforce source authorization in the data layer.
- Secrets: managed connection references or approved secret store; no tokens in Git, logs or prompts.
- Data protection: synthetic data in demos; production retention, geographic location and DLP approved by tenant owner.
- Reliability: unique keys, transaction-backed reservations, bounded retry and a manual recovery queue.
- Observability: correlation ID, source/version reference, attempt, stage, result and timestamps; exclude raw sensitive text.
- Accessibility: readable text, table headings, visible status and no color-only meaning in the eventual tenant UI.
- Performance pilot target: measure median and p95 end-to-end latency on at least 20 representative sources. Set budget only after baseline collection.
- Availability: no production SLA for this portfolio reference; tenant SLA and ownership require a separate operational agreement.

## Build sequence and deliverables

| Stage | Milestone | Work and exit condition |
|---|---|---|
| 1 | Knowledge and policies | Create the synthetic document library, owners, review dates and restricted sublibrary. |
| 2 | Agent behavior | Create the agent, add instructions and SharePoint knowledge, configure Microsoft authentication and abstention. |
| 3 | Ticket flow | Implement confirmation, server-derived requester, unique RequestKey, ticket creation and response. |
| 4 | Pilot and evidence | Publish to a test Teams group, execute role-based tests and capture solution export and screenshots. |

Sequence across portfolio: support agent, meeting automation, document processing, executive reporting. Each project has its own commit history, tests and deployment gate.

## Dependencies and licensing gate

Target stack: Copilot Studio, Teams, SharePoint, Power Automate. A tenant owner must verify environment roles, SharePoint permissions, premium connector availability, Copilot/AI Builder capacity, Azure deployment quota and Power BI sharing rights as applicable. This repository does not provision resources or incur cloud charges. Do not hard-code trial eligibility or prices.

## Pilot acceptance

- All local automated tests pass with evidence recorded.
- All requirement rows pass in a configured tenant using synthetic data.
- Two differently authorized test users demonstrate expected access boundaries.
- Duplicate, rejection, missing-data and downstream-failure scenarios produce correct audit states.
- Sanitized Microsoft solution export/report artifact, real screenshots and a 2-4 minute demonstration are attached.
- A business owner signs off the source-of-truth data, KPI meanings and reviewer routing.

## Risks and mitigations

| Risk | Mitigation | Owner |
|---|---|---|
| Model produces unsupported facts | Source evidence, schema checks and human review | AI solution owner |
| Connector runs with broader access than user | Least privilege, caller authorization and dual-user tests | Tenant admin |
| Retry duplicates a remote write | Unique ledger plus post-timeout reconciliation | Workflow owner |
| Source content changes after approval | Versioned keys and exact approved payload hash | Data owner |
| Trial or licensing gaps prevent demo | Validate capacity and permissions before provisioning | Tenant admin |
| Prototype mistaken for deployment | Evidence status in README and release checklist | Portfolio owner |

## Measurement and resume evidence

Measure baseline manual effort, automated processing effort, reviewer time, success rate, review rate, error rate and actual cost over a documented sample. Preserve numerator, denominator, sample selection and environment. Describe local reference and cloud pilot separately. Do not claim production deployment or percentage savings until verified.

## Release definition

Local reference release: code, fixtures, tests, executed walkthrough, PRD and implementation plan committed. Microsoft pilot release: tenant prerequisites configured, native artifacts exported, acceptance evidence recorded and approved test group onboarded. Production release: separate security, support, cost and retention approval.

## Authoritative implementation references

- [SharePoint knowledge](https://learn.microsoft.com/microsoft-copilot-studio/knowledge-add-sharepoint)
