import numpy as np
import pytest

import xarray as xr
from xarray import set_options


def test_xr_where_keep_attrs_true_dataarray():
    da = xr.DataArray(
        np.arange(5), dims=["t"], attrs={"units": "m", "desc": "test"}
    )
    cond = da < 3
    out = xr.where(cond, da, da * 10, keep_attrs=True)
    assert out.attrs == da.attrs


def test_xr_where_keep_attrs_false_dataarray():
    da = xr.DataArray(np.arange(5), dims=["t"], attrs={"a": 1})
    cond = da < 3
    out = xr.where(cond, da, da * 10, keep_attrs=False)
    assert out.attrs == {}


def test_xr_where_respects_global_option_dataarray():
    da = xr.DataArray(np.arange(5), dims=["t"], attrs={"a": 1})
    cond = da < 3
    with set_options(keep_attrs=True):
        out = xr.where(cond, da, da * 10)
        assert out.attrs == da.attrs
    with set_options(keep_attrs=False):
        out2 = xr.where(cond, da, da * 10)
        assert out2.attrs == {}


def test_xr_where_keep_attrs_dataset():
    ds = xr.Dataset(
        {"a": ("t", np.arange(5))}, attrs={"title": "ds"}
    )
    ds["a"].attrs = {"units": "m"}
    cond = ds["a"] < 3

    out_true = xr.where(cond, ds, ds * 10, keep_attrs=True)
    assert out_true.attrs == ds.attrs
    assert out_true["a"].attrs == ds["a"].attrs

    out_false = xr.where(cond, ds, ds * 10, keep_attrs=False)
    assert out_false.attrs == {}
    assert out_false["a"].attrs == {}

