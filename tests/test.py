import json
import unittest

import requests

from functions import HelpTestFunctions

unittest.TestLoader.sortTestMethodsUsing = None


class TestRegisterAndLogin(unittest.TestCase, HelpTestFunctions):

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


class TestAskBank(unittest.TestCase, HelpTestFunctions):
    
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)
        self.accounts = json.loads(requests.get(
            'http://localhost:5000/getAccounts').text)['accounts']
        self.add_shop()
        self.create_bank_account()

    def test_ask_bank(self) -> None:
        self.assertEqual(self.ask_bank(), True)
        self.assertDictEqual(self.get_all_asks_bank()[0], {
            'shop': self.accounts[2],
            'value': '1'
        })


class TestSendMoney(unittest.TestCase, HelpTestFunctions):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)
        self.accounts = json.loads(requests.get(
            'http://localhost:5000/getAccounts').text)['accounts']
        self.add_shop()
        self.create_bank_account()
        self.ask_bank()

    def test_send_money(self) -> None:
        previous = self.get_balance()
        self.assertEqual(self.send_money(), True)
        current = self.get_balance()
        diffrence = int(current[0]) - int(previous[0])
        self.assertEqual(diffrence, 1000000000000000000)
        self.assertDictEqual(
            self.get_debt_list()[0],
            {'shop': self.accounts[2], 'debt': '1000000000000000000'}
        )


class TestAddAdmin(unittest.TestCase, HelpTestFunctions):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)
        self.accounts = json.loads(requests.get(
            'http://localhost:5000/getAccounts').text)['accounts']
        self.register()

    def test_add_admin(self) -> None:
        self.assertEqual(self.add_admin(), True)
        self.assertDictEqual(
            self.get_all_admins()[0], {
                'address': self.accounts[1],
                'name': 'Max',
                'login': 'max'
            })
        self.assertEqual(self.get_role(), 'admin')


class TestDeleteShop(unittest.TestCase, HelpTestFunctions):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)
        self.accounts = json.loads(requests.get(
            'http://localhost:5000/getAccounts').text)['accounts']
        self.register()
        self.add_shop()
        self.ask_for_up()
        self.up_role()

    def test_delete_shop(self) -> None:
        self.assertEqual(self.delete_shop(), True)
        self.assertEqual(self.get_role(), 'customer')
        self.assertListEqual(self.get_all_shops(), [])


class TestCommentShop(unittest.TestCase, HelpTestFunctions):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)
        self.accounts = json.loads(requests.get(
            'http://localhost:5000/getAccounts').text)['accounts']
        self.register()
        self.add_shop()

    def test_comment_shop(self) -> None:
        self.assertEqual(self.comment_shop(), True)
        self.assertDictEqual(self.get_comment(), {
            'owner': 'Max',
            'message': 'pretty good shop',
            'rate': '10',
            'likes': '0',
            'dislikes': '0'
        })


class TestReplyOnComment(unittest.TestCase, HelpTestFunctions):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)
        self.accounts = json.loads(requests.get(
            'http://localhost:5000/getAccounts').text)['accounts']
        self.register()
        self.add_shop()
        self._register_customer_for_reply_on_comment()
        self.comment_shop()

    def test_reply_on_comment(self) -> None:
        self.assertEqual(self.reply_on_comment(), True)
        self.assertDictEqual(self.get_reply(), {
            'owner': 'Ben',
            'commentId': '0',
            'message': 'actually agree',
            'rate': '10',
            'likes': '0',
            'dislikes': '0'
        })


class TestReplyOnCommentByShop(unittest.TestCase, HelpTestFunctions):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)
        self.accounts = json.loads(requests.get(
            'http://localhost:5000/getAccounts').text)['accounts']
        self.register()
        self.add_shop()
        self._register_customer_for_reply_on_comment()
        self._up_seller_for_reply_on_comment()
        self.comment_shop()

    def test_reply_on_comment_by_shop(self) -> None:
        self.assertEqual(self.reply_on_comment_by_shop(), True)
        self.assertDictEqual(self.get_reply(), {
            'owner': 'Ben',
            'commentId': '0',
            'message': 'thank you for review, we were glad to help you',
            'rate': '0',
            'likes': '0',
            'dislikes': '0'
        })

class TestLikeComment(unittest.TestCase, HelpTestFunctions):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)
        self.accounts = json.loads(requests.get(
            'http://localhost:5000/getAccounts').text)['accounts']
        self.register()
        self.add_shop()
        self._register_customer_for_reply_on_comment()
        self.comment_shop()

    def test_like_comment(self) -> None:
        self.assertEqual(self.like_comment(), True)
        self.assertEqual(self.get_comment()['likes'], '1')


class TestDislikeComment(unittest.TestCase, HelpTestFunctions):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)
        self.accounts = json.loads(requests.get(
            'http://localhost:5000/getAccounts').text)['accounts']
        self.register()
        self.add_shop()
        self._register_customer_for_reply_on_comment()
        self.comment_shop()

    def test_dislike_comment(self) -> None:
        self.assertEqual(self.dislike_comment(), True)
        self.assertEqual(self.get_comment()['dislikes'], '1')


class TestLikeReply(unittest.TestCase, HelpTestFunctions):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)
        self.accounts = json.loads(requests.get(
            'http://localhost:5000/getAccounts').text)['accounts']
        self.register()
        self.add_shop()
        self._register_customer_for_reply_on_comment()
        self.comment_shop()
        self.reply_on_comment()

    def test_like_comment(self) -> None:
        self.assertEqual(self.like_reply(), True)
        self.assertEqual(self.get_reply()['likes'], '1')


class TestDislikeReply(unittest.TestCase, HelpTestFunctions):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)
        self.accounts = json.loads(requests.get(
            'http://localhost:5000/getAccounts').text)['accounts']
        self.register()
        self.add_shop()
        self._register_customer_for_reply_on_comment()
        self.comment_shop()
        self.reply_on_comment()

    def test_dislike_comment(self) -> None:
        self.assertEqual(self.dislike_reply(), True)
        self.assertEqual(self.get_reply()['dislikes'], '1')


class TestUpRate(unittest.TestCase, HelpTestFunctions):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)
        self.accounts = json.loads(requests.get(
            'http://localhost:5000/getAccounts').text)['accounts']
        self.register()
        self.add_shop()
        self._register_customer_for_reply_on_comment()
        self.comment_shop()
        for i in range(0, 10):
            self.like_comment()

    def test_up_rate(self) -> None:
        self.assertDictEqual(self.get_shop(), {
            'name': 'XXX-shop',
            'city': 'Moscow',
            'sellers': [],
            'rate': 10
        })
        self.assertDictEqual(self.get_comment(), {
            'owner': 'Max',
            'message': 'pretty good shop',
            'rate': '10',
            'likes': '10',
            'dislikes': '0'
        })

if __name__ == '__main__':
    unittest.main()
