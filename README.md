# Enterprise AI Employee Support Agent

Independent portfolio project by Richard Parr • Future of Work Training Institute

Employees repeatedly search HR and IT policies, while support teams handle duplicate requests.

**Current status:** tested Python reference application with synthetic data. Microsoft cloud deployment is pending. This repository does not establish business adoption or tenant deployment.

## Run the working reference

Python 3.11+; no paid service, API key or third-party Python package required for runtime or tests.

```bash
python3 -m unittest discover -s tests -v
python3 src/app.py ask "vacation leave policy"
python3 src/app.py ask "executive salary compensation"
python3 src/app.py ticket --key demo-1 --employee synthetic-user --category IT --description "VPN connection fails" --confirm
python3 src/app.py tickets
```

Run from this repository root. SQLite state is local and excluded from Git. Use a fresh `--db` path for repeat demonstrations. The CLI will return a nonzero exit code for invalid operations.

## Microsoft target

Copilot Studio, Teams, SharePoint, Power Automate

See [the PRD](docs/PRD.md), [architecture](docs/architecture.md), [deployment guide](docs/deployment-guide.md), [data contract](docs/data-contract.md), [test results](tests/results.txt), [recorded CLI run](demo/output.txt), and [evidence status](docs/evidence-status.md).

## Included behavior and limits

1. Ground policy responses in permission-filtered SharePoint knowledge with visible citations.
2. Provide IT, HR, software access and escalation paths; abstain when sources are absent.
3. Collect category and description, show a confirmation card, then create one ticket per request.
4. Return a ticket reference; restrict ticket-status access to the requester and authorized support staff.

- Keyword retrieval is a deterministic local reference, not Copilot Studio generative answers.
- CLI group names simulate permission contexts. They do not authenticate the caller.
- The reference lists ticket IDs and categories locally; real requester-specific status lookup belongs in the authenticated cloud flow.

Power Automate artifacts in `flows/` are explicit build specifications, not tenant-generated solution exports. Production permission and connector tests remain outstanding. The reference's CLI approval flags simulate a reviewer; cloud deployment must verify reviewer identity server-side.

## Validation and business value

Eight automated reference tests cover positive and failure paths. Tests are regression evidence for the included synthetic cases, not an enterprise performance benchmark. See [measurement plan](docs/measurement-plan.md) before making any ROI claim.

## Sources

Implementation references checked October 22, 2026; confirm tenant-specific licensing, connector availability and capacity before deployment.

- [SharePoint knowledge](https://learn.microsoft.com/microsoft-copilot-studio/knowledge-add-sharepoint)

MIT licensed. All sample records are synthetic.
