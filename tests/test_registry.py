from itertools import chain
from pathlib import Path

from glom import glom, Match, Optional as optmatch, Or
from glom import MatchError, TypeMatchError
import pytest

import friendly_data_registry as registry


class schschemaema:
    _schema = {
        "name": str,
        "type": str,
        optmatch("format"): str,
        optmatch("constraints"): {
            optmatch("enum"): list,
            optmatch("maximum"): Or(int, float),
            optmatch("minimum"): Or(int, float),
            optmatch("pattern"): str,
        },
        optmatch("title"): str,
        optmatch("description"): str,
        optmatch("alias"): [{"name": str, "description": str}],
    }

    def __init__(self, schema: dict):
        glom(schema, Match(self._schema))


@pytest.mark.parametrize(
    "schema, _file", chain.from_iterable(registry.getall(with_file=True).values())
)
def test_match_registry_schema(schema, _file):
    _file = Path(_file)
    try:
        schschemaema(schema)
    except TypeMatchError as err:
        e, f = err.args[1:]
        print(f"{_file}: type mismatch in value, expected {e}, found {f}")
        raise
    except MatchError as err:
        print(f"{_file}: {err.args[1]}: bad key in schema")
        raise
    else:
        assert (
            _file.stem == schema["name"]
        ), f"{_file}: schema names do not match: `{schema['name']}`"
