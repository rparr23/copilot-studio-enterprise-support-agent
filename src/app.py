"""Offline support reference. Groups are trusted CLI test inputs, NOT authentication."""
import argparse
import json
import re
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def answer(question, groups, knowledge=None):
    docs = knowledge if knowledge is not None else json.loads((ROOT / 'sample-data/knowledge.json').read_text())
    tokens = set(re.findall(r'[a-z0-9]+', question.lower()))
    ranked = []
    for doc in docs:
        if not set(doc['groups']).intersection(groups):
            continue
        score = len(tokens.intersection(doc['keywords']))
        if score >= 2:
            ranked.append((score, doc))
    if not ranked:
        return {'status': 'escalate', 'answer': 'No authorized source found. Please create a support request.', 'sources': []}
    doc = max(ranked, key=lambda pair: pair[0])[1]
    return {'status': 'grounded', 'answer': doc['text'], 'sources': [doc['id']]}


def connect(path):
    db = sqlite3.connect(path)
    db.execute('CREATE TABLE IF NOT EXISTS tickets (id INTEGER PRIMARY KEY, request_key TEXT UNIQUE NOT NULL, employee TEXT NOT NULL, category TEXT NOT NULL, description TEXT NOT NULL, created TEXT DEFAULT CURRENT_TIMESTAMP)')
    return db


def create_ticket(db, request_key, employee, category, description, confirmed=False):
    if not confirmed:
        raise ValueError('Explicit confirmation is required')
    if not all(isinstance(v, str) and v.strip() for v in [request_key, employee, category, description]):
        raise ValueError('All ticket fields are required')
    if category not in {'IT', 'HR', 'Access', 'Other'} or len(description) > 2000:
        raise ValueError('Invalid category or description too long')
    with db:
        old = db.execute('SELECT id, employee, category, description FROM tickets WHERE request_key=?', (request_key,)).fetchone()
        if old:
            if old[1:] != (employee, category, description):
                raise ValueError('Idempotency key already used for different request')
            return {'ticket_id': f'SUP-{old[0]:06}', 'duplicate': True}
        cur = db.execute('INSERT INTO tickets(request_key,employee,category,description) VALUES (?,?,?,?)', (request_key, employee, category, description))
        return {'ticket_id': f'SUP-{cur.lastrowid:06}', 'duplicate': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--db', default='state.db')
    sub = parser.add_subparsers(dest='command', required=True)
    ask = sub.add_parser('ask')
    ask.add_argument('question')
    ask.add_argument('--groups', nargs='+', default=['employees'])
    ticket = sub.add_parser('ticket')
    ticket.add_argument('--key', required=True)
    ticket.add_argument('--employee', required=True)
    ticket.add_argument('--category', choices=['IT', 'HR', 'Access', 'Other'], required=True)
    ticket.add_argument('--description', required=True)
    ticket.add_argument('--confirm', action='store_true')
    sub.add_parser('tickets')
    args = parser.parse_args()
    try:
        if args.command == 'ask':
            result = answer(args.question, args.groups)
        else:
            with connect(args.db) as db:
                if args.command == 'ticket':
                    result = create_ticket(db, args.key, args.employee, args.category, args.description, args.confirm)
                else:
                    result = [{'ticket_id': f'SUP-{r[0]:06}', 'category': r[1], 'created': r[2]} for r in db.execute('SELECT id,category,created FROM tickets')]
        print(json.dumps(result, indent=2))
    except (ValueError, sqlite3.Error) as exc:
        parser.exit(2, f'Operation failed: {exc}\n')


if __name__ == '__main__':
    main()
