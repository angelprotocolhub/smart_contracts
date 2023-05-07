from brownie import reverts, chain
from web3 import Web3


native_tx_claim_code = "popo25fat2"
erc20_tx_claim_code = "oprahbacnk"
nft_tx_claim_code = "pq12g65"


def test_claim_funds_reverts_if_claimer_isnt_regsitered(
    angel_claim_funds, acct_one, acct_two, accounts
):
    angel, native_tx_hash, erc20_tx_hash, nft_tx_hash = angel_claim_funds

    with reverts("Sender Has No Username"):
        angel.claimFunds(native_tx_hash, native_tx_claim_code, {"from": accounts[9]})


def test_claim_funds_reverts_if_transaction_is_not_pendinng(
    angel_claim_funds, acct_one, acct_two, accounts
):
    angel, native_tx_hash, erc20_tx_hash, nft_tx_hash = angel_claim_funds

    tx_reclaim = angel.reclaimFunds(native_tx_hash, {"from": acct_one})
    tx_reclaim.wait(1)

    with reverts("Transaction !Pending State"):
        angel.claimFunds(native_tx_hash, native_tx_claim_code, {"from": acct_two})


def test_claim_funds_reverts_if_caller_isnt_recipient(
    angel_claim_funds, acct_one, acct_two, accounts
):
    angel, native_tx_hash, erc20_tx_hash, nft_tx_hash = angel_claim_funds

    with reverts("Sender Isnt Recipient"):
        angel.claimFunds(native_tx_hash, native_tx_claim_code, {"from": acct_one})


def test_claim_funds_reverts_if_claim_time_is_over(
    angel_claim_funds, acct_one, acct_two, accounts
):
    angel, native_tx_hash, erc20_tx_hash, nft_tx_hash = angel_claim_funds

    claim_time = 300  # 5 mins

    # time traveling
    chain.sleep(claim_time + 20)

    with reverts("Claim Time Is Over"):
        angel.claimFunds(native_tx_hash, native_tx_claim_code, {"from": acct_two})


def test_claim_funds_reverts_on_incorrect_claim_code(
    angel_claim_funds, acct_one, acct_two, accounts
):
    angel, native_tx_hash, erc20_tx_hash, nft_tx_hash = angel_claim_funds

    incorrect_claim_code = "incorrect123baby"

    with reverts("Incorrect Claim Code"):
        angel.claimFunds(native_tx_hash, incorrect_claim_code, {"from": acct_two})


def test_claim_funds_sets_the_tx_status_to_claimed(
    angel_claim_funds, acct_one, acct_two, accounts
):
    angel, native_tx_hash, erc20_tx_hash, nft_tx_hash = angel_claim_funds

    angel.claimFunds(native_tx_hash, native_tx_claim_code, {"from": acct_two})

    stored_tx_status = angel.transactions(native_tx_hash)[5]

    assert stored_tx_status == 2


def test_claim_funds_sends_recipient_native_asset(
    angel_claim_funds, acct_one, acct_two, accounts
):
    angel, native_tx_hash, erc20_tx_hash, nft_tx_hash = angel_claim_funds

    acct_two_initial_balance = acct_two.balance()

    angel.claimFunds(native_tx_hash, native_tx_claim_code, {"from": acct_two})

    assert acct_two.balance() == acct_two_initial_balance + Web3.toWei(1, "ether")


def test_claim_funds_sends_recipient_erc20_asset(
    angel_claim_funds, acct_one, acct_two, accounts, MockToken
):
    angel, native_tx_hash, erc20_tx_hash, nft_tx_hash = angel_claim_funds

    acct_one_initial_balance = MockToken[-1].balanceOf(acct_one.address)

    angel.claimFunds(erc20_tx_hash, erc20_tx_claim_code, {"from": acct_one})

    assert MockToken[-1].balanceOf(
        acct_one.address
    ) == acct_one_initial_balance + Web3.toWei(1, "ether")


def test_claim_funds_sends_recipient_nft(
    angel_claim_funds, acct_one, acct_two, accounts, MockNFT
):
    angel, native_tx_hash, erc20_tx_hash, nft_tx_hash = angel_claim_funds
    token_id = 1

    token_id_owner = MockNFT[-1].ownerOf(token_id)

    angel.claimFunds(nft_tx_hash, nft_tx_claim_code, {"from": acct_two})

    assert MockNFT[-1].ownerOf(token_id) == acct_two.address
