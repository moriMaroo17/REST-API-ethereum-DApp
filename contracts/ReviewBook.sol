// SPDX-License-Identifier: MIT
pragma solidity < 0.9.0;

import "./Accounts.sol";

contract ReviewBook is Accounts {

    struct Comment {
        address owner;
        string message;
        uint8 rate;
        uint128 likes;
        uint128 dislikes;
    }

    struct Reply {
        address owner;
        uint256 comment_id;
        string message;
        uint8 rate;
        uint128 likes;
        uint128 dislikes;
    }

    mapping (address => Comment[]) public comments;
    mapping (address => Reply[]) public replyes;

    function get_comment(address _shop_address, uint256 _index) public view returns (Comment memory) {
        return comments[_shop_address][_index];
    }

    function get_reply(address _shop_address, uint256 _index) public view returns (Reply memory) {
        return replyes[_shop_address][_index];
    }

    function comment_shop(address _shop_address, string memory _message, uint8 _rate) public {
        if (role_per_address[msg.sender] == Role.Seller) {
            require(sellers[msg.sender].shop_address != _shop_address);
        }
        comments[_shop_address].push(Comment(msg.sender, _message, _rate, 0, 0));
    }

    function reply_on_comment(address _shop_address, string memory _message, uint8 _rate, uint256 _comment_id) public {
        if (role_per_address[msg.sender] == Role.Seller) {
            require(sellers[msg.sender].shop_address != _shop_address);
        }
        replyes[_shop_address].push(Reply(msg.sender, _comment_id, _message, _rate, 0, 0));
    }

    function reply_on_comment_by_shop(address _shop_address, string memory _message, uint256 _comment_id) public {
        require(sellers[msg.sender].shop_address == _shop_address);
        replyes[_shop_address].push(Reply(msg.sender, _comment_id, _message, 0, 0, 0));
    }
}