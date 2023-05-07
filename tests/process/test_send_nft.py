from brownie import Angel, accounts, reverts, chain, MockNFT
from web3 import Web3
import math


def test_send_nft_reverts_if_sender_isnt_registered(
    angel, acct_one, acct_two, address_zero, deployer
):
    token_id = 1
    # deploy nft contract andmint token id 1
    mock_nft = MockNFT.deploy({"from": deployer})
    mock_nft.mintFree(token_id, {"from": acct_one})

    # approve
    mock_nft.approve(angel.address, 1, {"from": acct_one})

    asset = mock_nft.address

    narration = "voting reward"
    claim_code = b"pq12g65"
    claim_code_hash = Web3.keccak(claim_code).hex()
    time_limit = 300  # 5 minutes

    with reverts("Sender Has No Username"):
        angel.sendNFT(
            acct_two.address,
            asset,
            token_id,
            narration,
            claim_code_hash,
            time_limit,
            {"from": accounts[9]},
        )


def test_send_nft_deposits_nft_into_the_contract(angel, acct_one, acct_two, deployer):
    token_id = 1
    # deploy nft contract andmint token id 1
    mock_nft = MockNFT.deploy({"from": deployer})
    mock_nft.mintFree(token_id, {"from": acct_one})

    # approve
    mock_nft.approve(angel.address, 1, {"from": acct_one})

    asset = mock_nft.address
    narration = "voting reward"
    claim_code = b"pq12g65"
    claim_code_hash = Web3.keccak(claim_code).hex()
    time_limit = 300  # 5 minutes

    angel.sendNFT(
        acct_two.address,
        asset,
        token_id,
        narration,
        claim_code_hash,
        time_limit,
        {"from": acct_one},
    )

    assert mock_nft.ownerOf(token_id) == angel.address


def test_send_nft_populates_tx_struct_correctly(
    angel, acct_one, acct_two, address_zero, deployer
):
    token_id = 1
    # deploy nft contract andmint token id 1
    mock_nft = MockNFT.deploy({"from": deployer})
    mock_nft.mintFree(token_id, {"from": acct_one})

    # approve
    mock_nft.approve(angel.address, 1, {"from": acct_one})

    asset = mock_nft.address
    narration = "voting reward"
    claim_code = b"pq12g65"
    claim_code_hash = Web3.keccak(claim_code).hex()
    time_limit = 300  # 5 minutes

    tx = angel.sendNFT(
        acct_two.address,
        asset,
        token_id,
        narration,
        claim_code_hash,
        time_limit,
        {"from": acct_one},
    )
    tx.wait(1)

    tx_ref = angel.generateTransactionReference(
        acct_one.address, angel.senderNonce(acct_one.address)
    )

    stored_tx = angel.transactions(tx_ref)

    assert stored_tx[0] == acct_one.address
    assert stored_tx[1] == acct_two.address
    assert stored_tx[2] == asset
    assert stored_tx[3] == token_id
    assert stored_tx[4] == narration
    assert stored_tx[5] == 1
    assert math.isclose(stored_tx[6], chain.time())
    assert stored_tx[7] == claim_code_hash
    assert math.isclose(stored_tx[8], chain.time() + time_limit)
    assert stored_tx[9] == tx_ref
    assert stored_tx[10] == True


def test_send_nft_populates_transaction_list(
    angel, acct_one, acct_two, address_zero, deployer
):
    token_id = 1
    # deploy nft contract andmint token id 1
    mock_nft = MockNFT.deploy({"from": deployer})
    mock_nft.mintFree(token_id, {"from": acct_one})

    # approve
    mock_nft.approve(angel.address, 1, {"from": acct_one})

    asset = mock_nft.address
    narration = "voting reward"
    claim_code = b"pq12g65"
    claim_code_hash = Web3.keccak(claim_code).hex()
    time_limit = 300  # 5 minutes

    tx = angel.sendNFT(
        acct_two.address,
        asset,
        token_id,
        narration,
        claim_code_hash,
        time_limit,
        {"from": acct_one},
    )
    tx.wait(1)

    tx_ref = angel.generateTransactionReference(
        acct_one.address, angel.senderNonce(acct_one.address)
    )

    stored_tx = angel.transactionList(0)

    assert stored_tx[0] == acct_one.address
    assert stored_tx[1] == acct_two.address
    assert stored_tx[2] == asset
    assert stored_tx[3] == token_id
    assert stored_tx[4] == narration
    assert stored_tx[5] == 1
    assert math.isclose(stored_tx[6], chain.time())
    assert stored_tx[7] == claim_code_hash
    assert math.isclose(chain.time() + time_limit, stored_tx[8])
    assert stored_tx[9] == tx_ref
    assert stored_tx[10] == True
