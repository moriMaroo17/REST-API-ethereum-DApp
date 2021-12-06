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
        bool in_use;
    }

    struct Reply {
        address owner;
        uint256 comment_id;
        string message;
        uint8 rate;
        uint128 likes;
        uint128 dislikes;
        bool in_use;
    }

    mapping (address => Comment[]) public comments;
    mapping (address => Reply[]) public replyes;

    function get_comment(address _shop_address, uint256 _comment_id) public view returns (Comment memory) {
        return comments[_shop_address][_comment_id];
    }

    function get_reply(address _shop_address, uint256 _comment_id) public view returns (Reply memory) {
        return replyes[_shop_address][_comment_id];
    }

    function comment_shop(address _shop_address, string memory _message, uint8 _rate) public {
        if (role_per_address[msg.sender] == Role.Seller) {
            require(sellers[msg.sender].shop_address != _shop_address);
        }
        comments[_shop_address].push(Comment(msg.sender, _message, _rate, 0, 0, false));
    }

    function reply_on_comment(address _shop_address, string memory _message, uint8 _rate, uint256 _comment_id) public {
        if (role_per_address[msg.sender] == Role.Seller) {
            require(sellers[msg.sender].shop_address != _shop_address);
        }
        replyes[_shop_address].push(Reply(msg.sender, _comment_id, _message, _rate, 0, 0, false));
    }

    function reply_on_comment_by_shop(address _shop_address, string memory _message, uint256 _comment_id) public {
        require(sellers[msg.sender].shop_address == _shop_address);
        replyes[_shop_address].push(Reply(msg.sender, _comment_id, _message, 0, 0, 0, false));
    }

    function _check_comment_for_using(address _shop_address, uint256 _comment_id) internal view returns (bool) {
        Comment memory comment = comments[_shop_address][_comment_id];
        
        if (comment.likes > 9 && comment.likes > comment.dislikes) {
            return true;
        }
        return false;
    }

    function _check_reply_for_using(address _shop_address, uint256 _reply_id) internal view returns (bool) {
        Reply memory reply = replyes[_shop_address][_reply_id];
        
        if (reply.likes > 9 && reply.likes > reply.dislikes && reply.rate != 0) {
            return true;
        }
        return false;
    }

    function like_comment(address _shop_address, uint256 _comment_id) public {
        Comment storage liked_comment = comments[_shop_address][_comment_id];
        bool already_using = _check_comment_for_using(_shop_address, _comment_id);
        liked_comment.likes += 1;
        if (!already_using && _check_comment_for_using(_shop_address, _comment_id)) {
            liked_comment.in_use = true;
            Shop storage liked_shop = shops[_shop_address];
            liked_shop.rate = _count_rate(_shop_address);
        }
    }

    function dislike_comment(address _shop_address, uint256 _comment_id) public {
        Comment storage disliked_comment = comments[_shop_address][_comment_id];
        bool already_using = _check_comment_for_using(_shop_address, _comment_id);
        disliked_comment.dislikes += 1;
        if (already_using && !_check_comment_for_using(_shop_address, _comment_id)) {
            disliked_comment.in_use = false;
            Shop storage disliked_shop = shops[_shop_address];
            disliked_shop.rate = _count_rate(_shop_address);
        }
    }

    function like_reply(address _shop_address, uint256 _reply_id) public {
        Reply storage liked_reply = replyes[_shop_address][_reply_id];
        bool already_using = _check_reply_for_using(_shop_address, _reply_id);
        liked_reply.likes += 1;
        if (!already_using && _check_reply_for_using(_shop_address, _reply_id) && liked_reply.rate != 0) {
            liked_reply.in_use = true;
            Shop storage liked_shop = shops[_shop_address];
            liked_shop.rate = _count_rate(_shop_address);
        }
    }

    function dislike_reply(address _shop_address, uint256 _reply_id) public {
        Reply storage disliked_reply = replyes[_shop_address][_reply_id];
        bool already_using = _check_reply_for_using(_shop_address, _reply_id);
        disliked_reply.dislikes += 1;
        if (already_using && !_check_reply_for_using(_shop_address, _reply_id) && disliked_reply.rate != 0) {
            disliked_reply.in_use = true;
            Shop storage disliked_shop = shops[_shop_address];
            disliked_shop.rate = _count_rate(_shop_address);
        }
    }

    function _count_rate(address _shop_address) internal view returns (uint16){
        uint256 new_rate = 0;
        uint256 counter = 0;
        for (uint256 i = 0; i < comments[_shop_address].length; i++) {
            if (comments[_shop_address][i].in_use) {
                new_rate += comments[_shop_address][i].rate * (comments[_shop_address][i].likes / (comments[_shop_address][i].likes + comments[_shop_address][i].dislikes));
                counter++;
            }
        }

        for (uint256 i = 0; i < replyes[_shop_address].length; i++) {
            if (comments[_shop_address][i].in_use) {
                new_rate += replyes[_shop_address][i].rate * (replyes[_shop_address][i].likes / (replyes[_shop_address][i].likes + replyes[_shop_address][i].dislikes));
                counter++;
            }
        }

        return uint16(new_rate / counter * 100);
    }
}