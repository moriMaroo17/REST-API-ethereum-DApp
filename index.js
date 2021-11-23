const express = require('express');
const Web3 = require('web3')
const connection = require('./connection/app.js')

const PORT = 5000;

const app = express()

app.use(express.json())
app.use(express.urlencoded({extends: false}))


app.get('/login', (req, res) => {
    const {login, password} = req.body
    connection.login(login, password, (err, result) => {
        if (!err) {
            res.json({result})
        } else {
            console.log(err)
        }
    })
})

app.get('/getAccounts', (req, res) => {
    connection.getAccounts(accounts => {
        res.json({accounts})
    })
})

app.get('/getRole', (req, res) => {
    const {address} = req.body
    connection.getRole(address, (err, result) => {
        if (!err) {
            res.json({result})
        } else {
            console.log(err)
        }
    })
})

app.post('/register', (req, res) => {
    const {login, name, password, account} = req.body
    connection.register(login, name, password, account, (err, result) => {
        if (!err) {
            res.json({result: true})
        } else {
            console.log(err)
        }
    })
})

app.get('/getShop', (req, res) => {
    const {shopAddress} = req.body
    connection.getShop(shopAddress, (err, result) => {
        if (!err) {
            res.json({result})
        } else {
            console.log(err)
        }
    })
})

app.get('/getAllShops', async (req, res) => {
    var shops = []
    var users = []
    await connection.getUsers((err, result) => {
        if (!err) {
            users = result
        } else {
            console.log(err)
        }
    })
    for (let i = 0; i < users.length; i++) {
        await connection.getShop(users[i], (err, result) => {
                if (!err) {
                    if (result['name'] !== '') {
                        shops.push({
                            'address': users[i],
                            'name': result['name'],
                            'city': result['city'],
                            'sellers': result['shop_sellers']
                        })
                    }
                } else {
                    console.log(err)
                }   
            })
        }
    res.json({shops})
})

app.get('/getBalance', (req, res) => {
    const {address} = req.body
    connection.getBalance(address, balance => {
        res.json({balance})
    })
})

app.get('/getCustomer', (req, res) => {
    const {address} = req.body
    connection.getCustomer(address, (err, result) => {
        if (!err) {
            res.json({result: {
                login: result[0],
                name: result[1]
            }})
        } else {
            console.log(err)
        }
    })
})

app.get('/getUsers', (req, res) => {
    connection.getUsers((err, result) => {
        if (!err) {
            res.json({result})
        } else {
            console.log(err)
        }
    })
})

app.post('/addShop', (req, res) => {
    const {adminAddress, shopAddress, name, city, password} = req.body
    connection.addShop(adminAddress, shopAddress, name, city, password, (err, result) => {
        if (!err) {
            res.json({result: true})
        } else {
            console.log(err)
        }
    })
})

app.post('/askForUp', (req, res) => {
    const {customerAddress, shopAddress} = req.body
    connection.askForUp(customerAddress, shopAddress, (err, result) => {
        if (!err) {
            res.json({result: true})
        } else {
            console.log(err)
        }
    })
})

app.post('/askForDown', (req, res) => {
    const {sellerAddress} = req.body
    connection.askForDown(sellerAddress, (err, result) => {
        if (!err) {
            res.json({result: true})
        } else {
            console.log(err)
        }
    })
})

app.get('/getAskForUp', (req, res) => {
    const {customerAddress} = req.body
    connection.getAskForUp(customerAddress, (err, result) => {
        if (!err) {
            res.json(result)
        } else {
            console.log(err)
        }
    })
})

app.get('/getAllAsksForUp', async (req, res) => {
    var asks = []
    var users = []
    await connection.getUsers((err, result) => {
        if (!err) {
            users = result
        } else {
            console.log(err)
        }
    })
    for (let i = 0; i < users.length; i++) {
        await connection.getAskForUp(users[i], (err, result) => {
                if (!err) {
                    if (result !== '0x0000000000000000000000000000000000000000') {
                        asks.push({
                            'asker': users[i],
                            'shopAddress': result
                        })
                    }  
                } else {
                    console.log(err)
                }   
            })
        }
    res.json({asks})
})

