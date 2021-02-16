from itertools import chain
import json
from pathlib import Path
from string import Template
from textwrap import dedent
from typing import cast, Dict, List, Union
from warnings import warn

from pkg_resources import resource_filename

import yaml

_path_t = Union[str, Path]


def read_file(fpath: _path_t) -> Union[Dict, List]:
    """Read JSON or yaml file; file type is guessed from extension"""
    fpath = Path(fpath)
    if fpath.suffix in (".yaml", ".yml"):
        reader = yaml.safe_load
    elif fpath.suffix == ".json":
        reader = json.loads
    else:
        raise RuntimeError(f"{fpath}: not a JSON or YAML file")
    return reader(fpath.read_text())


# FIXME: can't use Literal until we drop 3.7
def get(col: str, col_t: str) -> Dict:
    """Retrieve the column schema from column schema registry: `sark_registry`

    Parameters
    ----------
    col : str
        Column name to look for

    col_t : Literal["cols", "idxcols"]
        A literal string specifying the kind of column; one of: "cols", or "idxcols"

    Returns
    -------
    Dict
        Column schema; an empty dictionary is returned in case there are no matches

    Raises
    ------
    RuntimeError
        When more than one matches are found
    ValueError
        When the schema file in the registry is unsupported; not one of: JSON, or YAML

    """
    if col_t not in ("cols", "idxcols"):
        raise ValueError(f"{col_t}: unknown column type")

    curdir = Path(resource_filename("sark_registry", col_t))
    schema = list(
        chain.from_iterable(curdir.glob(f"{col}.{fmt}") for fmt in ("json", "yaml"))
    )
    if len(schema) == 0:
        warn(f"{col}: not in registry", RuntimeWarning)
        return {}  # no match, unregistered column
    if len(schema) > 1:  # pragma: no cover, bad registry
        raise RuntimeError(f"{schema}: multiple matches, duplicates in registry")
    return cast(Dict, read_file(curdir / schema[0]))


def help() -> str:
    """Generate documentation for all columns in the registry"""
    # definition list entry
    entry = Template(
        dedent(
            """
    **$name ($type)**
        constraints: $constraints
    """
        )
    )

    col_types = {
        "cols": "Value columns - ``cols``",
        "idxcols": "Index columns - ``idxcols``",
    }
    contents = []
    for col_t, desc in col_types.items():
        contents += [desc, "-" * len(desc)]  # section heading
        curdir = Path(resource_filename("sark_registry", col_t))
        schemas: List[Dict] = [
            read_file(f)
            for f in chain.from_iterable(
                curdir.glob(f"*.{fmt}") for fmt in ("json", "yaml")
            )
        ]
        contents += [
            "".join(
                [
                    # substitute and clean up unsubstituted keys
                    entry.safe_substitute(**schema).replace(
                        "constraints: $constraints", ""
                    )
                    for schema in schemas
                ]
            )
        ]
    return "\n".join(contents)
