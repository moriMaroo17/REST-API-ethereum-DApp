import json
import unittest

import requests


unittest.TestLoader.sortTestMethodsUsing = None


class TestAccountsContractAPI(unittest.TestCase):

    accounts = None

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)
        self.accounts = json.loads(requests.get(
            'http://localhost:5000/getAccounts').text)['accounts']

    def register(self) -> None:

        res = requests.post('http://localhost:5000/register', data={
            'login': 'max',
            'name': 'Max',
            'password': '1234',
            'account': self.accounts[1]
        }).text

        self.assertEqual(json.loads(res)['result'], True)

    def get_customer(self) -> None:

        res = requests.get('http://localhost:5000/getCustomer', data={
            'address': self.accounts[1]
        }).text

        customer = json.loads(res)['result']
        self.assertDictEqual(customer, {'login': 'max', 'name': 'Max'})

    def login(self) -> None:

        res = requests.post('http://localhost:5000/login', data={
            'login': 'max',
            'password': '1234'
        }).text

        self.assertEqual(json.loads(res)['result'], True)

    def get_customer_role(self) -> None:

        res = requests.get('http://localhost:5000/getRole', data={
            'address': self.accounts[1]
        }).text

        self.assertEqual(json.loads(res)['result'], 'customer')

    def test_add_customer(self) -> None:
        self.register()
        self.get_customer()
        self.get_customer_role()
        self.login()

    def add_shop(self) -> None:

        res = requests.post('http://localhost:5000/addShop', data={
            'adminAddress': self.accounts[0],
            'shopAddress': self.accounts[2],
            'name': 'XXX-shop',
            'city': 'Moscow',
            'password': '1234'
        }).text

        self.assertEqual(json.loads(res)['result'], True)

    def get_shop(self) -> None:

        res = requests.get('http://localhost:5000/getShop', data={
            'shopAddress': self.accounts[2]
        }).text

        shop = json.loads(res)['result']

        self.assertDictEqual(shop, {
            'name': 'XXX-shop',
            'city': 'Moscow',
            'sellers': [],
            'rate': '0'
        })

    def get_all_shops(self) -> None:

        res = requests.get('http://localhost:5000/getAllShops').text

        shop_list = json.loads(res)['shops']

        self.assertDictEqual(shop_list[0], {
            'address': self.accounts[2],
            'name': 'XXX-shop',
            'city': 'Moscow',
            'sellers': [],
        })

    def test_add_shop(self) -> None:
        self.add_shop()
        self.get_shop()
        self.get_all_shops()

    def create_bank_account(self) -> None:

        res = requests.post('http://localhost:5000/createBankAccount', data={
            'bankName': 'Golden Fish',
            'bankAddress': self.accounts[3],
            'adminAddress': self.accounts[0],
            'password': '1234'
        }).text

        self.assertEqual(json.loads(res)['result'], True)

    def get_bank(self) -> None:

        res = requests.get('http://localhost:5000/getBank').text

        bank = json.loads(res)['result']

        self.assertDictEqual(bank, {
            'name': 'Golden Fish',
            'bankAddress': self.accounts[3]
        })
    
    def test_create_bank_account(self) -> None:
        self.create_bank_account()
        self.get_bank()

    def ask_for_up(self) -> None:

        res = requests.post('http://localhost:5000/askForUp', data={
            'customerAddress': self.accounts[1],
            'shopAddress': self.accounts[2]
        }).text

        self.assertEqual(json.loads(res)['result'], True)

    def get_ask_for_up(self) -> None:

        res = requests.get('http://localhost:5000/getAskForUp', data={
            'customerAddress': self.accounts[1]
        }).text

        self.assertEqual(json.loads(res)['result'], self.accounts[2])

    def get_all_asks_for_up(self) -> None:

        res = requests.get('http://localhost:5000/getAllAsksForUp').text

        asks = json.loads(res)['asks']

        self.assertDictEqual(asks[0], {
            'asker': self.accounts[1],
            'shopAddress': self.accounts[2]
        })

    def test_ask_for_up(self) -> None:
        self.ask_for_up()
        self.get_ask_for_up()
        self.get_all_asks_for_up()

if __name__ == '__main__':
    unittest.main()
