#!/usr/bin/env python

"""Tests for `xarray_pickler` package."""

__author__ = """Elle Smith"""
__contact__ = 'eleanor.smith@stfc.ac.uk'
__copyright__ = "Copyright 2020 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"

import pytest
import xarray as xr

from xarray_pickler.xarray_pickler import _get_pickle_path, open_dset

from xarray_pickler import CONFIG

def test_get_pickle_path():
    dpath = "/badc/cmip6/data/CMIP6/CMIP/IPSL/IPSL-CM6A-LR/historical/r1i1p1f1/Amon/rlds/gr/v20180803"

    pickle_path = _get_pickle_path(dpath)

    assert pickle_path == "/badc/cmip6/data/CMIP6/CMIP/IPSL/IPSL-CM6A-LR/historical/r1i1p1f1/Amon.rlds.gr.v20180803.pickle"


def test_open_dset_default_kwargs(tmpdir):
    CONFIG['paths']['cache_base_dir'] = tmpdir
    dpath = "/badc/cmip6/data/CMIP6/CMIP/IPSL/IPSL-CM6A-LR/historical/r1i1p1f1/Amon/rlds/gr/v20180803"

    ds_original = xr.open_mfdataset(dpath, usecftime=True, combine="by_coords")

    print(ds_original)

    ds = open_dset(dpath)

    print(ds)

    assert ds == ds_original

    # try and open again now that it has been pickled
    ds_from_pickle = open_dset(dpath)

    assert ds_from_pickle == ds_original

    print(ds_from_pickle)


def test_open_dset_force_repickle():
    CONFIG['paths']['cache_base_dir'] = tmpdir
    dpath = "/badc/cmip6/data/CMIP6/CMIP/IPSL/IPSL-CM6A-LR/historical/r1i1p1f1/Amon/rlds/gr/v20180803"

    ds_original = xr.open_mfdataset(dpath, usecftime=True, combine="by_coords")

    ds_pickle = open_dset(dpath, force_repickle=True)

    assert ds_pickle == ds_original

    ds_repickle = open_dset(dpath, force_repickle=False)

    assert ds_repickle == ds_original
