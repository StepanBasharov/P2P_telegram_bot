pay_methods = {
    'EGP': {
        "bank": ["sar", "dcp"],
        "online_wallet": [],
        "world": [],
        "crypto": [],
        "other": []
    },
    'SAR': {
        "bank": [],
        "online_wallet": [],
        "world": [],
        "crypto": [],
        "other": []
    },
    'AED': {
        "bank": [],
        "online_wallet": [],
        "world": [],
        "crypto": [],
        "other": []
    },
    'TRY': {
        "bank": [],
        "online_wallet": [],
        "world": [],
        "crypto": [],
        "other": []
    },
    'RUB': {
        "bank": [],
        "online_wallet": [],
        "world": [],
        "crypto": [],
        "other": []
    },
    'IRR': {
        "bank": [],
        "online_wallet": [],
        "world": [],
        "crypto": [],
        "other": []
    },
    'BRL': {
        "bank": [],
        "online_wallet": [],
        "world": [],
        "crypto": [],
        "other": []
    },
    'VND': {
        "bank": [],
        "online_wallet": [],
        "world": [],
        "crypto": [],
        "other": []
    },
    'CNY': {
        "bank": [],
        "online_wallet": [],
        "world": [],
        "crypto": [],
        "other": []
    },
    'UAH': {
        "bank": [],
        "online_wallet": [],
        "world": [],
        "crypto": [],
        "other": []
    },
    'KZT': {
        "bank": [],
        "online_wallet": [],
        "world": [],
        "crypto": [],
        "other": []
    },
    'USD': {
        "bank": [],
        "online_wallet": [],
        "world": [],
        "crypto": [],
        "other": []
    }
}

def parse_methods():
    all_methods = []
    for i in pay_methods:
        all_methods.extend(i)
        all_methods.extend(i)
        all_methods.extend(i)
        all_methods.extend(i)
        all_methods.extend(i)
    return all_methods
print(parse_methods())