#!/usr/bin/env python

"""Tests for `xarray_pickler` package."""

__author__ = """Elle Smith"""
__contact__ = "eleanor.smith@stfc.ac.uk"
__copyright__ = "Copyright 2020 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"

import xarray as xr

from xarray_pickler import CONFIG
from xarray_pickler.xarray_pickler import _get_pickle_path, open_dset

from .conftest import MINI_ESGF_CACHE_DIR


def test_get_pickle_path(tmpdir):
    CONFIG["paths"]["cache_base_dir"] = f"{tmpdir}/fakepath"
    dpath = "/badc/cmip6/data/CMIP6/CMIP/IPSL/IPSL-CM6A-LR/historical/r1i1p1f1/Amon/rlds/gr/v20180803"

    pickle_path = _get_pickle_path(dpath)

    assert (
        pickle_path
        == f"{tmpdir}/fakepath/badc/cmip6/data/CMIP6/CMIP/IPSL/IPSL-CM6A-LR/historical/r1i1p1f1/Amon.rlds.gr.v20180803.pickle"
    )


def test_open_dset_default_kwargs(tmpdir, load_test_data):
    CONFIG["paths"]["cache_base_dir"] = tmpdir
    dpath = f"{MINI_ESGF_CACHE_DIR}/master/test_data/badc/cmip6/data/CMIP6/CMIP/INM/INM-CM5-0/historical/r1i1p1f1/Amon/rlds/gr1/v20190610/"

    ds_original = xr.open_mfdataset(
        f"{dpath}/*nc", use_cftime=True, combine="by_coords"
    )

    ds = open_dset(dpath)

    assert ds == ds_original

    #  try and open again now that it has been pickled
    ds_from_pickle = open_dset(dpath)

    assert ds_from_pickle == ds_original


def test_open_dset_force_repickle(tmpdir, load_test_data):
    CONFIG["paths"]["cache_base_dir"] = tmpdir
    dpath = f"{MINI_ESGF_CACHE_DIR}/master/test_data/badc/cmip6/data/CMIP6/CMIP/INM/INM-CM5-0/historical/r1i1p1f1/Amon/rlds/gr1/v20190610/"

    ds_original = xr.open_mfdataset(
        f"{dpath}/*nc", use_cftime=True, combine="by_coords"
    )

    ds_pickle = open_dset(dpath)

    assert ds_pickle == ds_original

    ds_repickle = open_dset(dpath, force_repickle=True)

    assert ds_repickle == ds_original


def test_curvilinear_dataset(tmpdir, load_test_data):
    dpath = f"{MINI_ESGF_CACHE_DIR}/master/test_data/badc/cmip6/data/CMIP6/CMIP/MPI-M/MPI-ESM1-2-LR/historical/r1i1p1f1/Omon/tos/gn/v20190710/"

    ds_original = xr.open_mfdataset(
        f"{dpath}/*nc", use_cftime=True, combine="by_coords"
    )

    ds = open_dset(dpath)

    assert ds == ds_original

    ds_pickle = open_dset(dpath)

    assert ds_pickle == ds_original
