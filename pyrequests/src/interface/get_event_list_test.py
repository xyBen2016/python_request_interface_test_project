import unittest
import requests


class GetEventListTest(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://127.0.0.1:8001/api/sec_get_event_list/"
        self.auth_user = ('admin', 'admin123456')

    def test_get_event_list_auth_null(self):
        r = requests.get(self.base_url, params={'eid': ''})
        result = r.json()
        self.assertEqual(result['status'], 10011)
        self.assertEqual(result['message'], 'user auth null')

    def test_get_event_list_auth_error(self):
        r = requests.get(self.base_url, auth=(
            'abc', '123'), params={'eid': ''})
        result = r.json()
        self.assertEqual(result['status'], 10012)
        self.assertEqual(result['message'], 'user auth fail')

    def test_get_event_list_eid_null(self):
        r = requests.get(self.base_url, auth=self.auth_user,
                         params={'eid': ''})
        result = r.json()
        self.assertEqual(result['status'], 10021)
        self.assertEqual(result['message'], 'parameter error')

    def test_get_event_list_eid_success(self):
        r = requests.get(self.base_url, auth=self.auth_user,
                         params={'eid': 1})
        result = r.json()
        self.assertEqual(result['status'], 200)
        self.assertEqual(result['message'], 'success')
        self.assertEqual(result['data']['name'], u'红米 Pro 发布会')
        self.assertEqual(result['data']['address'], u'北京会展中心')
