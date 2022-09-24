"""

███╗   ███╗ █████╗ ██╗
████╗ ████║██╔══██╗██║
██╔████╔██║███████║██║
██║╚██╔╝██║██╔══██║██║
██║ ╚═╝ ██║██║  ██║██║
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝

Made With ❤️ By Ghoul & Nerd

"""

import json

from pycord18n.language import Language

FRENCH: Language = Language(
    "French", "fr", json.load(open("locales/fr_FR/fr.json", encoding="UTF-8"))
)
SPANISH: Language = Language(
    "Spanish", "es", json.load(open("locales/es_ES/es.json", encoding="UTF-8"))
)
ENGLISH: Language = Language(
    "English", "en", json.load(open("locales/en_US/en.json", encoding="UTF-8"))
)
JAPANESE: Language = Language(
    "Japanese", "ja", json.load(open("locales/ja_JP/ja.json", encoding="UTF-8"))
)
GERMAN: Language = Language(
    "German", "de", json.load(open("locales/de_DE/de.json", encoding="UTF-8"))
)
KOREAN: Language = Language(
    "Korean", "ko", json.load(open("locales/ko_KO/ko.json", encoding="UTF-8"))
)
TURKISH: Language = Language(
    "Turkish", "tr", json.load(open("locales/tr_TR/tr.json", encoding="UTF-8"))
)
RUSSIAN: Language = Language(
    "Russian", "ru", json.load(open("locales/ru_RU/ru.json", encoding="UTF-8"))
)
