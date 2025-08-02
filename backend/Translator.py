from googletrans import Translator

translator = Translator()

def translate_text(text, target_lang="English"):
    lang_map = {
        "English": "en",
        "Hindi": "hi",
        "Telugu": "te",
        "Tamil": "ta",
        "Kannada": "kn"
    }
    target_code = lang_map.get(target_lang, "en")
    translated = translator.translate(text, dest=target_code)
    return translated.text
