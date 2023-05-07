from brownie import Angel, accounts, MockLiveToken


def deploy():
    acct = accounts.load("test-1")

    comm_address = "0xb3971BCef2D791bc4027BbfedFb47319A4AAaaAa"
    channel_address = "0x5F7FbE4bf8987FA77Ec6C22FD3f3d558B3b68D4e"

    print("Deploying Angel Protocol...")
    Angel.deploy(
        comm_address,
        channel_address,
        {"from": acct, "required_confs": 6},
        publish_source=True,
    )

    print("Protocol Deployed!")


def deploy_mock_tokens():
    acct = accounts.load("test-1")

    print("Deploying Mock SAND Token....")
    sand_token = MockLiveToken.deploy("SAND", "SND", {"from": acct})
    print(f"Deployed Mock SAND to: {sand_token.address}")

    print("Deploying Mock USDT Token....")
    usdt_token = MockLiveToken.deploy("USDT", "USDT", {"from": acct})
    print(f"Deployed Mock USDT to: {usdt_token.address}")

    print("Deploying Mock LINK Token....")
    link_token = MockLiveToken.deploy("LINK", "LINK", {"from": acct})
    print(f"Deployed Mock LINK to: {link_token.address}")

    print("Deploying Mock ANGEL Token....")
    angel_token = MockLiveToken.deploy("ANGEL", "ANG", {"from": acct})
    print(f"Deployed Mock ANGEL to: {angel_token.address}")

    print("Deploying Mock DAI Token....")
    dai_token = MockLiveToken.deploy("DAI", "DAI", {"from": acct})
    print(f"Deployed Mock DAI to: {dai_token.address}")


def check_current_address():
    print(Angel[-1].address)


def verify_contract():
    angel = Angel.at("0x68876bcabd609dBDf92573616007AC3a95e46788")
    Angel.publish_source(angel)


def main():
    verify_contract()


# LIVE CONTRACT - 0x68876bcabd609dBDf92573616007AC3a95e46788


# MOCK LIVE TOKENS
# SAND - 0xc9A6E60B894e41574F93023f3C6DD8Caf4Ae4fe2
# USDT - 0xd3BFA2c17E98274aa86BbeA183a5b12562f689C4
# LINK - 0xfD86305830e490B188C3C5e3B02baE346F930dDa
# ANGEL - 0xe3088919A826125aF0DaF96Cf74dca3583550BB6
# DAI - 0x9F192326C0C17b9F4E5F9A428cC958b887397f08
