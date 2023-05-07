from brownie import reverts, chain
from web3 import Web3


def test_add_to_beneficiaries_reverts_if_caller_isnt_registered(
    angel_claim_funds, acct_one, acct_two, accounts
):
    angel, native_tx_hash, erc20_tx_hash, nft_tx_hash = angel_claim_funds

    with reverts("Sender Has No Username"):
        angel.addToBeneficiaries(acct_two, {"from": accounts[9]})


def test_add_to_beneficiaries_reverts_if_beneficiary_isnt_registered(
    angel_claim_funds, acct_one, acct_two, accounts
):
    angel, native_tx_hash, erc20_tx_hash, nft_tx_hash = angel_claim_funds

    with reverts("Recipient Has No Username"):
        angel.addToBeneficiaries(accounts[9], {"from": acct_one})


def test_add_to_beneficiaries_updates_beneficiary_mapping(
    angel_claim_funds, acct_one, acct_two, accounts
):
    angel, native_tx_hash, erc20_tx_hash, nft_tx_hash = angel_claim_funds

    angel.addToBeneficiaries(acct_two, {"from": acct_one})

    assert angel.beneficaries(acct_one, acct_two) == True
