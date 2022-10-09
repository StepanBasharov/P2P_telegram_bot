from translate import Translator

def translator(string, from_lang, to_lang):
    translator = Translator(from_lang=from_lang, to_lang=to_lang)
    translation = translator.translate(string)
    return translation

print(f'{translator("Введите сумму отправки: ", "russian", "english")}\n{translator("Введите сумму отправки: ", "russian", "english")}')

