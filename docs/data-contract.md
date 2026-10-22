# Data contract

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

The Python reference uses SQLite or CSV equivalents, not native SharePoint schema provisioning. See src/app.py for exact reference fields. All cloud identity fields must be resolved by the authenticated service, not accepted from model output. Use ISO 8601 dates and UTC audit timestamps; the reporting period uses the agreed business calendar.
