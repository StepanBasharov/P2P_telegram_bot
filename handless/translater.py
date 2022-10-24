import json
from database.settingsdb import check_lang

def get_json_text(type_text, message_text, user_id):
    with open("handless/text.json", "r", encoding='utf-8') as f:
        data = json.loads(f.read())
        return data[type_text][message_text][f"text_{check_lang(user_id)}"]