// SPDX-License-Identifier: MIT
pragma solidity < 0.9.0;

contract Accounts {

    enum Role {
        Bank,
        Shop,
        Provider,
        Seller,
        Customer,
        Admin,
        Guest
    }

    struct Bank {
        string name;
        address bank_address;
    }

    struct Shop {
        string name;
        string city;
        address[] shop_sellers;
        uint16 rate;
        uint256 using_reviews;
    }

    struct Provider {
        string name;
    }

    struct Seller {
        string login;
        string name;
        string city;
        address shop_address;
    }

    struct Customer {
        string login;
        string name;
    }

    struct Admin {
        string login;
        string name;
    }

    address[] public users;

    mapping(address => Role) public role_per_address;
    mapping(string => bytes32) private auth_data;
    mapping(string => address) public address_per_login;

    mapping(address => address) public asks_for_up;
    mapping(address => address) public asks_for_down;

    mapping(address => uint256) public asks_bank;
    
    Bank main_bank;

    mapping(address => uint256) main_bank_creditors;

    mapping(address => Shop) public shops;
    mapping(address => Provider) public providers;
    mapping(address => Seller) public sellers;
    mapping(address => Customer) public customers;
    mapping(address => Admin) public admins;

    function get_role(address _user_address) public view returns (string memory) {
        Role role = role_per_address[_user_address];
        if (role == Role.Bank) {
            return "bank";
        } else if (role == Role.Shop) {
            return "shop";
        } else if (role == Role.Provider) {
            return "provider";
        } else if (role == Role.Seller) {
            return "seller";
        } else if (role == Role.Customer) {
            return "customer";
        } else if (role == Role.Admin) {
            return "admin";
        }
        return "guest";
    }

    function add_admin(address _new_admin_address) public {
        admins[_new_admin_address] = Admin(customers[_new_admin_address].login, customers[_new_admin_address].name);
        role_per_address[_new_admin_address] = Role.Admin;
    }

    function ask_bank(address _shop_address, uint256 value) public {
        asks_bank[_shop_address] = value;
    }

    function create_bank_account(string memory _bank_name, address _bank_address, string memory _password) public {
        main_bank = Bank(_bank_name, _bank_address);
        role_per_address[_bank_address] = Role.Bank;
        auth_data[_bank_name] = keccak256(abi.encode(_password));
    }

    function get_bank() public view returns (Bank memory) {
        return main_bank;
    }

    function add_customer(string memory _login, string memory _name, string memory _password) public {
        customers[msg.sender] = Customer(_login, _name);
        auth_data[_login] = keccak256(abi.encode(_password));
        role_per_address[msg.sender] = Role.Customer;
        address_per_login[_login] = msg.sender;
        users.push(msg.sender);
    }

    function send_money(address _shop_address) public payable {
        main_bank_creditors[_shop_address] = msg.value;
        payable(_shop_address).transfer(msg.value);
        delete asks_bank[_shop_address];
    }

    function add_shop(address payable _shop_address, string memory _name, string memory _city, string memory _password) public {
        Shop memory shop;
        shop.name = _name;
        shop.city = _city;
        shop.rate = 0;
        shop.using_reviews = 0;
        shops[_shop_address] = shop;
        role_per_address[_shop_address] = Role.Shop;
        auth_data[_name] = keccak256(abi.encode(_password));
       
        users.push(_shop_address);
    }

    function check_auth_data(string memory _login, string memory _password) public view returns (bool) {
        return (auth_data[_login] == keccak256(abi.encode(_password)));
    }

    function ask_for_up(address _shop_address) public {
        asks_for_up[msg.sender] = _shop_address;
    }

    function ask_for_down() public {
        asks_for_down[msg.sender] = sellers[msg.sender].shop_address;
    }

    function get_users() public view returns (address[] memory) {
        return users;
    }

    function get_shop(address _shop_address) public view returns (Shop memory) {
        return shops[_shop_address];
    }

    function get_admin(address _admin_address) public view returns (Admin memory) {
        return admins[_admin_address];
    }

    function get_customer(address _customer_address) public view returns (Customer memory) {
        return customers[_customer_address];
    }

    function get_ask_for_up(address _customer_address) public view returns (address) {
        return asks_for_up[_customer_address];
    }

    function get_ask_for_down(address _customer_address) public view returns (address) {
        return asks_for_down[_customer_address];
    }

    function get_ask_bank(address _shop_address) public view returns (uint256) {
        return asks_bank[_shop_address];
    }

    function up_role(address _customer_address) public {
        address shop_address = asks_for_up[_customer_address];
        sellers[_customer_address] = Seller(
            customers[_customer_address].login,
            customers[_customer_address].name,
            shops[shop_address].city,
            shop_address
        );
        role_per_address[_customer_address] = Role.Seller;
        shops[shop_address].shop_sellers.push(_customer_address);
        delete asks_for_up[_customer_address];
    }

    // function _get_seller_index(address _shop_address, address _seller_address) internal view returns (uint256) {
    //     address[] storage shop_sellers = shops[_shop_address].shop_sellers;
    //     for (uint256 i = 0; i < shop_sellers.length; i++) {
    //         if (shop_sellers[i] == _seller_address) {
    //             return i;
    //         }
    //     }
    // }

    function down_role(address _seller_address) public {
        // uint256 index = _get_seller_index(asks_for_down[_seller_address], _seller_address);
        // address[] storage shop_sellers = shops[asks_for_down[_seller_address]].shop_sellers;
        // role_per_address[_seller_address] = Role.Customer;
        // delete shop_sellers[index];
        // shop_sellers[index] = shop_sellers[shop_sellers.length - 1];
        // delete shop_sellers[shop_sellers.length - 1];
        // delete asks_for_down[_seller_address];
        address[] storage shop_sellers = shops[
            sellers[_seller_address].shop_address
        ].shop_sellers;
        for (uint24 i = 0; i < shop_sellers.length; i++) {
            if (shop_sellers[i] == _seller_address) {
                delete shop_sellers[i];
                shop_sellers[i] = shop_sellers[shop_sellers.length - 1];
                delete shop_sellers[shop_sellers.length - 1];
                break;
            }
        }
        role_per_address[_seller_address] = Role.Customer;
        delete sellers[_seller_address];
        delete asks_for_down[_seller_address];
    }

    function get_debt(address _shop_address) public view returns (uint256) {
        return main_bank_creditors[_shop_address];
    }

    function delete_shop(address _shop_address) public {
        for (uint24 i = 0; i < shops[_shop_address].shop_sellers.length; i++) {
            down_role(shops[_shop_address].shop_sellers[i]);
        }
        delete auth_data[shops[_shop_address].name];
        delete role_per_address[_shop_address];

        for (uint128 i = 0; i < users.length; i++) {
            if (users[i] == _shop_address ) {
                delete users[i];
                break;
            }
        }

        delete shops[_shop_address];
    }
}