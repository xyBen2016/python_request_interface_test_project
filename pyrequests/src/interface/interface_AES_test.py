from Crypto.Cipher import AES
import base64
import requests
import unittest
import json


class AESTest(unittest.TestCase):
    def setUp(self):
        BS = 16
        self.pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
        self.base_url = "http://127.0.0.1:8001/api/sec_get_guest_list/"
        self.app_key = 'W7v4D60fds2Cmk2U'

        url2 = "http://127.0.0.1:8001/index/"
        self.s = requests.Session()
        page = self.s.get(url2)
        self.csrf_token = page.cookies['csrftoken']

    def encryptBase64(self, src):
        return base64.urlsafe_b64encode(src)

    def encryptAES(self, src, key):
        iv = b"1172311105789011"
        cryptor = AES.new(key, AES.MODE_CBC, iv)
        ciphertext = cryptor.encrypt(self.pad(src))
        return self.encryptBase64(ciphertext)

    def test_aes_interface(self):
        payload = {'eid': '1', 'phone': '13511001100'}
        # 加密
        encoded = self.encryptAES(json.dumps(payload), self.app_key).decode()
        r = self.s.post(self.base_url, data={"data": encoded,
                                             'csrfmiddlewaretoken': self.csrf_token})
        result = r.json()
        self.assertEqual(result['status'], 200)
        self.assertEqual(result['message'], "success")

    def test_get_guest_list_eid_null(self):
        payload = {'eid': '', 'phone': ''}
        encoded = self.encryptAES(json.dumps(payload), self.app_key).decode()
        r = self.s.post(self.base_url, data={"data": encoded,
                                             'csrfmiddlewaretoken': self.csrf_token})
        result = r.json()
        self.assertEqual(result['status'], 10021)
        self.assertEqual(result['message'], 'eid cannot be empty')

    def test_get_event_list_eid_error(self):
        payload = {'eid': '901', 'phone': ''}
        encoded = self.encryptAES(json.dumps(payload), self.app_key).decode()
        r = self.s.post(self.base_url, data={"data": encoded,
                                             'csrfmiddlewaretoken': self.csrf_token})
        result = r.json()
        self.assertEqual(result['status'], 10022)
        self.assertEqual(result['message'], 'query result is empty')

    def test_get_event_list_eid_success(self):
        payload = {'eid': '1', 'phone': ''}
        encoded = self.encryptAES(json.dumps(payload), self.app_key).decode()
        r = self.s.post(self.base_url, data={"data": encoded,
                                             'csrfmiddlewaretoken': self.csrf_token})
        result = r.json()
        self.assertEqual(result['status'], 200)
        self.assertEqual(result['message'], 'success')
        self.assertEqual(result['data'][0]['realname'], 'alen')
        self.assertEqual(result['data'][0]['phone'], '13511001100')

    def test_get_event_list_eid_phone_null(self):
        payload = {'eid': 2, 'phone': '10000000000'}
        encoded = self.encryptAES(json.dumps(payload), self.app_key).decode()
        r = self.s.post(self.base_url, data={"data": encoded,
                                             'csrfmiddlewaretoken': self.csrf_token})
        result = r.json()
        self.assertEqual(result['status'], 10022)
        self.assertEqual(result['message'], 'query result is empty')

    def test_get_event_list_eid_phone_success(self):
        payload = {'eid': 1, 'phone': '13511001100'}
        encoded = self.encryptAES(json.dumps(payload), self.app_key).decode()
        r = self.s.post(self.base_url, data={"data": encoded,
                                             'csrfmiddlewaretoken': self.csrf_token})
        result = r.json()
        self.assertEqual(result['status'], 200)
        self.assertEqual(result['message'], 'success')
        self.assertEqual(result['data']['realname'], 'alen')
        self.assertEqual(result['data']['phone'], '13511001100')
