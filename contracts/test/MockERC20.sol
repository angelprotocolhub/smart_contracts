// SPDX-License-Identifier: MIT

pragma solidity 0.8.17;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";

// contract
contract MockToken is ERC20 {
    constructor() ERC20("MockToken", "MTN") {}

    function mintFree(uint256 _amount) public {
        _mint(msg.sender, _amount);
    }
}
