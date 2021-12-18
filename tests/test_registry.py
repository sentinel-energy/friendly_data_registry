from itertools import chain
from pathlib import Path

from glom import MatchError, TypeMatchError
import pytest

import friendly_data_registry as registry

logger = registry.logger


@pytest.mark.parametrize(
    "schema, _file", chain.from_iterable(registry.getall(with_file=True).values())
)
def test_match_registry_schema(schema, _file):
    _file = Path(_file)
    try:
        registry.schschemaema(schema)
    except TypeMatchError as err:
        e, f = err.args[1:]
        logger.error(f"{_file}: type mismatch in value, expected {e}, found {f}")
        raise err from None
    except MatchError as err:
        logger.error(f"{_file}: {err.args[1]}: bad key in schema")
        raise err from None
    else:
        assert (
            _file.stem == schema["name"]
        ), f"{_file}: schema names do not match: `{schema['name']}`"
        logger.info("done")
