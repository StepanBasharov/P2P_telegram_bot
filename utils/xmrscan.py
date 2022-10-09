import requests

from config.xmrkey import XMR_KEY
from config.addreses import XMR_address

def xmr_hash_scaner(hash):
    try:
        res = requests.get(f'https://api.blockchair.com/monero/raw/outputs?txprove=0&txhash={hash}&address={XMR_address}&viewkey={XMR_KEY}').json()
        try:
            amount = res['data']['outputs']
            return float(amount[1]['amount']) / 1000000000000
        except:
            return False
    except:
        return False

