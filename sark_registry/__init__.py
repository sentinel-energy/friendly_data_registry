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
