// SPDX-License-Identifier: MIT

pragma solidity 0.8.3;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {ERC721} from "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import {Strings} from "@openzeppelin/contracts/utils/Strings.sol";

import {IPUSHCommInterface} from "../interfaces/PushCommInterface.sol";

import {AutomationCompatibleInterface} from "@chainlink/contracts/src/v0.8/interfaces/automation/AutomationCompatibleInterface.sol";

contract Angel is AutomationCompatibleInterface {
    uint256 constant MAX_HANDLE_LENGTH = 15;
    string constant SALT = "ImTheSalttt";
    string constant DEFAULT_USERNAME = "nousername";
    string constant DEFAULT_PROFILE_PICTURE =
        "https://bafybeifnpeom22nwbtsv52ivwqd3fzaygmjjgql5wgeximwvl4s32mvdo4.ipfs.w3s.link/petergriffin.jpg";

    uint256 public listCounter;

    address public COMM_CONTRACT_ADDRESS;
    address public CHANNEL_ADDRESS;

    mapping(address => string) public userName;
    mapping(string => address) public userNameAddress;
    mapping(address => string) public profileImage;

    mapping(string => bool) public userNameExistence;
    mapping(address => bool) public addressExists;
    mapping(address => string) public profilePicture;

    mapping(address => uint256) public senderNonce;
    mapping(bytes32 => Transaction) public transactions;

    mapping(address => mapping(address => bool)) public beneficaries;

    Transaction[] public transactionList;

    struct Transaction {
        address sender;
        address recipient;
        address asset;
        uint256 amountOrTokenId;
        string narration;
        uint8 status; // 1 - pending, 2 - successfull and 3 - reclaimed
        uint256 time;
        bytes32 claimCode;
        uint256 endTime;
        bytes32 ref;
        bool txType; // false - crypto, true - nfts
        uint256 listId;
    }

    event Angel__AccountCreated(address user, string profileImage);

    event AssetSent(
        address sender,
        string senderUserName,
        address recipient,
        string recipientUserName,
        address asset,
        uint256 amount,
        string narration,
        uint8 status,
        bytes32 txReference,
        uint256 time,
        bool txType
    );

    event AssetClaimed(
        address sender,
        string senderUserName,
        address recipient,
        string recipientUserName,
        address asset,
        uint256 amount,
        uint8 status,
        bytes32 txReference,
        uint256 claimTime,
        bool txType
    );

    event AssetReclaimed(
        address sender,
        string senderUserName,
        address recipient,
        string recipientUserName,
        address asset,
        uint256 amount,
        uint8 status,
        bytes32 txReference,
        uint256 reclaimTime,
        bool txType
    );

    event AddedBeneficiary(address sender, address beneficiary);

    constructor(address _commAddress, address _channelAddress) {
        COMM_CONTRACT_ADDRESS = _commAddress;
        CHANNEL_ADDRESS = _channelAddress;
    }

    /**
     * @notice attaches username to an address across the supported chains
     * @param _userName the username
     * @param _profileImage the username
     */
    function registerAngelAccount(
        string memory _userName,
        string memory _profileImage
    ) public payable {
        checkHandleValidity(_userName);
        checkUserNameAndAddressExistence(_userName);

        userName[msg.sender] = _userName;
        profileImage[msg.sender] = _profileImage;

        userNameExistence[_userName] = true;
        addressExists[msg.sender] = true;
        userNameAddress[_userName] = msg.sender;
        profilePicture[msg.sender] = _profileImage;

        emit Angel__AccountCreated(msg.sender, _userName);
    }

    /**
     * @notice sends native asset of the chain and also erc20s to recipients
     * @param _recipient recipient address
     * @param _asset asset address
     * @param _amount asset amount
     * @param _narration transaction narration
     * @param _claimCode the claim code hash
     * @param _endTime the time in seconds for an unclaimed refund
     */
    function sendCrypto(
        address _recipient,
        address _asset,
        uint256 _amount,
        string memory _narration,
        bytes32 _claimCode,
        uint256 _endTime
    ) public payable {
        // check address exits
        if (!addressExists[msg.sender]) {
            revert("Sender Has No Username");
        }

        // handle native asset and token transfers
        if (_asset != address(0)) {
            ERC20(_asset).transferFrom(msg.sender, address(this), _amount);
        } else {
            require(msg.value >= _amount);
        }

        // comment out while testing
        // send notification via push protocol
        IPUSHCommInterface(COMM_CONTRACT_ADDRESS).sendNotification(
            CHANNEL_ADDRESS,
            _recipient,
            bytes(
                string(
                    abi.encodePacked(
                        "0",
                        "+",
                        "3",
                        "+",
                        "Crypto Credit Alert",
                        "+",
                        "Credit Alert: ",
                        getUsername(msg.sender),
                        " sent some ",
                        _asset == address(0) ? "matic" : ERC20(_asset).name(),
                        " to you! Make sure to claim before the claim period expires on our application. "
                    )
                )
            )
        );

        // generate, populate and store transaction then fire event
        generateTransaction(
            _recipient,
            _asset,
            _amount,
            _narration,
            _claimCode,
            _endTime,
            false
        );
    }

    /**
     * @notice send nfts to recipients
     * @param _recipient recipient address
     * @param _contractAddress nft contract address
     * @param _tokenId token id
     * @param _narration transaction narration
     * @param _claimCode the claim code hash
     * @param _endTime the time in seconds for an unclaimed refund
     */
    function sendNFT(
        address _recipient,
        address _contractAddress,
        uint256 _tokenId,
        string memory _narration,
        bytes32 _claimCode,
        uint256 _endTime
    ) public payable {
        // check address exists
        if (!addressExists[msg.sender]) {
            revert("Sender Has No Username");
        }

        // handle nft transfer
        ERC721(_contractAddress).transferFrom(
            msg.sender,
            address(this),
            _tokenId
        );

        // send notification via push protocol
        IPUSHCommInterface(COMM_CONTRACT_ADDRESS).sendNotification(
            CHANNEL_ADDRESS,
            _recipient,
            bytes(
                string(
                    abi.encodePacked(
                        "0",
                        "+",
                        "3",
                        "+",
                        "NFT Credit Alert",
                        "+",
                        "Credit Alert: ",
                        getUsername(msg.sender),
                        " sent an NFT. Name : ",
                        ERC721(_contractAddress).name(),
                        " , Token Id : ",
                        Strings.toString(_tokenId),
                        " to you! Make sure you claim before claim period expires!",
                        " NFT Contract Address : ",
                        addressToString(_contractAddress)
                    )
                )
            )
        );

        // generate populate and store transaction then fire event
        generateTransaction(
            _recipient,
            _contractAddress,
            _tokenId,
            _narration,
            _claimCode,
            _endTime,
            true
        );
    }

    /**
     * @notice claim funds sent to you
     * @param _txRef the unique transcation reference
     * @param _claimCode the code required to claim the asset
     */
    function claimFunds(bytes32 _txRef, string memory _claimCode) public {
        //check address exists
        if (!addressExists[msg.sender]) {
            revert("Sender Has No Username");
        }

        // tx status must be pending
        if (transactions[_txRef].status != 1) {
            revert("Transaction !Pending State");
        }

        // get tx recipient and sender
        address recipient = transactions[_txRef].recipient;
        address sender = transactions[_txRef].sender;

        // msg.sender must be recipient
        if (recipient != msg.sender) {
            revert("Sender Isnt Recipient");
        }

        // revert if claim time is over
        if (transactions[_txRef].endTime < block.timestamp) {
            revert("Claim Time Is Over");
        }

        // revert on incorrect claim code
        bool status = validateCode(_claimCode, _txRef);
        if (!status) {
            revert("Incorrect Claim Code");
        }

        // transfer assets to the recipient
        address asset = transactions[_txRef].asset;
        uint256 amountOrTokenId = transactions[_txRef].amountOrTokenId;

        // update tx status
        transactions[_txRef].status = 2;

        //handle crypto and nfts
        if (!transactions[_txRef].txType) {
            // handle native asset and token transfers
            if (asset != address(0)) {
                ERC20(asset).transfer(recipient, amountOrTokenId);
            } else {
                (bool success, ) = recipient.call{value: amountOrTokenId}("");
                require(success, "!successful");
            }

            // send notification via push protocol
            IPUSHCommInterface(COMM_CONTRACT_ADDRESS).sendNotification(
                CHANNEL_ADDRESS,
                sender,
                bytes(
                    string(
                        abi.encodePacked(
                            "0",
                            "+",
                            "3",
                            "+",
                            "Crypto Claim Alert",
                            "+",
                            "Crypto Claim: ",
                            getUsername(recipient),
                            " claimed the ",
                            asset == address(0) ? "matic" : ERC20(asset).name(),
                            " you sent them!"
                        )
                    )
                )
            );

            emit AssetClaimed(
                transactions[_txRef].sender,
                getUsername(transactions[_txRef].sender),
                recipient,
                getUsername(recipient),
                asset,
                amountOrTokenId,
                2,
                _txRef,
                block.timestamp,
                false
            );
        } else {
            ERC721(asset).transferFrom(
                address(this),
                recipient,
                amountOrTokenId
            );

            // send notification via push protocol
            IPUSHCommInterface(COMM_CONTRACT_ADDRESS).sendNotification(
                CHANNEL_ADDRESS,
                sender,
                bytes(
                    string(
                        abi.encodePacked(
                            "0",
                            "+",
                            "3",
                            "+",
                            "NFT Claim Alert",
                            "+",
                            "NFT Claimed: ",
                            getUsername(recipient),
                            " claimed an NFT you sent them. Name: ",
                            ERC721(asset).name(),
                            ", Token ID : ",
                            Strings.toString(amountOrTokenId),
                            ". NFT Contract Address : ",
                            addressToString(asset)
                        )
                    )
                )
            );

            emit AssetClaimed(
                transactions[_txRef].sender,
                getUsername(transactions[_txRef].sender),
                recipient,
                getUsername(recipient),
                asset,
                amountOrTokenId,
                2,
                _txRef,
                block.timestamp,
                true
            );
        }
    }

    /**
     * @notice reclaim funds on wrong transfer
     * @param _txRef the unique transcation reference
     */
    function reclaimFunds(bytes32 _txRef) public {
        // tx status must be pending
        if (transactions[_txRef].status != 1) {
            revert("Transaction Not Pending");
        }

        // get tx sender and recipient
        address sender = transactions[_txRef].sender;
        address recipient = transactions[_txRef].recipient;

        // revert if msg.sender isnt tx sender
        if (msg.sender != sender) {
            revert("Msg Sender Isnt Tx Sender");
        }

        transactions[_txRef].status = 3;
        transactionList[transactions[_txRef].listId].status = 3;

        // reclaim asset, update tx status and fire event
        handleReclaimAsset(_txRef, sender, recipient);
    }

    /**
     * @notice logic for handling reclaiming of assets for users and chainlink keepers
     * @param _recipient the recipient to be added as a beneficiary
     */
    function addToBeneficiaries(address _recipient) public {
        // must have an angel account
        if (!addressExists[msg.sender]) {
            revert("Sender Has No Username");
        }

        // recipient must also have an angel account
        if (!addressExists[_recipient]) {
            revert("Recipient Has No Username");
        }

        // add the beeficiary
        beneficaries[msg.sender][_recipient] = true;

        emit AddedBeneficiary(msg.sender, _recipient);
    }

    function changeProfilePicture(string memory _imageURI) public {
        // must have an angel account
        if (!addressExists[msg.sender]) {
            revert("Sender Has No Username");
        }

        profilePicture[msg.sender] = _imageURI;
    }

    /**
     * @notice logic for handling reclaiming of assets for users and chainlink keepers
     * @param _txRef the unique transcation reference
     * @param _sender tx sender
     * @param _recipient tx recipient
     */
    function handleReclaimAsset(
        bytes32 _txRef,
        address _sender,
        address _recipient
    ) internal {
        // update tx status

        // get asset address with amount/tokenId
        address asset = transactions[_txRef].asset;
        uint256 amountOrTokenId = transactions[_txRef].amountOrTokenId;

        // handle crypto or nft reclaims
        if (!transactions[_txRef].txType) {
            // handle native asset and token reclaims
            if (asset != address(0)) {
                ERC20(asset).transfer(_sender, amountOrTokenId);
            } else {
                (bool success, ) = _sender.call{value: amountOrTokenId}("");
                // require(success, "!successful");
            }

            // send notification via push protocol
            IPUSHCommInterface(COMM_CONTRACT_ADDRESS).sendNotification(
                CHANNEL_ADDRESS,
                _recipient,
                bytes(
                    string(
                        abi.encodePacked(
                            "0",
                            "+",
                            "3",
                            "+",
                            "Crypto Re-Claim Alert",
                            "+",
                            "Crypto Reclaimed: ",
                            getUsername(_recipient),
                            " re-claimed the ",
                            asset == address(0) ? "matic" : ERC20(asset).name(),
                            " they sent you!"
                        )
                    )
                )
            );

            // fire event
            emit AssetReclaimed(
                transactions[_txRef].sender,
                getUsername(_sender),
                _recipient,
                getUsername(_recipient),
                asset,
                amountOrTokenId,
                3,
                _txRef,
                block.timestamp,
                false
            );
        } else {
            // handle nft reclaims
            ERC721(asset).transferFrom(address(this), _sender, amountOrTokenId);

            // send notification via push protocol
            IPUSHCommInterface(COMM_CONTRACT_ADDRESS).sendNotification(
                CHANNEL_ADDRESS,
                _recipient,
                bytes(
                    string(
                        abi.encodePacked(
                            "0",
                            "+",
                            "3",
                            "+",
                            "NFT Re-Claim Alert",
                            "+",
                            "NFT Reclaimed: ",
                            getUsername(_recipient),
                            " re-claimed an NFT they sent you. Name : ",
                            ERC721(asset).name(),
                            ", Token ID : ",
                            Strings.toString(amountOrTokenId),
                            ". NFT Contract Address : ",
                            addressToString(asset)
                        )
                    )
                )
            );

            // fire event
            emit AssetReclaimed(
                transactions[_txRef].sender,
                getUsername(_sender),
                _recipient,
                getUsername(_recipient),
                asset,
                amountOrTokenId,
                3,
                _txRef,
                block.timestamp,
                true
            );
        }
    }

    // AUTOMATION Functions

    // check up keep
    function checkUpkeep(
        bytes calldata /* checkData */
    )
        external
        view
        override
        returns (bool upkeepNeeded, bytes memory performData)
    {
        uint256 counter;
        for (uint i = 0; i < transactionList.length; i++) {
            if (transactionList[i].status == 1) {
                if (block.timestamp > transactionList[i].endTime) {
                    counter++;
                }
            }
        }

        // uint256[] memory indexes = new uint256[](counter);
        Transaction[] memory txns = new Transaction[](counter);

        uint256 indexCounter;
        upkeepNeeded = false;

        for (uint i = 0; i < transactionList.length; i++) {
            if (transactionList[i].status == 1) {
                if (block.timestamp > transactionList[i].endTime) {
                    upkeepNeeded = true;

                    // indexes[indexCounter] = i;
                    txns[indexCounter] = transactionList[i];
                    indexCounter++;
                }
            }
        }

        performData = abi.encode(txns);
    }

    // perform upkeep
    function performUpkeep(bytes calldata performData) external override {
        Transaction[] memory txns = abi.decode(performData, (Transaction[]));

        //We highly recommend revalidating the upkeep in the performUpkeep function
        for (uint i = 0; i < txns.length; i++) {
            if (txns[i].status == 1) {
                if (block.timestamp > txns[i].endTime) {
                    address sender = txns[i].sender;
                    address recipient = txns[i].recipient;
                    bytes32 txRef = txns[i].ref;

                    transactions[txRef].status = 3;
                    transactionList[transactions[txRef].listId].status = 3;

                    handleReclaimAsset(txRef, sender, recipient);
                }
            }
        }
    }

    // HELPER FUNCTIONS

    /**
     * @notice logic for generating, populating and storing transaction
     * @param _recipient the recipient
     * @param _asset asset contract address
     * @param _amountOrTokenId asset amount or token id
     * @param _narration narration for the transaction
     * @param _claimCode claim code for the transaction
     * @param _endTime claim expiration time in seconds
     * @param _txType nativeAsset/ erc20 or nft tx type
     */
    function generateTransaction(
        address _recipient,
        address _asset,
        uint256 _amountOrTokenId,
        string memory _narration,
        bytes32 _claimCode,
        uint256 _endTime,
        bool _txType
    ) internal {
        // generate tx unique tx reference
        senderNonce[msg.sender] += 1;
        uint256 nonce = senderNonce[msg.sender];
        bytes32 transactionReference = generateTransactionReference(
            msg.sender,
            nonce
        );

        // populate transaction
        Transaction memory txn = Transaction({
            sender: msg.sender,
            recipient: _recipient,
            asset: _asset,
            amountOrTokenId: _amountOrTokenId,
            narration: _narration,
            status: 1,
            time: block.timestamp,
            claimCode: _claimCode,
            endTime: block.timestamp + _endTime,
            ref: transactionReference,
            txType: _txType,
            listId: listCounter
        });

        listCounter++;

        // store tx
        transactions[transactionReference] = txn;
        transactionList.push(txn);

        // fire event
        emit AssetSent(
            msg.sender,
            getUsername(msg.sender),
            _recipient,
            addressExists[_recipient]
                ? getUsername(_recipient)
                : DEFAULT_USERNAME,
            _asset,
            _amountOrTokenId,
            _narration,
            1,
            transactionReference,
            block.timestamp,
            transactions[transactionReference].txType
        );
    }

    // Helper function to convert address to string
    function addressToString(
        address _address
    ) internal pure returns (string memory) {
        bytes32 _bytes = bytes32(uint256(uint160(_address)));
        bytes memory HEX = "0123456789abcdef";
        bytes memory _string = new bytes(42);
        _string[0] = "0";
        _string[1] = "x";
        for (uint i = 0; i < 20; i++) {
            _string[2 + i * 2] = HEX[uint8(_bytes[i + 12] >> 4)];
            _string[3 + i * 2] = HEX[uint8(_bytes[i + 12] & 0x0f)];
        }
        return string(_string);
    }

    // Helper function to convert uint to string
    function uint2str(
        uint _i
    ) internal pure returns (string memory _uintAsString) {
        if (_i == 0) {
            return "0";
        }
        uint j = _i;
        uint len;
        while (j != 0) {
            len++;
            j /= 10;
        }
        bytes memory bstr = new bytes(len);
        uint k = len - 1;
        while (_i != 0) {
            bstr[k--] = bytes1(uint8(48 + (_i % 10)));
            _i /= 10;
        }
        return string(bstr);
    }

    // generate transcation ref.
    function generateTransactionReference(
        address msgSender,
        uint256 nonce
    ) public pure returns (bytes32) {
        bytes32 txRef = keccak256(abi.encodePacked(msgSender, nonce, SALT));
        return txRef;
    }

    // validate code
    function validateCode(
        string memory _code,
        bytes32 _txRef
    ) internal view returns (bool) {
        bytes32 codeHash = keccak256(bytes(_code));
        if (codeHash == transactions[_txRef].claimCode) {
            return true;
        } else {
            return false;
        }
    }

    // CHECKER FUNCTIONS

    // check handle validity
    function checkHandleValidity(string memory _userName) internal pure {
        bytes memory byteUserName = bytes(_userName);
        if (byteUserName.length == 0 || byteUserName.length > MAX_HANDLE_LENGTH)
            revert("Max Handle Length Exceeded");

        uint256 byteHandleLength = byteUserName.length;
        for (uint256 i = 0; i < byteHandleLength; ) {
            if (
                (byteUserName[i] < "0" ||
                    byteUserName[i] > "z" ||
                    (byteUserName[i] > "9" && byteUserName[i] < "a")) ||
                byteUserName[i] == "." ||
                byteUserName[i] == "-" ||
                byteUserName[i] == "_"
            ) revert("Invalid Characters Used");

            unchecked {
                ++i;
            }
        }

        if (
            keccak256(abi.encodePacked(_userName)) ==
            keccak256(abi.encodePacked("nousername"))
        ) {
            revert("Cant Use Default Username");
        }
    }

    // check handle/address existence
    function checkUserNameAndAddressExistence(
        string memory _userName
    ) internal view {
        if (userNameExistence[_userName] || addressExists[msg.sender]) {
            revert("Username Taken Or Address Already Registered");
        }
    }

    // GETTER FUNCTIONS

    // get username from address
    function getUsername(address _user) public view returns (string memory) {
        return userName[_user];
    }

    // get address from username
    function getAddress(string memory _userName) public view returns (address) {
        return userNameAddress[_userName];
    }

    // get token balance
    function getTokenBalance(
        address _user,
        address _asset
    ) public view returns (uint256) {
        return ERC20(_asset).balanceOf(_user);
    }

    // get transaction
    function getTransaction(
        bytes32 _txRef
    ) public view returns (Transaction memory) {
        return transactions[_txRef];
    }
}
