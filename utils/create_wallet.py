from bitcoinlib.wallets import Wallet

w = Wallet.create('Wallet123')
key1 = w.get_key()
print(key1.account_id)