const express = require('express');
const Web3 = require('web3')
const connection = require('./connection/app.js')

const PORT = 5000;

const app = express()

app.use(express.json())
app.use(express.urlencoded({extends: false}))


app.post('/login', (req, res) => {
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
            res.json({result: {
                name: result[0],
                city: result[1],
                sellers: result[2],
                rate: result[3] / 100
            }})
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
            res.json({result})
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
            res.json({result})
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
    const {bankName, bankAddress, adminAddress, password} = req.body
    connection.createBankAccount(bankName, bankAddress, adminAddress, password, (err, result) => {
        if (!err) {
            res.json({result: true})
        } else {
            console.log(err)
        }
    })
})

app.get('/getBank', (req, res) => {
    connection.getBank((err, result) => {
        if (!err) {
            res.json({result: {
                name: result[0],
                bankAddress: result[1]
            }})
        } else {
            console.log(err)
        }
    })
})

app.post('/askBank', (req, res) => {
    const {shopAddress, value} = req.body
    connection.askBank(shopAddress, value, (err, result) => {
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
                        asks.push({
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

app.post('/deleteShop', async (req, res) => {
    const {shopAddress, adminAddress} = req.body
    await connection.deleteShop(shopAddress, adminAddress, (err, result) => {
        if (!err) {
            res.json({result: true})
        } else {
            console.log(err)
        }
    })
})

// Routes for role model (Accounts.sol) end here

// Router for review book feature (ReviewBook.sol) starts here

app.get('/getComment', async (req, res) => {
    var comment;
    var owner;
    const {shopAddress, index} = req.body
    await connection.getComment(shopAddress, index, (err, result) => {
        if (!err) {
            comment = result
        } else {
            console.log(err)
        }
    })
    await connection.getCustomer(comment['owner'], (err, result) => {
        if (!err) {
            owner = result['name']
        } else {
            console.log(err)
        }
    })
    res.json({
        owner: owner,
        message: comment['message'],
        rate: comment['rate'],
        likes: comment['likes'],
        dislikes: comment['dislikes']
    })
})

app.get('/getReply', async (req, res) => {
    var reply;
    var owner;
    const {shopAddress, index} = req.body
    await connection.getReply(shopAddress, index, (err, result) => {
        if (!err) {
            reply = result
        } else {
            console.log(err)
        }
    })
    await connection.getCustomer(reply['owner'], (err, result) => {
        if (!err) {
            owner = result['name']
        } else {
            console.log(err)
        }
    })
    res.json({
        owner: owner,
        commentId: reply['comment_id'],
        message: reply['message'],
        rate: reply['rate'],
        likes: reply['likes'],
        dislikes: reply['dislikes']
    })
})

app.post('/commentShop', async (req, res) => {
    const {customerAddress, shopAddress, message, rate} = req.body
    connection.commentShop(customerAddress, shopAddress, message, rate, (err, result) => {
        if (!err) {
            res.json({result: true})
        } else {
            console.log(err)
        }
    })
})

app.post('/replyOnComment', async (req, res) => {
    const {customerAddress, shopAddress, message, rate, commentId} = req.body
    connection.replyOnComment(customerAddress, shopAddress, message, rate, commentId, (err, result) => {
        if (!err) {
            res.json({result: true})
        } else {
            console.log(err)
        }
    })
})

app.post('/replyOnCommentByShop', async (req, res) => {
    const {sellerAddress, shopAddress, message, commentId} = req.body
    connection.replyOnCommentByShop(sellerAddress, shopAddress, message, commentId, (err, result) => {
        if (!err) {
            res.json({result: true})
        } else {
            console.log(err)
        }
    })
})

app.post('/likeComment', async (req, res) => {
    const {customerAddress, shopAddress, commentId} = req.body
    connection.likeComment(customerAddress, shopAddress, commentId, (err, result) => {
        if (!err) {
            res.json({result: true})
        } else {
            console.log(err)
        }
    })
})

app.post('/dislikeComment', async (req, res) => {
    const {customerAddress, shopAddress, commentId} = req.body
    connection.dislikeComment(customerAddress, shopAddress, commentId, (err, result) => {
        if (!err) {
            res.json({result: true})
        } else {
            console.log(err)
        }
    })
})

app.post('/likeReply', async (req, res) => {
    const {customerAddress, shopAddress, replyId} = req.body
    connection.likeReply(customerAddress, shopAddress, replyId, (err, result) => {
        if (!err) {
            res.json({result: true})
        } else {
            console.log(err)
        }
    })
})

app.post('/dislikeReply', async (req, res) => {
    const {customerAddress, shopAddress, replyId} = req.body
    connection.dislikeReply(customerAddress, shopAddress, replyId, (err, result) => {
        if (!err) {
            res.json({result: true})
        } else {
            console.log(err)
        }
    })
})

app.listen(PORT, () => {

    connection.web3 = new Web3(new Web3.providers.HttpProvider('http://localhost:8545'))
    connection.start()

    console.log(`App listening on address http://localhost:${PORT}`)
})
