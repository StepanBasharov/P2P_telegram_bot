import requests


def tron_hash_scaner(hash, wallet):
    try:
        resp = requests.get(f"https://apilist.tronscanapi.com/api/transaction-info?hash={hash}")
        amount = resp.json()['tokenTransferInfo']['amount_str']

        if resp.json()['tokenTransferInfo']['to_address'] == wallet:
            return float(amount) / 1000000
        else:
            return False
    except:

        return False