app.get('/getAskForDown', (req, res) => {
    const {sellerAddress} = req.body
    connection.getAskForDown(sellerAddress, (err, result) => {
        if (!err) {
            res.json(result)
        } else {
            console.log(err)
        }
    })
})

app.get('/getAllAsksForDown', async (req, res) => {
    var asks = []
    var users = []
    await connection.getUsers((err, result) => {
        if (!err) {
            users = result
        } else {
            console.log(err)
        }
    })
    for (let i = 0; i < users.length; i++) {
        await connection.getAskForDown(users[i], (err, result) => {
                if (!err) {
                    if (result !== '0x0000000000000000000000000000000000000000') {
                        asks.push({
                            'asker': users[i],
                            'shopAddress': result
                        })
                    }  
                } else {
                    console.log(err)
                }   
            })
        }
    res.json({asks})
})

app.post('/upRole', (req, res) => {
    const {customerAddress, adminAddress} = req.body
    connection.upRole(customerAddress, adminAddress, (err, result) => {
        if (!err) {
            res.json({result: true})
        } else {
            console.log(err)
        }
    })
})

app.post('/downRole', (req, res) => {
    const {sellerAddress, adminAddress} = req.body
    connection.downRole(sellerAddress, adminAddress, (err, result) => {
        if (!err) {
            res.json({result: true})
        } else {
            console.log(err)
        }
    })
})

app.post('/createBankAccount', (req, res) => {
    const {bankName, bankAddress, adminAddress} = req.body
    connection.createBankAccount(bankName, bankAddress, adminAddress, (err, result) => {
        if (!err) {
            res.json({result: true})
        } else {
            console.log(err)
        }
    })
})

app.post('/sendMoney', (req, res) => {
    const {shopAddress, bankAddress, value} = req.body
    connection.sendMoney(shopAddress, bankAddress, value, (err, result) => {
        if (!err) {
            res.json({result: true})
        } else {
            console.log(err)
        }
    })
})

app.get('/getDebtList', async (req, res) => {
    var debts = []
    var users = []
    await connection.getUsers((err, result) => {
        if (!err) {
            users = result
        } else {
            console.log(err)
        }
    })
    for (let i = 0; i < users.length; i++) {
        await connection.getDebt(users[i], (err, result) => {
                if (!err) {
                    if (result !== '0') {
                        debts.push({
                            'shop': users[i],
                            'debt': result
                        })
                    }
                } else {
                    console.log(err)
                }   
            })
        }
    res.json({debts})
})

app.post('/addAdmin', async (req, res) => {
    const {newAdminAddress, adminAddress} = req.body
    connection.addAdmin(newAdminAddress, adminAddress, (err, result) => {
        if (!err) {
            res.json({result: true})
        } else {
            console.log(err)
        }
    })
})

app.get('/getAllAsksBank', async (req, res) => {
    var asks = []
    var users = []
    await connection.getUsers((err, result) => {
        if (!err) {
            users = result
        } else {
            console.log(err)
        }
    })
    for (let i = 0; i < users.length; i++) {
        await connection.getAskBank(users[i], (err, result) => {
                if (!err) {
                    if (result !== '0') {
                        debts.push({
                            'shop': users[i],
                            'value': result
                        })
                    }
                } else {
                    console.log(err)
                }   
            })
        }
    res.json({asks})
})

app.get('/getAllAdmins', async (req, res) => {
    var admins = []
    var users = []
    await connection.getUsers((err, result) => {
        if (!err) {
            users = result
        } else {
            console.log(err)
        }
    })
    for (let i = 0; i < users.length; i++) {
        await connection.getAdmin(users[i], (err, result) => {
                if (!err) {
                    if (result['name'] !== '') {
                        admins.push({
                            'address': users[i],
                            'name': result['name'],
                            'login': result['login'],
                        })
                    }
                } else {
                    console.log(err)
                }   
            })
        }
    res.json({admins})
})


app.listen(PORT, () => {

    connection.web3 = new Web3(new Web3.providers.HttpProvider('http://localhost:8545'))
    connection.start()

    console.log(`App listening on address http://localhost:${PORT}`)
})
