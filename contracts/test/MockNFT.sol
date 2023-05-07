// SPDX-License-Identifier: MIT

pragma solidity 0.8.17;

import {ERC721} from "@openzeppelin/contracts/token/ERC721/ERC721.sol";

// contract
contract MockNFT is ERC721 {
    constructor() ERC721("MockNFT", "MFT") {}

    function mintFree(uint256 _tokenId) public {
        _mint(msg.sender, _tokenId);
    }
}
