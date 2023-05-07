from brownie import Angel, accounts, reverts
from web3 import Web3


def test_register_angel_account_reverts_on_max_username_length_exceeded(angel):
    too_long_username = "popopopopopopopopo"
    profile_image = "http://fakeimage.uri/image.jpg"

    with reverts("Max Handle Length Exceeded"):
        angel.registerAngelAccount(
            too_long_username, profile_image, {"from": accounts[9]}
        )


def test_register_angel_account_reverts_on_disallowed_username_characters(angel):
    disallowed_characters = "Popopo-."
    profile_image = "http://fakeimage.uri/image.jpg"

    with reverts("Invalid Characters Used"):
        angel.registerAngelAccount(
            disallowed_characters, profile_image, {"from": accounts[9]}
        )


def test_register_angel_account_reverts_on_existing_username_or_registered_address(
    angel, acct_one
):
    existing_username = "franfran"
    non_existent_username = "dodo"
    profile_image = "http://fakeimage.uri/image.jpg"

    # existent handle
    with reverts("Username Taken Or Address Already Registered"):
        angel.registerAngelAccount(
            existing_username, profile_image, {"from": accounts[9]}
        )

    # existent address
    with reverts("Username Taken Or Address Already Registered"):
        angel.registerAngelAccount(
            non_existent_username, profile_image, {"from": acct_one}
        )


def test_register_angel_account_updates_associated_mappings_correctly(
    angel, acct_one, acct_one_username
):
    # using acct 1 registration
    stored_username = angel.userName(acct_one)
    stored_profile_image = angel.profileImage(acct_one)

    username_existence = angel.userNameExistence(acct_one_username)
    address_existence = angel.addressExists(acct_one)

    assert stored_username == "franfran"
    assert stored_profile_image == "https://fake-image/image.jpg"
    assert username_existence == True
    assert address_existence == True
