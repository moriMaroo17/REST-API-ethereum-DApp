import json

import requests


class HelpTestFunctions():

    accounts = None

    # starts functions for Accounts.sol

    # test add customer

    def register(self) -> bool:

        res = requests.post('http://localhost:5000/register', data={
            'login': 'max',
            'name': 'Max',
            'password': '1234',
            'account': self.accounts[1]
        }).text

        return json.loads(res)['result']

    def get_customer(self) -> dict:

        res = requests.get('http://localhost:5000/getCustomer', data={
            'address': self.accounts[1]
        }).text

        return json.loads(res)['result']

    def login(self) -> bool:

        res = requests.post('http://localhost:5000/login', data={
            'login': 'max',
            'password': '1234'
        }).text

        return json.loads(res)['result']

    def get_role(self) -> str:

        res = requests.get('http://localhost:5000/getRole', data={
            'address': self.accounts[1]
        }).text

        return json.loads(res)['result']

    # test add shop

    def add_shop(self) -> bool:

        res = requests.post('http://localhost:5000/addShop', data={
            'adminAddress': self.accounts[0],
            'shopAddress': self.accounts[2],
            'name': 'XXX-shop',
            'city': 'Moscow',
            'password': '1234'
        }).text

        return json.loads(res)['result']

    def get_shop(self) -> dict:

        res = requests.get('http://localhost:5000/getShop', data={
            'shopAddress': self.accounts[2]
        }).text

        return json.loads(res)['result']

    def get_all_shops(self) -> list:

        res = requests.get('http://localhost:5000/getAllShops').text

        return json.loads(res)['shops']

    # test create bank account

    def create_bank_account(self) -> bool:

        res = requests.post('http://localhost:5000/createBankAccount', data={
            'bankName': 'Golden Fish',
            'bankAddress': self.accounts[3],
            'adminAddress': self.accounts[0],
            'password': '1234'
        }).text

        return json.loads(res)['result']

    def get_bank(self) -> dict:

        res = requests.get('http://localhost:5000/getBank').text

        return json.loads(res)['result']

    # test ask for up role

    def ask_for_up(self) -> bool:

        res = requests.post('http://localhost:5000/askForUp', data={
            'customerAddress': self.accounts[1],
            'shopAddress': self.accounts[2]
        }).text

        return json.loads(res)['result']

    def get_ask_for_up(self) -> str:

        res = requests.get('http://localhost:5000/getAskForUp', data={
            'customerAddress': self.accounts[1]
        }).text

        return json.loads(res)['result']

    def get_all_asks_for_up(self) -> list:

        res = requests.get('http://localhost:5000/getAllAsksForUp').text

        return json.loads(res)['asks']

    # test up role by ask

    def up_role(self) -> bool:

        res = requests.post('http://localhost:5000/upRole', data={
            'customerAddress': self.accounts[1],
            'adminAddress': self.accounts[0]
        }).text

        return json.loads(res)['result']

    # test ask for down role

    def ask_for_down(self) -> bool:
        res = requests.post('http://localhost:5000/askForDown', data={
            'sellerAddress': self.accounts[1],
        }).text

        return json.loads(res)['result']

    def get_ask_for_down(self) -> str:

        res = requests.get('http://localhost:5000/getAskForDown', data={
            'sellerAddress': self.accounts[1]
        }).text

        return json.loads(res)['result']

    def get_all_asks_for_down(self) -> list:

        res = requests.get('http://localhost:5000/getAllAsksForDown').text

        return json.loads(res)['asks']

    # test down role by ask

    def down_role(self) -> bool:

        res = requests.post('http://localhost:5000/downRole', data={
            'sellerAddress': self.accounts[1],
            'adminAddress': self.accounts[0]
        }).text

        return json.loads(res)['result']


    # test send money from bank

    def ask_bank(self) -> bool:

        res = requests.post('http://localhost:5000/askBank', data={
            'shopAddress': self.accounts[2],
            'value': 1
        }).text

        return json.loads(res)['result']

    def get_all_asks_bank(self) -> list:

        res = requests.get('http://localhost:5000/getAllAsksBank').text

        return json.loads(res)['asks']
    
    def send_money(self) -> bool:

        res = requests.post('http://localhost:5000/sendMoney', data={
            'shopAddress': self.accounts[2],
            'bankAddress': self.accounts[3],
            'value': 1
        }).text

        return json.loads(res)['result']

    def get_balance(self) -> tuple:

        shop_balance = requests.get('http://localhost:5000/getBalance', data={
            'address': self.accounts[2]
        }).text

        bank_balance = requests.get('http://localhost:5000/getBalance', data={
            'address': self.accounts[3]
        }).text

        return (
            json.loads(shop_balance)['balance'],
            json.loads(bank_balance)['balance']
        )

    def get_debt_list(self) -> list:

        res = requests.get('http://localhost:5000/getDebtList').text

        return json.loads(res)['debts']

    # test adding admin

    def add_admin(self) -> bool:

        res = requests.post('http://localhost:5000/addAdmin', data={
            'newAdminAddress': self.accounts[1],
            'adminAddress': self.accounts[0]
        }).text

        return json.loads(res)['result']

    def get_all_admins(self) -> list:

        res = requests.get('http://localhost:5000/getAllAdmins').text

        return json.loads(res)['admins']

    # test deleting shop

    def delete_shop(self) -> bool:

        res = requests.post('http://localhost:5000/deleteShop', data={
            'shopAddress': self.accounts[2],
            'adminAddress': self.accounts[0]
        }).text

        return json.loads(res)['result']

    # end functions for Accounts.sol

    # start functions for ReviewBook.sol

    def comment_shop(self) -> bool:

        res = requests.post('http://localhost:5000/commentShop', data={
            'customerAddress': self.accounts[1],
            'shopAddress': self.accounts[2],
            'message': 'pretty good shop',
            'rate': 10
        }).text

        return json.loads(res)['result']

    def get_comment(self) -> dict:

        res = requests.get('http://localhost:5000/getComment', data={
            'shopAddress': self.accounts[2],
            'index': 0
        }).text

        return json.loads(res)

    def _up_seller_for_reply_on_comment(self) -> bool:

        res1 = requests.post('http://localhost:5000/askForUp', data={
            'customerAddress': self.accounts[9],
            'shopAddress': self.accounts[2]
        }).text

        res2 = requests.post('http://localhost:5000/upRole', data={
            'customerAddress': self.accounts[9],
            'adminAddress': self.accounts[0]
        }).text

        return json.loads(res1)['result'] and json.loads(res2)['result']

    def _register_customer_for_reply_on_comment(self) -> bool:

        res = requests.post('http://localhost:5000/register', data={
            'login': 'ben',
            'name': 'Ben',
            'password': '1234',
            'account': self.accounts[9]
        }).text

        return json.loads(res)['result']

    def reply_on_comment(self) -> bool:

        res = requests.post('http://localhost:5000/replyOnComment', data={
            'customerAddress': self.accounts[9],
            'shopAddress': self.accounts[2],
            'message': 'actually agree',
            'rate': 10,
            'commentId': 0
        }).text

        return json.loads(res)['result']

    def reply_on_comment_by_shop(self) -> bool:

        res = requests.post(
            'http://localhost:5000/replyOnCommentByShop', data={
                'sellerAddress': self.accounts[9],
                'shopAddress': self.accounts[2],
                'message': 'thank you for review, we were glad to help you',
                'commentId': 0
        }).text

        return json.loads(res)['result']

    def get_reply(self) -> dict:

        res = requests.get('http://localhost:5000/getReply', data={
            'shopAddress': self.accounts[2],
            'index': 0
        }).text

        return json.loads(res)

    def like_comment(self) -> bool:

        res = requests.post('http://localhost:5000/likeComment', data={
            'customerAddress': self.accounts[9],
            'shopAddress': self.accounts[2],
            'commentId': 0
        }).text

        return json.loads(res)['result']

    def dislike_comment(self) -> bool:

        res = requests.post('http://localhost:5000/dislikeComment', data={
            'customerAddress': self.accounts[9],
            'shopAddress': self.accounts[2],
            'commentId': 0
        }).text

        return json.loads(res)['result']

    def like_reply(self) -> bool:

        res = requests.post('http://localhost:5000/likeReply', data={
            'customerAddress': self.accounts[1],
            'shopAddress': self.accounts[2],
            'replyId': 0
        }).text

        return json.loads(res)['result']

    def dislike_reply(self) -> bool:

        res = requests.post('http://localhost:5000/dislikeReply', data={
            'customerAddress': self.accounts[1],
            'shopAddress': self.accounts[2],
            'replyId': 0
        }).text

        return json.loads(res)['result']

