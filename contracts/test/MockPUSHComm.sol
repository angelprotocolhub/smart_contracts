// SPDX-License-Identifier: MIT

pragma solidity 0.8.17;

contract MockPushComm {
    event NotificationPushed(
        address channel,
        address recipient,
        bytes identity
    );

    function sendNotification(
        address _channel,
        address _recipient,
        bytes calldata _identity
    ) external {
        emit NotificationPushed(_channel, _recipient, _identity);
    }
}
