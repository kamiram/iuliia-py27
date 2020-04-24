"""
UNGEGN 1987 V/18 transliteration schema.
https://dangry.ru/iuliia/ungegn-1987/
"""

from iuliia.mapping import BASE_MAPPING
from iuliia.schema import Schema

MAPPING = {
    **BASE_MAPPING,
    **{
        "ё": "ё",
        "ж": "ž",
        "й": "j",
        "х": "h",
        "ц": "c",
        "ч": "č",
        "ш": "š",
        "щ": "šč",
        "ъ": "ʺ",
        "ы": "y",
        "ь": "ʹ",
        "э": "è",
        "ю": "ju",
        "я": "ja",
    },
}

UNGEGN_1987 = Schema(MAPPING)