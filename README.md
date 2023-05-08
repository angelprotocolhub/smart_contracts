# Angel Protocol

- The smart contracts for angel protocol.
  Link to smart contrcats - https://github.com/angelprotocolhub/smart_contracts

- The frontend application for angel protocol
  Link to front end - https://github.com/angelprotocolhub/frontend

- The subgraoh for angel protocol
  Link to subgraph - https://github.com/angelprotocolhub/subgraph

- The Documentation Page
  Link to Docs - https://francis-4.gitbook.io/angel-protocol/

- The Live Demo Site
  Link to Site - https://main--fantastic-froyo-63d537.netlify.app/

# **CORE CONCEPTS**

## **Claim Codes**

When one person sends cryptocurrency to another. Being a smart contract for escrow. Angel Protocol retains these assets and distributes them only to the specified recipient.

When transmitting the asset, the sender must include the hash of the claim code that the recipient will use to unlock the funds in the transaction. It is up to both parties how the sender communicates the claim code to the recipient. Consider the following example where claim codes could be useful.

- John sends Angela 5 Matic via angel protocol
- Angela Receives the notification on her push inbox or mobile app.
- For one reason or another Angela's wallet gets compromised.
  T- he attacker wont be able to claim the funds sent to - Angela without knowing the claim code.
- This in turn reduces the loss of funds overall incase of a wallet compromise.

  ## Another scenario would be sending to the wrong address.

- John means to send some tokens he just deployed to Angela.
- While transferring the asset he makes a mistake with the address.
- Assuming the address he sends the asset to is a wallet address who uses Angel Protocol too.
- The user can easily claim these funds even though it wan an unintended transaction.

  Claim codes allow for personal distribution of the code drafted by the sender to his intended recipient before the transaction was ever executed.
  Meaning in this case the unintended user cannot claim those funds and they get reversed back to John.
  All Smiles!

When a user sends an asset we store the hash of the claim code in the contract not the code itself. Then we validate it against the pure code the recipient sends. Its advisable for a sender to never use the same claim code he used for a previous sender.

## **Automatic Reversals**

Angel Protocol provides automatic reversal for unclaimed transactions after a specified period of time. This is very beneficial when you accidentally transfer money to the wrong address. Chainlink Automation handles automatic reversals.

When you send a transaction, you are prompted to indicate a time range for reversal.

Consider this example.

- John wants to send Angela some LINK and Angela mistakenly sends him the wrong address.
- John sends the LINK via our protocol with a reclaim time of 24 hours.
- John realizes that he's sent his LINK to the wrong address and even Angela cant claim the asset.
- Because John used Angel Protocol, he has the option of manually reclaiming his LINK from his transaction history or allowing the 24 hour time he selected to pass and allowing Angel Protocol to automatically reverse his LINK. Simply because the recipient did not claim it within the time frame he established due to not possessing the claim code or not being a contract address.

## **Push Protocol Notifications**

Whenever an angel protocol transaction occurs, depending on the type of transaction, alerts are issued to either the recipient or the sender. When an asset is sent, claimed, or reclaimed, notifications are sent.

To maintain the notification system within the world of blockchains and wallet addresses, we manage serving our notifications using push protocol. You are also requested to opt in to our push protocol channel by signing a message while registering for an angel name (we'll get to angel names soon).
Push protocol sends a notification directly from the smart contract to your mailbox, which you can access by connecting or inputting your wallet address in the push online application or mobile application. The following is a list of the alerts we send.

- When an NFT, ERC20, or Native Asset is received, we notify the recipient.
- When the recipient successfully claims the asset sent to them, we notify the sender.
- Finally, we notify the recipient when an unclaimed asset sent to them is reclaimed.

Learn more about Push Protocol [here](https://docs.push.org/developers/developer-guides/receiving-notifications/receiving-notifications-via-dapp)

## **Support For Any Asset including NFTs**

Except for the assets displayed on our application. Users can manually enter the contract addresses of the tokens they want to send into our application and send them while still receiving all of our escrow benefits.
We also support ERC721 NFT contracts, which provide the same level of security or satisfaction for NFT transfers.

## **Angel Names**

Angel names enable the concept of tagged addresses, each of which represents a distinct username. Overall, this reduces the need for users to go through the trouble of copy-pasting wallet addresses and instead provides them with a better and more user-friendly option.

By simply tying their address to a username, individuals no longer have to worry about copying and pasting addresses and can instead quickly communicate their angel names.

- Having to go from `0x68876bcabd609dBDf92573616007AC3a95e46788` to `francis.angel`

## **User Friendly Interface**

We developed Angel Protocol to be as user-friendly as possible, allowing users to access features similar to those found in other applications while maintaining the escrow nature of the smart contract. Angel Protocol thinks that having a user-friendly user interface puts us one step closer to eliminating all of the processes associated with repeating a process for transferring assets which in turn leads to lesser mistakes.

### Some of our app's cool features include...

- Live transaction Checker
- Transaction History
- Transaction Status
- Claims section
- Beneficiaries for repeating Transactions
- No Limited support for assets.
- Sending assets to regular addresses and angel names
