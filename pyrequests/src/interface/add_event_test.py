import unittest
import requests
import os
import sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
from db_fixture import test_data


class AddEventTest(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://127.0.0.1:8001/api/add_event/"
        url2 = "http://127.0.0.1:8001/index/"
        self.s = requests.Session()
        page = self.s.get(url2)
        self.csrf_token = page.cookies['csrftoken']

    def tearDown(self):
        print(self.result)

    def test_add_event_all_null(self):
        payload = {'eid': '', 'name': '', 'limit': '',
                   'address': '', 'start_time': '', 'csrfmiddlewaretoken': self.csrf_token}
        r = self.s.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10021)
        self.assertEqual(self.result['message'], 'parameter error')

    def test_add_event_eid_exist(self):
        payload = {'eid': 1, 'name': '一加 4 发布会', 'limit': 2000,
                   'address': "深圳宝体", 'start_time': '2017', 'csrfmiddlewaretoken': self.csrf_token}
        r = self.s.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10022)
        self.assertEqual(self.result['message'], 'event id already exists')

    def test_add_event_name_exist(self):
        payload = {'eid': 13, 'name': '红米 Pro 发布会', 'limit': 2000,
                   'address': "北京水立方", 'start_time': '2017', 'csrfmiddlewaretoken': self.csrf_token}
        r = self.s.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10023)
        self.assertEqual(self.result['message'], 'event name already exists')

    def test_add_event_data_type_error(self):
        payload = {'eid': 12, 'name': '一加 5 手机发布会', 'limit': 1000,
                   'address': "北京土立方", 'start_time': '2018', 'csrfmiddlewaretoken': self.csrf_token}
        r = self.s.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10024)
        self.assertIn('start_time format error.', self.result['message'])

    def test_add_event_success(self):
        payload = {'eid': 14, 'name': '一加 6 手机发布会', 'limit': 2500,
                   'address': "北京风立方", 'start_time': '2018-01-10 12:00:00', 'csrfmiddlewaretoken': self.csrf_token}
        r = self.s.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 200)
        self.assertEqual(self.result['message'], 'add event success')


if __name__ == '__main__':
    test_data.init_data()  # 初始化接口测试数据
    unittest.main()
