import json
import unittest

import requests

from functions import HelpTestFunctions

unittest.TestLoader.sortTestMethodsUsing = None


class TestRegisterAndLogin(unittest.TestCase, HelpTestFunctions):

    accounts = None

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)
        self.accounts = json.loads(requests.get(
            'http://localhost:5000/getAccounts').text)['accounts']

    def test_add_customer(self) -> None:
        self.assertEqual(self.register(), True)
        self.assertDictEqual(self.get_customer(), {
            'login': 'max',
            'name': 'Max'
        })
        self.assertEqual(self.get_role(), 'customer')
        self.assertEqual(self.login(), True)


class TestAddShop(unittest.TestCase, HelpTestFunctions):

    accounts = None

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)
        self.accounts = json.loads(requests.get(
            'http://localhost:5000/getAccounts').text)['accounts']

    def test_add_shop(self) -> None:
        self.assertEqual(self.add_shop(), True)
        self.assertDictEqual(self.get_shop(), {
            'name': 'XXX-shop',
            'city': 'Moscow',
            'sellers': [],
            'rate': '0'
        })
        self.assertDictEqual(self.get_all_shops()[0], {
            'address': self.accounts[2],
            'name': 'XXX-shop',
            'city': 'Moscow',
            'sellers': [],
        })


class TestCreateBankAccount(unittest.TestCase, HelpTestFunctions):

    accounts = None

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)
        self.accounts = json.loads(requests.get(
            'http://localhost:5000/getAccounts').text)['accounts']

    def test_create_bank_account(self) -> None:
        self.assertEqual(self.create_bank_account(), True)
        self.assertDictEqual(self.get_bank(), {
            'name': 'Golden Fish',
            'bankAddress': self.accounts[3]
        })


class TestAskForUp(unittest.TestCase, HelpTestFunctions):

    accounts = None

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)
        self.accounts = json.loads(requests.get(
            'http://localhost:5000/getAccounts').text)['accounts']
        self.register()
        self.add_shop()

    def test_ask_for_up(self) -> None:
        self.assertEqual(self.ask_for_up(), True)
        self.assertEqual(
            self.get_ask_for_up(),
            self.accounts[2]
        )
        self.assertDictEqual(self.get_all_asks_for_up()[0], {
            'asker': self.accounts[1],
            'shopAddress': self.accounts[2]
        })


class TestUpRole(unittest.TestCase, HelpTestFunctions):

    accounts = None

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)
        self.accounts = json.loads(requests.get(
            'http://localhost:5000/getAccounts').text)['accounts']
        self.register()
        self.add_shop()
        self.ask_for_up()

    def test_up_role(self) -> None:
        self.assertEqual(self.up_role(), True)
        self.assertEqual(self.get_role(), 'seller')
        self.assertEqual(
            self.get_ask_for_up(),
            '0x0000000000000000000000000000000000000000'
        )
        self.assertEqual(self.get_all_asks_for_up(), [])
        self.assertEqual(self.get_shop()['sellers'][0], self.accounts[1])


class TestAskForDown(unittest.TestCase, HelpTestFunctions):

    accounts = None

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)
        self.accounts = json.loads(requests.get(
            'http://localhost:5000/getAccounts').text)['accounts']
        self.register()
        self.add_shop()
        self.ask_for_up()
        self.up_role()

    def test_ask_for_down(self) -> None:
        self.assertEqual(self.ask_for_down(), True)
        self.assertEqual(self.get_ask_for_down(), self.accounts[2])
        self.assertDictEqual(self.get_all_asks_for_down()[0], {
            'asker': self.accounts[1],
            'shopAddress': self.accounts[2]
        })


class TestDownRole(unittest.TestCase, HelpTestFunctions):

    accounts = None

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)
        self.accounts = json.loads(requests.get(
            'http://localhost:5000/getAccounts').text)['accounts']
        self.register()
        self.add_shop()
        self.ask_for_up()
        self.up_role()
        self.ask_for_down()

    def test_down_role(self) -> None:
        self.assertEqual(self.down_role(), True)
        self.assertEqual(self.get_role(), 'customer')
        self.assertEqual(
            self.get_ask_for_down(),
            '0x0000000000000000000000000000000000000000'
        )
        self.assertEqual(self.get_all_asks_for_up(), [])
        self.assertEqual(
            self.get_shop()['sellers'][0],
            '0x0000000000000000000000000000000000000000'
        )


# need write tests for send money feature


if __name__ == '__main__':
    unittest.main()
