from contextlib import nullcontext as does_not_raise

import pytest

import sark_registry as registry


@pytest.mark.parametrize(
    "col, col_t, expectation",
    [
        ("locs", "idxcols", does_not_raise()),
        ("storage", "cols", does_not_raise()),
        (
            "notinreg",
            "cols",
            pytest.warns(RuntimeWarning, match="notinreg: not in registry"),
        ),
        (
            "timesteps",
            "bad_col_t",
            pytest.raises(ValueError, match="bad_col_t: unknown column type"),
        ),
    ],
)
def test_registry(col, col_t, expectation):
    with expectation:
        res = registry.get(col, col_t)
        assert isinstance(res, dict)
        if col == "notinreg":
            assert res == {}
