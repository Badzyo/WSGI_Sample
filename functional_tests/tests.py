from datetime import datetime
import unittest
import json
import requests


class FunctionalTest(unittest.TestCase):
    """
    Еhe expected functionality:
    1.  POST: http://<target_url>/import:
        input JSON data with 3 fields:
        {
            "date": <current date>,
            "time": <current time>,
            "text": <any text>
        }
        Response body must be "OK" if data is valid
        and "FAIL" if data is invalid

    2.  GET: http://<target_url>/last:
        the last imported JSON data is expected
    """

    target_url = 'http://127.0.0.1:8080/'

    def test_requests(self):
        url = '{}import'.format(self.target_url)
        r = requests.post(url, data=json.dumps(self.request_body))
        self.assertEqual(r.content, b'OK')

        r = requests.post(url, data='{"junk": "cc45t3tg3"}')
        self.assertEqual(r.content, b'FAIL')

        url = '{}last'.format(self.target_url)
        r = requests.get(url)
        content = json.loads(r.content.decode('utf-8'))
        self.assertEqual(content, self.request_body)

    @property
    def request_body(self):
        if not hasattr(self,'_request_body'):
            self._request_body = dict()
            self._request_body['date'] = datetime.now().strftime('%d.%m.%Y')
            self._request_body['time'] = datetime.now().strftime('%H:%M:%S')
            self._request_body['text'] = 'test_text'
        return self._request_body


if __name__ == '__main__':
    unittest.main()
