from brownie import Angel, accounts, reverts, chain
from web3 import Web3
import math


def test_send_crypto_reverts_if_sender_isnt_registered(angel, acct_two, address_zero):
    asset = address_zero
    amount = Web3.toWei(1, "ether")
    narration = "voting reward"

    claim_code = "pq12g65"
    claim_code_hash = Web3.keccak(text=claim_code)
    time_limit = 300  # 5 minutes

    with reverts("Sender Has No Username"):
        angel.sendCrypto(
            acct_two.address,
            asset,
            amount,
            narration,
            claim_code_hash,
            time_limit,
            {"from": accounts[9]},
        )


def test_send_crypto_deposits_native_asset_into_the_contract(
    angel, acct_one, acct_two, address_zero
):
    asset = address_zero
    amount = Web3.toWei(0.0001, "ether")
    narration = "voting reward"

    angel_prev_bal = angel.balance()

    claim_code = "pq12g65"
    claim_code_hash = Web3.keccak(text=claim_code)
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

    assert angel.balance() == angel_prev_bal + amount


def test_send_crypto_deposits_erc20_asset_into_the_contract(
    angel, MockToken, acct_one, acct_two, deployer, address_zero
):
    # deploy mock token
    mock_token = MockToken.deploy({"from": deployer})
    angel_prev_bal = mock_token.balanceOf(angel)

    # params
    asset = mock_token.address
    amount = Web3.toWei(1, "ether")
    narration = "voting reward"
    claim_code = "pq12g65"
    claim_code_hash = Web3.keccak(text=claim_code)
    time_limit = 300  # 5 minutes

    # mint and approve token
    mock_token.mintFree(amount, {"from": acct_one})
    mock_token.approve(angel, amount, {"from": acct_one})

    angel.sendCrypto(
        acct_two.address,
        asset,
        amount,
        narration,
        claim_code_hash,
        time_limit,
        {"from": acct_one, "value": amount},
    )

    assert mock_token.balanceOf(angel) == angel_prev_bal + amount


def test_send_crypto_populates_tx_struct_correctly(
    angel, acct_one, acct_two, address_zero
):
    asset = address_zero
    amount = Web3.toWei(1, "ether")
    narration = "voting reward"
    claim_code = b"pq12g65"
    claim_code_hash = Web3.keccak(claim_code).hex()
    time_limit = 300  # 5 minutes

    tx = angel.sendCrypto(
        acct_two.address,
        asset,
        amount,
        narration,
        claim_code_hash,
        time_limit,
        {"from": acct_one, "value": amount},
    )
    tx.wait(1)

    tx_ref = angel.generateTransactionReference(
        acct_one.address, angel.senderNonce(acct_one.address)
    )

    stored_tx = angel.transactions(tx_ref)

    assert stored_tx[0] == acct_one.address
    assert stored_tx[1] == acct_two.address
    assert stored_tx[2] == address_zero
    assert stored_tx[3] == amount
    assert stored_tx[4] == narration
    assert stored_tx[5] == 1
    assert math.isclose(stored_tx[6], chain.time())
    assert stored_tx[7] == claim_code_hash
    assert stored_tx[8] == chain.time() + time_limit
    assert stored_tx[9] == tx_ref
    assert stored_tx[10] == False


def test_send_crypto_populates_transaction_list(
    angel, acct_one, acct_two, address_zero
):
    asset = address_zero
    amount = Web3.toWei(1, "ether")
    narration = "voting reward"
    claim_code = "pq12g65"
    claim_code_hash = Web3.keccak(text=claim_code).hex()
    time_limit = 300  # 5 minutes

    tx = angel.sendCrypto(
        acct_two.address,
        asset,
        amount,
        narration,
        claim_code_hash,
        time_limit,
        {"from": acct_one, "value": amount},
    )
    tx.wait(1)

    tx_ref = angel.generateTransactionReference(
        acct_one.address, angel.senderNonce(acct_one.address)
    )

    stored_tx = angel.transactionList(0)

    assert stored_tx[0] == acct_one.address
    assert stored_tx[1] == acct_two.address
    assert stored_tx[2] == address_zero
    assert stored_tx[3] == amount
    assert stored_tx[4] == narration
    assert stored_tx[5] == 1
    assert math.isclose(stored_tx[6], chain.time())
    assert stored_tx[7] == claim_code_hash
    assert stored_tx[8] == chain.time() + time_limit
    assert stored_tx[9] == tx_ref
    assert stored_tx[10] == False
