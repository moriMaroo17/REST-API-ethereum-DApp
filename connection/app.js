const contract = require('../bin/contracts/Accounts.json')

module.exports = {

    web3: null,
    contractAddress: null,

    start: async function () {
        const accounts = await this.web3.eth.getAccounts()

        if (accounts) {
            console.log('Attempting to deploy from account', accounts[0]);
        } else {
            console.log('No accounts detected')
        }

        const result = await new this.web3.eth.Contract(contract.abi)
            .deploy({ data: contract.bytecode })
            .send({ gas: 4712388, from: accounts[0] })

        this.contractAddress = result._address
    },

    register: async function (login, name, password, address, callback) {
        const instance = await new this.web3.eth.Contract(contract.abi, this.contractAddress)
        await instance.setProvider(this.web3.currentProvider)
        await instance.methods.add_customer(login, name, password)
            .send({ gas: 4712388, from: address }, (error, result) => {
                callback(error, result)
            })
    },

    getAccounts: async function (callback) {
        const accounts = await this.web3.eth.getAccounts()
        callback(accounts)
    },

    login: async function (login, password, callback) {
        const instance = await new this.web3.eth.Contract(contract.abi, this.contractAddress)
        await instance.setProvider(this.web3.currentProvider)
        await instance.methods.check_auth_data(login, password)
            .call((error, result) => {
                callback(error, result)
            })
    },

    getRole: async function (address, callback) {
        const instance = await new this.web3.eth.Contract(contract.abi, this.contractAddress)
        await instance.setProvider(this.web3.currentProvider)
        await instance.methods.get_role(address)
            .call((error, result) => {
                callback(error, result)
            })
    },

    getShop: async function(shopAddress, callback) {
        const instance = await new this.web3.eth.Contract(contract.abi, this.contractAddress)
        await instance.setProvider(this.web3.currentProvider)
        await instance.methods.get_shop(shopAddress)
            .call((error, result) => {
                callback(error, result)
            })
    },

    getUsers: async function(callback) {
        const instance = await new this.web3.eth.Contract(contract.abi, this.contractAddress)
        await instance.setProvider(this.web3.currentProvider)
        await instance.methods.get_users()
            .call((error, result) => {
                callback(error, result)
            })
    },

    getCustomer: async function(customerAddress, callback) {
        const instance = await new this.web3.eth.Contract(contract.abi, this.contractAddress)
        await instance.setProvider(this.web3.currentProvider)
        await instance.methods.get_customer(customerAddress)
            .call((error, result) => {
                callback(error, result)
            })
    },

    getBalance: async function(address, callback) {
        const balance = await this.web3.eth.getBalance(address)
        callback(balance)
    },

    addShop: async function(adminAddress, shopAddress, name, city, password, callback) {
        const instance = await new this.web3.eth.Contract(contract.abi, this.contractAddress)
        await instance.setProvider(this.web3.currentProvider)
        await instance.methods.add_shop(shopAddress, name, city, password)
            .send({gas: 4712388, from: adminAddress}, (error, result) => {
                callback(error, result)
            })
    },

    askForUp: async function(customerAddress, shopAddress, callback) {
        const instance = await new this.web3.eth.Contract(contract.abi, this.contractAddress)
        await instance.setProvider(this.web3.currentProvider)
        await instance.methods.ask_for_up(shopAddress)
            .send({gas: 100000, from: customerAddress}, (error, result) => {
                callback(error, result)
            })
    },

    askForDown: async function(sellerAddress, callback) {
        const instance = await new this.web3.eth.Contract(contract.abi, this.contractAddress)
        await instance.setProvider(this.web3.currentProvider)
        await instance.methods.ask_for_down()
            .send({gas: 100000, from: sellerAddress}, (error, result) => {
                callback(error, result)
            })
    },

    getAskForUp: async function(customerAddress, callback) {
        const instance = await new this.web3.eth.Contract(contract.abi, this.contractAddress)
        await instance.setProvider(this.web3.currentProvider)
        await instance.methods.get_ask_for_up(customerAddress)
            .call((error, result) => {
                callback(error, result)
            })
    },

    getAskForDown: async function(sellerAddress, callback) {
        const instance = await new this.web3.eth.Contract(contract.abi, this.contractAddress)
        await instance.setProvider(this.web3.currentProvider)
        await instance.methods.get_ask_for_down(sellerAddress)
            .call((error, result) => {
                callback(error, result)
            })
    },

    upRole: async function(customerAddress, adminAddress, callback) {
        const instance = await new this.web3.eth.Contract(contract.abi, this.contractAddress)
        await instance.setProvider(this.web3.currentProvider)
        await instance.methods.up_role(customerAddress)
            .send({gas: 4712388, from: adminAddress}, (error, result) => {
                callback(error, result)
            })
    },

    downRole: async function(sellerAddress, adminAddress, callback) {
        const instance = await new this.web3.eth.Contract(contract.abi, this.contractAddress)
        await instance.setProvider(this.web3.currentProvider)
        await instance.methods.down_role(sellerAddress)
            .send({gas: 4712388, from: adminAddress}, (error, result) => {
                callback(error, result)
            })
    },

    createBankAccount: async function(bankName, bankAddress, adminAddress, callback) {
        const instance = await new this.web3.eth.Contract(contract.abi, this.contractAddress)
        await instance.setProvider(this.web3.currentProvider)
        await instance.methods.create_bank_account(bankName, bankAddress)
            .send({gas: 4712388, from: adminAddress}, (error, result) => {
                callback(error, result)
            })
    },

    sendMoney: async function(shopAddress, bankAddress, value, callback) {
        const instance = await new this.web3.eth.Contract(contract.abi, this.contractAddress)
        await instance.setProvider(this.web3.currentProvider)
        await instance.methods.send_money(shopAddress)
            .send({gas: 4712388, from: bankAddress, value: this.web3.utils.toWei(value, 'ether')}, (error, result) => {
                callback(error, result)
            })
    },

    getDebt: async function(shopAddress, callback) {
        const instace = await new this.web3.eth.Contract(contract.abi, this.contractAddress)
        await instace.setProvider(this.web3.currentProvider)
        await instace.methods.get_debt(shopAddress)
            .call((error, result) => {
                callback(error, result)
            })
    },

    askBank: async function(shopAddress, value, callback) {
        const instance = await new this.web3.eth.Contract(contract.abi, this.contractAddress)
        await instance.setProvider(this.web3.currentProvider)
        await instance.methods.ask_bank(shopAddress, value)
            .send({gas: 4712388, from: shopAddress}, (error, result) => {
                callback(error, result)
            })
    },

    addAdmin: async function(newAdminAddress, adminAddress, callback) {
        const instance = await new this.web3.eth.Contract(contract.abi, this.contractAddress)
        await instance.setProvider(this.web3.currentProvider)
        await instance.methods.add_admin(newAdminAddress)
            .send({gas: 4712388, from: adminAddress}, (error, result) => {
                callback(error, result)
            })
    },

    getAskBank: async function(shopAddress, callback) {
        const instance = await new this.web3.eth.Contract(contract.abi, this.contractAddress)
        await instance.setProvider(this.web3.currentProvider)
        await instance.methods.get_ask_bank(shopAddress)
            .call((error, result) => {
                callback(error, result)
            })
    },

    getAdmin: async function(adminAddress, callback) {
        const instance = await new this.web3.eth.Contract(contract.abi, this.contractAddress)
        await instance.setProvider(this.web3.currentProvider)
        await instance.methods.get_admin(adminAddress)
            .call((error, result) => {
                callback(error, result)
            }) 
    }
}