import json
import unittest

import requests


class TestAccountsContractAPI(unittest.TestCase):

    accounts = None

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)
        self.accounts = json.loads(requests.get(
            'http://localhost:5000/getAccounts').text)['accounts']

    def test_register(self) -> None:

        res = requests.post('http://localhost:5000/register', data={
            'login': 'max',
            'name': 'Max',
            'password': '1234',
            'account': self.accounts[1]
        }).text

        self.assertEqual(json.loads(res)['result'], True)

    def test_get_customer(self) -> None:

        self.test_register()

        res = requests.get('http://localhost:5000/getCustomer', data={
            'address': self.accounts[1]
        }).text

        customer = json.loads(res)['result']
        self.assertDictEqual(customer, {'login': 'max', 'name': 'Max'})

    def test_login(self) -> None:

        self.test_register()

        res = requests.post('http://localhost:5000/login', data={
            'login': 'max',
            'password': '1234'
        }).text

        self.assertEqual(json.loads(res)['result'], True)

    def test_get_role(self) -> None:

        self.test_register()

        res = requests.get('http://localhost:5000/getRole', data={
            'address': self.accounts[1]
        }).text

        self.assertEqual(json.loads(res)['result'], 'customer')

    def test_add_shop(self) -> None:

        res = requests.post('http://localhost:5000/addShop', data={
            'adminAddress': self.accounts[0],
            'shopAddress': self.accounts[2],
            'name': 'XXX-shop',
            'city': 'Moscow',
            'password': '1234'
        }).text

        self.assertEqual(json.loads(res)['result'], True)

    def test_get_shop(self) -> None:

        self.test_add_shop()

        res = requests.get('http://localhost:5000/getShop', data={
            'shopAddress': self.accounts[2]
        }).text

        shop = json.loads(res)['result']

        self.assertDictEqual(
            shop, {
                'name': 'XXX-shop',
                'city': 'Moscow',
                'sellers': [],
                'rate': '0'
        })

    def test_create_bank_account(self) -> None:

        res = requests.post('http://localhost:5000/createBankAccount', data={
            'bankName': 'Golden Fish',
            'bankAddress': self.accounts[3],
            'adminAddress': self.accounts[0],
            'password': '1234'
        }).text

        self.assertEqual(json.loads(res)['result'], True)


if __name__ == '__main__':
    unittest.main()
