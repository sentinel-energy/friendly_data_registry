from itertools import chain
import json
from pathlib import Path
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
    """Retrieve the column schema from column schema registry: `friendly_data_registry`

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

    curdir = Path(resource_filename("friendly_data_registry", col_t))
    schema = list(
        chain.from_iterable(curdir.glob(f"{col}.{fmt}") for fmt in ("json", "yaml"))
    )
    if len(schema) == 0:
        warn(f"{col}: not in registry", RuntimeWarning)
        return {}  # no match, unregistered column
    if len(schema) > 1:  # pragma: no cover, bad registry
        raise RuntimeError(f"{schema}: multiple matches, duplicates in registry")
    return cast(Dict, read_file(curdir / schema[0]))


def getall(with_file: bool = False) -> Dict[str, List[Dict]]:
    """Get all columns from registry, primarily to generate documentation

    Returns
    -------
    Dict[str, Dict]
        The returned value is separated by column type::

          {
            "idxcols": [
              {..}  # column schemas
            ],
            "cols": [
              {..}  # column schemas
            ],
          }

    Raises
    ------
    RuntimeError
        When more than one matches are found

    """
    res = {}
    for col_t in ("cols", "idxcols"):
        col_t_dir = Path(resource_filename("friendly_data_registry", col_t))
        cols = []
        schema_files = set()
        for f in chain.from_iterable(
            col_t_dir.glob(f"*.{fmt}") for fmt in ("json", "yaml")
        ):
            if f.stem in schema_files:
                raise RuntimeError(f"{f}: duplicate schema in registry")
            else:
                schema_files.add(f.stem)
            if with_file:
                cols += [(read_file(f), f"{f.relative_to(col_t_dir.parent)}")]
            else:
                cols += [read_file(f)]
        res[col_t] = cols
    return res
