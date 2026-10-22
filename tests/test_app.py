import sqlite3
import unittest
from src.app import answer, connect, create_ticket


class SupportTests(unittest.TestCase):
    def setUp(self):
        self.db = connect(':memory:')

    def tearDown(self):
        self.db.close()

    def test_authorized_grounded_answer(self):
        result = answer('vacation leave policy', ['employees'])
        self.assertEqual(result['sources'], ['HR-001'])
        self.assertIn('5 business days', result['answer'])

    def test_restricted_document_hidden(self):
        result = answer('executive salary compensation', ['employees'])
        self.assertEqual(result['status'], 'escalate')
        self.assertNotIn('HR-PRIVATE', str(result))

    def test_unauthenticated_empty_groups(self):
        self.assertEqual(answer('vacation leave', [])['sources'], [])

    def test_unknown_policy_not_invented(self):
        self.assertEqual(answer('mars relocation reimbursement', ['employees'])['status'], 'escalate')

    def test_ticket_confirmation(self):
        with self.assertRaises(ValueError):
            create_ticket(self.db, 'k', 'test', 'IT', 'VPN fails')
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM tickets').fetchone()[0], 0)

    def test_ticket_retry_and_payload_conflict(self):
        args = (self.db, 'k', 'synthetic-employee', 'IT', 'VPN fails', True)
        self.assertEqual(create_ticket(*args)['ticket_id'], 'SUP-000001')
        self.assertTrue(create_ticket(*args)['duplicate'])
        with self.assertRaises(ValueError):
            create_ticket(self.db, 'k', 'other', 'IT', 'VPN fails', True)

    def test_invalid_inputs(self):
        for category, text in [('Invalid', 'problem'), ('IT', ''), ('IT', 'x'*2001)]:
            with self.assertRaises(ValueError):
                create_ticket(self.db, 'key', 'employee', category, text, True)

    def test_storage_failure_surfaces(self):
        self.db.execute('DROP TABLE tickets')
        with self.assertRaises(sqlite3.Error):
            create_ticket(self.db, 'key', 'employee', 'IT', 'test', True)


if __name__ == '__main__':
    unittest.main()
