// SPDX-License-Identifier: MIT

pragma solidity 0.8.17;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";

// contract
contract MockLiveToken is ERC20 {
    constructor(
        string memory _name,
        string memory _symbol
    ) ERC20(_name, _symbol) {}

    function mintFree(address _user, uint256 _amount) public {
        _mint(_user, _amount);
    }
}
