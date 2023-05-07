from brownie import reverts, chain
from web3 import Web3
from eth_abi import encode


def test_automated_reversal_return_false_when_a_reversal_does_not_exists(
    angel_claim_funds, acct_one, acct_two
):
    angel, native_tx_hash, erc20_tx_hash, nft_tx_hash = angel_claim_funds

    # check up keep
    (valid, upkeeps) = angel.checkUpkeep(b"")

    assert valid == False


def test_automated_reversal_return_true_when_a_reversal_exists(
    angel_claim_funds, acct_one, acct_two
):
    angel, native_tx_hash, erc20_tx_hash, nft_tx_hash = angel_claim_funds

    # time travel
    chain.sleep(500)
    chain.mine(1)

    # check up keep
    valid, upkeeps = angel.checkUpkeep(b"")

    assert valid == True


def test_perform_upkeep_refunds_the_neccessary_txs(
    angel_claim_funds,
    acct_one,
    acct_two,
    perform_upkeep_data,
    deployer,
    MockNFT,
    MockToken,
):
    angel, native_tx_hash, erc20_tx_hash, nft_tx_hash = angel_claim_funds

    # time travel
    chain.sleep(500)
    chain.mine(1)

    token_id = 1

    initial_balance = acct_one.balance()

    tx_upkeep = angel.performUpkeep(perform_upkeep_data, {"from": deployer})
    tx_upkeep.wait(1)

    # refunds the native asset
    assert acct_one.balance() == initial_balance + Web3.toWei(1, "ether")

    # check the erc20 wasnt refunded
    assert MockToken[-1].balanceOf(angel.address) == Web3.toWei(1, "ether")

    # refunds the nft
    assert MockNFT[-1].ownerOf(token_id) == acct_one
