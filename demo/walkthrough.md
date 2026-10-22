# Demonstration script

## Reproducible local walkthrough

```bash
python3 src/app.py ask "vacation leave policy"
python3 src/app.py ask "executive salary compensation"
python3 src/app.py ticket --key demo-1 --employee synthetic-user --category IT --description "VPN connection fails" --confirm
python3 src/app.py tickets
```

Use a fresh state database when recording. SQLite state is local. `demo/output.txt` contains actual CLI output from this build session, not Microsoft UI evidence.

## Planned 2-4 minute Microsoft recording

- 0:00-0:30: State the business problem, roles and synthetic-data boundary.
- 0:30-1:20: Submit the successful sample and show its source evidence.
- 1:20-2:10: Show review/confirmation and final system record.
- 2:10-2:50: Demonstrate a duplicate, missing field or unauthorized source.
- 2:50-3:30: Show flow history, architecture and measured results with limitations.

No video has been recorded; add the real link only after tenant execution.
