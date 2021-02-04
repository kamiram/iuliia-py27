# coding: utf8
"""
Letter mapping for transliteration schema.
"""


class Mapping(object):
    """Letter map for transliteration schema."""

    def __init__(self, mapping):
        self.map = mapping.copy()

    def get(self, key, default=None):
        """Return mapped value for ``key`` if key is in the map, else ``default``."""
        return self.map.get(key, default)

    def __str__(self):
        return str(self.map)

    def __repr__(self):
        return repr(self.map)


class LetterMapping(Mapping):
    """Mapping for individual letters."""

    def __init__(self, mapping):
        super(LetterMapping, self).__init__(mapping)
        upper_map = {key.capitalize(): value.capitalize() for key, value in mapping.items()}
        self.map.update(upper_map)


class PrevMapping(Mapping):
    """Mapping for letters with respect to previous sibling."""

    def __init__(self, mapping):
        super(PrevMapping, self).__init__(mapping)
        upper_map_1 = {key.capitalize(): value for key, value in mapping.items()}
        upper_map_2 = {key.upper(): value.capitalize() for key, value in mapping.items()}
        self.map.update(upper_map_1)
        self.map.update(upper_map_2)


class NextMapping(Mapping):
    """Mapping for letters with respect to next sibling."""

    def __init__(self, mapping):
        super(NextMapping, self).__init__(mapping)
        upper_map_1 = {key.capitalize(): value.capitalize() for key, value in mapping.items()}
        upper_map_2 = {key.upper(): value.capitalize() for key, value in mapping.items()}
        self.map.update(upper_map_1)
        self.map.update(upper_map_2)


class EndingMapping(Mapping):
    """Mapping for word endings."""

    def __init__(self, mapping):
        super(EndingMapping, self).__init__(mapping)
        upper_map = {key.upper(): value.upper() for key, value in mapping.items()}
        self.map.update(upper_map)
