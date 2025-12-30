import numpy as np

import xarray as xr


def test_xr_where_keep_attrs_true_dataarray() -> None:
    cond = np.array([True, False])
    data = xr.DataArray([1, 2], dims=["x"], attrs={"source": "x"})
    other = xr.DataArray([3, 4], dims=["x"], attrs={"source": "y"})

    result = xr.where(cond, data, other, keep_attrs=True)

    assert result.attrs == data.attrs


def test_xr_where_keep_attrs_false_dataarray() -> None:
    cond = np.array([True, False])
    data = xr.DataArray([1, 2], dims=["x"], attrs={"source": "x"})
    other = xr.DataArray([3, 4], dims=["x"], attrs={"source": "y"})

    result = xr.where(cond, data, other, keep_attrs=False)

    assert result.attrs == {}


def test_xr_where_respects_global_option_dataarray() -> None:
    cond = np.array([True, False])
    data = xr.DataArray([1, 2], dims=["x"], attrs={"source": "x"})
    other = xr.DataArray([3, 4], dims=["x"], attrs={"source": "y"})

    with xr.set_options(keep_attrs=True):
        result_keep = xr.where(cond, data, other)
    assert result_keep.attrs == data.attrs

    with xr.set_options(keep_attrs=False):
        result_drop = xr.where(cond, data, other)
    assert result_drop.attrs == {}


def test_xr_where_keep_attrs_dataset() -> None:
    cond = xr.DataArray([True, False], dims=["x"])
    data = xr.Dataset(
        {
            "a": xr.DataArray([1, 2], dims=["x"], attrs={"va": "A"}),
            "b": xr.DataArray([3, 4], dims=["x"], attrs={"vb": "B"}),
        },
        attrs={"ds": "data"},
    )
    other = xr.Dataset(
        {
            "a": xr.DataArray([5, 6], dims=["x"], attrs={"va": "YA"}),
            "b": xr.DataArray([7, 8], dims=["x"], attrs={"vb": "YB"}),
        },
        attrs={"ds": "other"},
    )

    result_keep = xr.where(cond, data, other, keep_attrs=True)
    assert result_keep.attrs == data.attrs
    for name in data.data_vars:
        assert result_keep[name].attrs == data[name].attrs

    result_drop = xr.where(cond, data, other, keep_attrs=False)
    assert result_drop.attrs == {}
    for name in data.data_vars:
        assert result_drop[name].attrs == {}
