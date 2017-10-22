import json
import unittest

import ultidate.ultidate as ult


class UltimateTestCase(unittest.TestCase):
    def setUp(self):
        # self.db_fd, ultidate.app.config['DATABASE'] = tempfile.mkstemp()
        ult.app.testing = True
        self.app = ult.app.test_client()
        # with ultidate.app.app_context():
        #    ultidate.init_db()

    def tearDown(self):
        self.app.delete('/tournaments')
        pass

    # os.close(self.db_fd)
    # os.unlink(ultidate.app.config['DATABASE'])

    def test_no_tournaments(self):
        rv = self.app.get('/tournaments')
        self.assertEqual(b'{\n  "tournaments": []\n}\n', rv.get_data())
        self.assertEqual('application/json', rv.mimetype)
        self.assertEqual('200 OK', rv.status)

    def test_add_tournament(self):
        # Add
        rv = self.app.post('/tournaments', data=json.dumps(dict(name='Poolimate', description='A tournament')),
                           content_type='application/json')
        self.assertEqual('200 OK', rv.status)

        # List
        rv = self.app.get('/tournaments')
        self.assertEqual(
            b'{\n  "tournaments": [\n    {\n      "description": "A tournament", \n      "name": "Poolimate"\n    }\n  ]\n}\n',
            rv.get_data())
        self.assertEqual('application/json', rv.mimetype)
        self.assertEqual('200 OK', rv.status)

        # Get
        rv = self.app.get('/tournaments/Poolimate')
        self.assertEqual(b'{\n  "description": "A tournament", \n  "name": "Poolimate"\n}\n', rv.get_data())
        self.assertEqual('application/json', rv.mimetype)
        self.assertEqual('200 OK', rv.status)

        if __name__ == '__main__':
            unittest.main()
