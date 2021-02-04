# coding: utf8
"""
Transliteration schema registry.
"""

import os.path
import json
from operator import attrgetter
from iuliia.schema import Schema
from aenum import Enum


def _schema_loader():
    return (Schema.load(defn) for defn in _definition_reader())


def _definition_reader():
    schemas_path = os.path.join(os.path.abspath(os.path.join(__file__, os.pardir)), "schemas")
    if not os.path.exists(schemas_path):
        raise ValueError("Schema path does not exist: {schemas_path}".format(**locals()))
    for path in os.listdir(schemas_path):
        path = os.path.join(schemas_path, path)
        name, ext = os.path.splitext(path)
        if ext != '.json':
            continue
        definition = _load_definition(path)
        yield definition


def _load_definition(path):
    with open(path) as file:
        return json.load(file)


class _Schemas(Enum):
    """Base class for supported transliteration schemas."""

    @classmethod
    def names(cls):
        """Return names of all supported schemas."""
        return sorted(item.name for item in cls)

    @classmethod
    def items(cls):
        """Return all supported schemas."""
        return [(item.name, item.value) for item in sorted(cls, key=attrgetter("value.name"))]

    @classmethod
    def get(cls, name):
        """Return schema by its name or ``None`` if nothing found."""
        item = cls.__members__.get(name)
        return item.value if item else None


# All supported transliteration schemas
# pylint: disable=invalid-name
Schemas = Enum(  # type: ignore
    "Schemas", [(schema.name, schema) for schema in _schema_loader()], type=_Schemas
)
