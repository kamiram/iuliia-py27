# coding: utf8
"""
Transliteration schema base features.
"""

from .mapping import LetterMapping, PrevMapping, NextMapping, EndingMapping


class Schema(object):
    """
    Transliteration schema. Defines the way to translate individual letters.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        name,
        mapping,
        prev_mapping = None,
        next_mapping = None,
        ending_mapping = None,
        samples = None,
        description = None,
    ):
        self.name = name
        self.description = description
        self.map = LetterMapping(mapping)
        self.prev_map = PrevMapping(prev_mapping or {})
        self.next_map = NextMapping(next_mapping or {})
        self.ending_map = EndingMapping(ending_mapping or {})
        self.samples = samples or []

    def translate_letter(self, prev, curr, next_):
        """Translate ``curr`` letter according to schema mappings.

        ``prev`` (the previous letter) and ``next_`` (the next one)
        are taken into consideration according to corresponding mappings.

        """
        letter = self.prev_map.get(prev + curr)
        if letter is None:
            letter = self.next_map.get(curr + next_)
        if letter is None:
            letter = self.map.get(curr, curr)
        return letter

    def translate_ending(self, ending):
        """Translate word ending according to schema mapping."""
        return self.ending_map.get(ending)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    @classmethod
    def load(cls, definition):
        """Load schema from definition."""

        defn = SchemaDefinition(definition)
        defn.parse()
        return Schema(
            name=defn.name,
            description=defn.description,
            mapping=defn.mapping,
            prev_mapping=defn.prev_mapping,
            next_mapping=defn.next_mapping,
            ending_mapping=defn.ending_mapping,
            samples=defn.samples,
        )


# pylint: disable=too-many-instance-attributes
class SchemaDefinition(object):
    """Translitiration schema definition."""

    def __init__(self, source):
        self.source = source
        self.name = ""
        self.description = ""
        self.mapping = {}
        self.prev_mapping = None
        self.next_mapping = None
        self.ending_mapping = None
        self.samples = []

    def parse(self):
        """Parse source definition, raising ValueError if necessary."""
        self._parse_attr("name", type_=basestring, required=True, nonempty=True)
        self._parse_attr("description", type_=basestring, required=False)
        self._parse_attr("mapping", type_=dict, required=True)
        self._parse_attr("prev_mapping", type_=dict, required=False)
        self._parse_attr("next_mapping", type_=dict, required=False)
        self._parse_attr("ending_mapping", type_=dict, required=False)
        self._parse_samples()

    def _parse_attr(self, name, type_, required, nonempty=False):
        value = self.source.get(name)
        if required and value is None:
            raise ValueError("{self.name}: Missing schema {name}".format(**locals()))
        if required and nonempty and not value:
            raise ValueError("{self.name}: Schema {name} should not be empty".format(**locals()))
        if value is not None and not isinstance(value, type_):
            raise ValueError("{self.name}: Invalid schema {name}: {value}".format(**locals()))
        setattr(self, name, value)

    def _parse_samples(self):
        samples = self.source.get("samples")
        if samples is not None and not isinstance(samples, list):
            raise ValueError("{self.name}: Invalid schema samples: {samples}".format(**locals()))
        if samples:
            for sample in samples:
                self._raise_on_invalid_sample(sample)
        self.samples = samples

    def _raise_on_invalid_sample(self, sample):
        message = "{self.name}: Invalid schema sample: {sample}".format(**locals())
        if not isinstance(sample, list):
            raise ValueError(message)
        if len(sample) != 2:
            raise ValueError(message)
        if not isinstance(sample[0], basestring) or not isinstance(sample[1], basestring):
            raise ValueError(message)
