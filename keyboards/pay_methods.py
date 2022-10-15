import json


def choose_pay_method_from_json(fiat, method):
    with open("keyboards/pay_methods.json", "r") as f:
        data = json.loads(f.read())
    return data[fiat][method]


def add_methods_to_json(fiat, methods, method):
    with open("keyboards/pay_methods.json", "r") as f:
        data = json.loads(f.read())
    new_method = data[fiat][methods]
    new_method.append(method)
    data[fiat][methods] = new_method
    with open("keyboards/pay_methods.json", "w", encoding='utf-8') as f:
        json.dump(data, f, indent=4)


def check_all_data():
    with open("keyboards/pay_methods.json", "r") as f:
        data = json.loads(f.read())
    main_list = []
    for i in data:
        for j in data[i]:
            main_list.extend(data[i][j])
    return list(set(main_list))


def check_all_data_order():
    with open("keyboards/pay_methods.json", "r") as f:
        data = json.loads(f.read())
    main_list = []
    for i in data:
        for j in data[i]:
            data_order = [k + "_order" for k in data[i][j]]
            main_list.extend(data_order)
    return list(set(main_list))
