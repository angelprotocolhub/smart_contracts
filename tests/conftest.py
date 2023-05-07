import pytest
from web3 import Web3


mock_channel_address = "0x5F7FbE4bf8987FA77Ec6C22FD3f3d558B3b68D4e"
mock_image = "https://fake-image/image.jpg"


@pytest.fixture
def angel(accounts, Angel, MockPushComm):
    deployer = accounts[0]

    acct_one = accounts[1]
    acct_one_username = "franfran"

    acct_two = accounts[2]
    acct_two_username = "beamer"

    # deploy mock push comm contract
    mock_push_comm = MockPushComm.deploy({"from": deployer})

    # deploy angel contract
    angel_contract = Angel.deploy(
        mock_push_comm.address, mock_channel_address, {"from": deployer}
    )

    # register accounts
    tx_one = angel_contract.registerAngelAccount(
        acct_one_username, mock_image, {"from": acct_one}
    )
    tx_one.wait(1)

    tx_two = angel_contract.registerAngelAccount(
        acct_two_username, mock_image, {"from": acct_two}
    )
    tx_two.wait(1)

    return angel_contract


@pytest.fixture
def angel_claim_funds(
    angel, MockNFT, MockToken, acct_one, acct_two, address_zero, deployer
):
    # SEND NATIVE ASSET
    asset = address_zero
    amount = Web3.toWei(1, "ether")
    narration = "voting reward"

    claim_code_hash = Web3.keccak(b"popo25fat2")
    time_limit = 300  # 5 minutes

    angel.sendCrypto(
        acct_two.address,
        asset,
        amount,
        narration,
        claim_code_hash,
        time_limit,
        {"from": acct_one, "value": amount},
    )

    # SEND ERC20

    # deploy mock token
    mock_token = MockToken.deploy({"from": deployer})

    # params
    asset = mock_token.address
    amount = Web3.toWei(1, "ether")
    narration = "voting reward"
    claim_code_hash = Web3.keccak(b"oprahbacnk")
    time_limit = 1000  # 5 minutes

    # mint and approve token
    mock_token.mintFree(amount, {"from": acct_two})
    mock_token.approve(angel, amount, {"from": acct_two})

    angel.sendCrypto(
        acct_one.address,
        asset,
        amount,
        narration,
        claim_code_hash,
        time_limit,
        {"from": acct_two, "value": amount},
    )

    # SEND NFT

    token_id = 1
    # deploy nft contract andmint token id 1
    mock_nft = MockNFT.deploy({"from": deployer})
    mock_nft.mintFree(token_id, {"from": acct_one})

    # approve
    mock_nft.approve(angel.address, 1, {"from": acct_one})

    asset = mock_nft.address
    narration = "voting reward"
    claim_code_hash = Web3.keccak(b"pq12g65")
    time_limit = 300  # 5 minutes

    tx_nft = angel.sendNFT(
        acct_two.address,
        asset,
        token_id,
        narration,
        claim_code_hash,
        time_limit,
        {"from": acct_one},
    )
    tx_nft.wait(1)

    native_asset_tx_hash = angel.generateTransactionReference(
        acct_one.address, angel.senderNonce(acct_one.address) - 1
    )

    erc20_tx_hash = angel.generateTransactionReference(
        acct_two.address, angel.senderNonce(acct_two.address)
    )

    nft_tx_hash = angel.generateTransactionReference(
        acct_one.address, angel.senderNonce(acct_one.address)
    )

    return angel, native_asset_tx_hash, erc20_tx_hash, nft_tx_hash


# Vars


@pytest.fixture
def deployer(accounts):
    return accounts[0]


@pytest.fixture
def acct_one(accounts):
    return accounts[1]


@pytest.fixture
def acct_two(accounts):
    return accounts[2]


@pytest.fixture
def acct_one_username():
    return "franfran"


@pytest.fixture
def acct_two_username():
    return "beamer"


@pytest.fixture
def address_zero():
    return "0x0000000000000000000000000000000000000000"


@pytest.fixture
def perform_upkeep_data():
    return "0x00000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000001e000000000000000000000000033a4622b82d4c04a53e170c638b944ce27cffce30000000000000000000000000063046686e46dc6f15918b61ae2b121458534a500000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000de0b6b3a764000000000000000000000000000000000000000000000000000000000000000001600000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000006443938125d074eaa4e592e783847562380e05ed77ad0ccf99ab017dd6cfb77bda97bd7b00000000000000000000000000000000000000000000000000000000644394ad593c59a362f255a7ff44ed3ba98acd3ee78e0391ab79872c422289a38dd6937a0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000d766f74696e67207265776172640000000000000000000000000000000000000000000000000000000000000033a4622b82d4c04a53e170c638b944ce27cffce30000000000000000000000000063046686e46dc6f15918b61ae2b121458534a50000000000000000000000009e4c14403d7d9a8a782044e86a93cae09d7b2ac90000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000016000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000064439381cc359445a1b3b9fd6139b2136831c0126bdf08e053a2217eaa3dda2462e02b6f00000000000000000000000000000000000000000000000000000000644394adb711e9daea1899612fbd9506c78659e37b515ff3fc43010d5d0a36eaf1a251e30000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000d766f74696e672072657761726400000000000000000000000000000000000000"
