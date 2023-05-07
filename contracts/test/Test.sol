//SPDX-License-identifier: MIT

pragma solidity 0.8.17;

contract Test {
    bytes32 private hashedCode;

    function storeCodeHash(bytes32 _hashedCode) public {
        hashedCode = _hashedCode;
    }

    function validateCode(bytes memory _code) public view returns (bool) {
        bytes32 codeHash = keccak256(_code);
        return (codeHash == hashedCode);
    }
}
