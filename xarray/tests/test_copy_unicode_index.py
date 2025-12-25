import copy

import numpy as np
import pandas as pd

import xarray as xr
from xarray import IndexVariable, Variable


def test_indexvariable_unicode_deep_copy_preserves_dtype():
    values = np.array(["foo", "bar"], dtype="<U3")
    index_var = IndexVariable("x", values)

    shallow = index_var.copy(deep=False)
    assert shallow.dtype == index_var.dtype
    assert shallow.dtype.kind == "U"

    deep = index_var.copy(deep=True)
    assert deep.dtype == index_var.dtype
    assert deep.dtype.kind == "U"

    deepcopy_var = copy.deepcopy(index_var)
    assert deepcopy_var.dtype == index_var.dtype
    assert deepcopy_var.dtype.kind == "U"


def test_dataarray_unicode_coord_copy_methods_preserve_dtype():
    coord_values = np.array(["alpha", "beta"], dtype="<U5")
    data = np.arange(coord_values.size)
    array = xr.DataArray(data, dims="x", coords={"x": coord_values})

    for copier in (
        lambda a: a.copy(deep=True),
        lambda a: a.copy(deep=False),
        copy.copy,
        copy.deepcopy,
    ):
        result = copier(array)
        assert result.coords["x"].dtype == array.coords["x"].dtype
        assert result.coords["x"].dtype.kind == "U"


def test_dataset_unicode_coord_copy_methods_preserve_dtype():
    coord_values = np.array(["gamma", "delta"], dtype="<U5")
    ds = xr.Dataset(
        coords={"x": coord_values},
        data_vars={"z": ("x", np.array(["eps", "zeta"], dtype="<U4"))},
    )

    for copier in (
        lambda d: d.copy(deep=True),
        lambda d: d.copy(deep=False),
        copy.copy,
        copy.deepcopy,
    ):
        result = copier(ds)
        assert result.coords["x"].dtype == ds.coords["x"].dtype
        assert result.coords["x"].dtype.kind == "U"


def test_unicode_index_edge_cases():
    empty_index = IndexVariable("x", np.array([], dtype="<U1"))
    assert empty_index.copy(deep=True).dtype.kind == "U"
    assert copy.deepcopy(empty_index).dtype.kind == "U"

    multi_index = IndexVariable(
        "x", pd.MultiIndex.from_product([["a", "b"], [1, 2]])
    )
    assert multi_index.copy(deep=True).dtype == object
    assert copy.deepcopy(multi_index).dtype == object

    pandas_string = IndexVariable(
        "x", pd.Index(["one", "two"], dtype="string")
    )
    assert pandas_string.copy(deep=True).dtype == object
    assert copy.deepcopy(pandas_string).dtype == object

    scalar_unicode = Variable((), np.array("omega", dtype="<U5"))
    assert scalar_unicode.copy(deep=True).dtype.kind == "U"
    assert copy.deepcopy(scalar_unicode).dtype.kind == "U"
