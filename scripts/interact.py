from brownie import Angel, accounts, MockLiveToken, Unrelated
from web3 import Web3

zero_address = "0x0000000000000000000000000000000000000000"


def register_account():
    acct = accounts.load("test-1")
    acct_two = accounts.load("test-2")

    angel = Angel[-1]

    username = "franfran"
    image_uri = "https://bafybeib3faghcn66ax5o5enqk3vfzp23senitu5vlbjh4ceus5fhmyskpe.ipfs.w3s.link/adventure%20time%204.jpg"

    tx_register_one = angel.registerAngelAccount(username, image_uri, {"from": acct})
    tx_register_one.wait(1)

    username = "genevarock"
    image_uri = "https://bafybeib3faghcn66ax5o5enqk3vfzp23senitu5vlbjh4ceus5fhmyskpe.ipfs.w3s.link/adventure%20time%204.jpg"

    tx_register = angel.registerAngelAccount(username, image_uri, {"from": acct_two})
    tx_register.wait(1)


def send_crypto():
    acct = accounts.load("test-1")
    acct_two = accounts.load("test-2")

    angel = Angel[-1]

    recipient = acct_two.address
    asset = zero_address
    amount = Web3.toWei(0.0000123, "ether")
    narration = "seasons greetings"
    claim_code = Web3.keccak(text="claimcode0030").hex()
    end_time = 30

    print("initiating second tx...")
    tx = angel.sendCrypto(
        recipient,
        asset,
        amount,
        narration,
        claim_code,
        end_time,
        {"from": acct, "value": amount},
    )
    tx.wait(1)

    print("Initiated!")


def send_nft():
    acct = accounts.load("test-1")
    acct_two = accounts.load("test-2")

    angel = Angel[-1]

    recipient = acct.address
    asset = Unrelated[-1].address
    token_id = 1
    narration = "happy birthday. I love you!"
    claim_code = Web3.keccak(text="claimcode0050").hex()
    end_time = 1800

    print("initiating second tx...")

    approve_tx = Unrelated[-1].approve(angel.address, token_id, {"from": acct_two})
    approve_tx.wait(1)

    tx = angel.sendNFT(
        recipient,
        asset,
        token_id,
        narration,
        claim_code,
        end_time,
        {
            "from": acct_two,
        },
    )
    tx.wait(1)

    print("Initiated!")


def claim_nft():
    # acct = accounts.load("test-1")
    acct_two = accounts.load("test-2")

    angel = Angel[-1]

    # tx details
    tx_ref = "0x2449cb8e48e8ceabee35286e7afad3f6fa62b633d7027826503d05976059062d"
    claim_code = "claimcode0050"

    print("initiating second tx...")
    tx = angel.claimFunds(
        tx_ref,
        claim_code,
        {"from": acct_two},
    )
    tx.wait(1)

    print("Initiated!")


def claim_crypto():
    acct = accounts.load("test-1")
    # acct_two = accounts.load("test-2")

    angel = Angel[-1]

    # tx details
    tx_ref = "0x8e24557ac44cc7dae2257ab2e7ab05714f28110460df0a841f10173615d48674"
    claim_code = "claimcode0030"

    print("initiating second tx...")
    tx = angel.claimFunds(
        tx_ref,
        claim_code,
        {"from": acct},
    )
    tx.wait(1)

    print("Initiated!")


def reclaim_crypto():
    acct = accounts.load("test-1")
    # acct_two = accounts.load("test-2")

    angel = Angel[-1]

    # tx details
    tx_ref = "0xf942a7f072f6dac372a8c8f3caf6c261b78ebe7627c0f5b1cf5ab5f06956c748"

    print("initiating second tx...")
    tx = angel.reclaimFunds(
        tx_ref,
        {"from": acct},
    )
    tx.wait(1)

    print("Initiated!")


def get_contract_balance():
    print(Angel[-1].balance())


def get_username():
    acct_two = accounts.load("test-2")
    print(Angel[-1].getUsername(acct_two.address))


def print_code_hash():
    print(Web3.keccak(text="hello").hex())


def deploy_or_set_token_uri():
    account = accounts.load("test-1")
    unrelated_nfts = Unrelated.deploy(
        "Unrelated",
        "URTD",
        "https://arweave.net/i2UasvWWr_eFHYmOXU2yp3JYVn4WHIS9UxJqHit697w/",
        {"from": account},
    )


def mint():
    account = accounts.load("test-1")
    unrelated_nfts = Unrelated[-1]
    tx_mint = unrelated_nfts.mint(7, {"from": account})
    tx_mint.wait(1)


def add_to_beneficiaries():
    acct = accounts.load("test-1")
    acct_two = accounts.load("test-2")

    angel = Angel[-1]
    beneficiary = acct.address

    tx = angel.addToBeneficiaries(beneficiary, {"from": acct_two})


def check_upkeep():
    angel = Angel[-1]

    valid, data = angel.checkUpkeep(b"")

    print(data)
    print("Upkeep Needed ", valid)


def main():
    send_crypto()
