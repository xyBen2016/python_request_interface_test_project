import unittest
import requests


class UserTest(unittest.TestCase):

    def setUp(self):
        self.base_url = 'http://127.0.0.1:8000/users'

    def test_user1(self):
        r = requests.get(self.base_url + '/1/', auth=('admin', 'admin123456'))
        result = r.json()
        self.assertEqual(result['username'], 'admin')
        self.assertEqual(result['email'], 'admin@mail.com')

    def test_user2(self):
        r = requests.get(self.base_url + '/2/', auth=('admin', 'admin123456'))
        result = r.json()
        self.assertEqual(result['username'], 'tom')
        self.assertEqual(result['email'], 'tom@mail.com')

    def test_user3(self):
        r = requests.get(self.base_url + '/3/', auth=('admin', 'admin123456'))
        result = r.json()
        self.assertEqual(result['username'], 'jack')
        self.assertEqual(result['email'], 'jack@mail.com')


class GroupsTest(unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://127.0.0.1:8000/groups'

    def test_groups1(self):
        r = requests.get(self.base_url + '/1/', auth=('admin', 'admin123456'))
        result = r.json()
        self.assertEqual(result['name'], 'test')

    def test_user2(self):
        r = requests.get(self.base_url + '/2/', auth=('admin', 'admin123456'))
        result = r.json()
        self.assertEqual(result['name'], 'developer')


if __name__ == '__main__':
    unittest.main()
