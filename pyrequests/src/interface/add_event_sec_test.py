import unittest
import requests
import time
import hashlib


class AddEventTest(unittest.TestCase):

    def setUp(self):
        self.base_url = "http://127.0.0.1:8001/api/sec_add_event/"
        # app_key
        self.api_key = "&Guest-Bugmaster"
        # 当前时间
        now_time = time.time()
        self.client_time = str(now_time).split('.')[0]
        # sign
        md5 = hashlib.md5()
        sign_str = self.client_time + self.api_key
        sign_bytes_utf8 = sign_str.encode(encoding="utf-8")
        md5.update(sign_bytes_utf8)
        self.sign_md5 = md5.hexdigest()

        url2 = "http://127.0.0.1:8001/index/"
        self.s = requests.Session()
        page = self.s.get(url2)
        self.csrf_token = page.cookies['csrftoken']

    def test_add_event_sign_null(self):
        payload = {'eid': 1, '': '', 'limit': '', 'address': '',
                   'start_time': '', 'time': '', 'sign': '', 'csrfmiddlewaretoken': self.csrf_token}
        r = self.s.post(self.base_url, data=payload)
        result = r.json()
        self.assertEqual(result['status'], 10011)
        self.assertEqual(result['message'], 'user sign null')

    def test_add_event_time_out(self):
        now_time = str(int(self.client_time) - 61)
        payload = {'eid': 1, '': '', 'limit': '', 'address': '', 'start_time': '',
                   'time': now_time, 'sign': 'abc', 'csrfmiddlewaretoken': self.csrf_token}
        r = self.s.post(self.base_url, data=payload)
        result = r.json()
        self.assertEqual(result['status'], 10012)
        self.assertEqual(result['message'], 'user sign timeout')

    def test_add_event_sign_error(self):
        payload = {'eid': 1, '': '', 'limit': '', 'address': '', 'start_time': '',
                   'time': self.client_time, 'sign': 'abc', 'csrfmiddlewaretoken': self.csrf_token}
        r = self.s.post(self.base_url, data=payload)
        result = r.json()
        self.assertEqual(result['status'], 10013)
        self.assertEqual(result['message'], 'user sign error')

    def test_add_event_success(self):
        payload = {'eid': 11, 'name': '一加 4 手机发布会', 'limit': 2000, 'address': "深圳宝体", 'start_time': '2017-05-10 12:00:00',
                   'time': self.client_time, 'sign': self.sign_md5, 'csrfmiddlewaretoken': self.csrf_token}
        r = self.s.post(self.base_url, data=payload)
        result = r.json()
        self.assertEqual(result['status'], 200)
        self.assertEqual(result['message'], 'add event success')
