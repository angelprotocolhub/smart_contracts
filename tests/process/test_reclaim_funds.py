from brownie import reverts, chain
from web3 import Web3


def test_reclaim_funds_reverts_if_transaction_is_not_pending(
    angel_claim_funds, acct_one, acct_two, accounts
):
    angel, native_tx_hash, erc20_tx_hash, nft_tx_hash = angel_claim_funds
    native_tx_claim_code = "popo25fat2"

    angel.claimFunds(native_tx_hash, native_tx_claim_code, {"from": acct_two})

    with reverts("Transaction Not Pending"):
        angel.reclaimFunds(native_tx_hash, {"from": acct_one})


def test_reclaim_funds_reverts_if_caller_isnt_tx_sender(
    angel_claim_funds, acct_one, acct_two, accounts
):
    angel, native_tx_hash, erc20_tx_hash, nft_tx_hash = angel_claim_funds

    with reverts("Msg Sender Isnt Tx Sender"):
        angel.reclaimFunds(native_tx_hash, {"from": acct_two})


def test_reclaim_funds_returns_native_asset(
    angel_claim_funds, acct_one, acct_two, accounts
):
    angel, native_tx_hash, erc20_tx_hash, nft_tx_hash = angel_claim_funds

    acct_one_initial_balance = acct_one.balance()

    angel.reclaimFunds(native_tx_hash, {"from": acct_one})

    assert acct_one.balance() == acct_one_initial_balance + Web3.toWei(1, "ether")


def test_reclaim_funds_returns_erc20_asset(
    angel_claim_funds, acct_one, acct_two, accounts, MockToken
):
    angel, native_tx_hash, erc20_tx_hash, nft_tx_hash = angel_claim_funds

    acct_two_initial_balance = MockToken[-1].balanceOf(acct_one.address)

    angel.reclaimFunds(erc20_tx_hash, {"from": acct_two})

    assert MockToken[-1].balanceOf(
        acct_two.address
    ) == acct_two_initial_balance + Web3.toWei(1, "ether")


def test_reclaim_funds_returns_nft(
    angel_claim_funds, acct_one, acct_two, accounts, MockNFT
):
    angel, native_tx_hash, erc20_tx_hash, nft_tx_hash = angel_claim_funds

    token_id = 1
    token_id_owner = MockNFT[-1].ownerOf(token_id)

    angel.reclaimFunds(nft_tx_hash, {"from": acct_one})

    assert MockNFT[-1].ownerOf(token_id) == acct_one.address
