"""Main module."""

__author__ = """Elle Smith"""
__contact__ = "eleanor.smith@stfc.ac.uk"
__copyright__ = "Copyright 2020 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"

import os
import pickle

import xarray as xr

from xarray_pickler import CONFIG, logging

logger = logging.getLogger(__file__)


def _get_pickle_path(dpath):
    """
    Define a "grouped" path that splits facets across directories and then groups
    the final set into a file path, based on dir_grouping_level value in CONFIG
    """
    cache = CONFIG["paths"]["cache_base_dir"]
    gl = CONFIG["paths"]["dir_grouping_level"]

    parts = dpath.split("/")[1:]
    grouped_path = "/".join(parts[:-gl]) + "/" + ".".join(parts[-gl:])

    pickle_path = os.path.join(cache, grouped_path)

    if not os.path.isdir(pickle_path):
        os.makedirs(pickle_path)

    return pickle_path + ".pickle"


def open_dset(dpath, force_repickle=False, **kwargs):
    """
    Open xarray.Dataset object. If previsouly pickled, it will be opened from the pickle file stored in the cache.
    Otherwise, it will be pickled and stored in the cache and opened using xarray.open_mfdataset() with and extra keyword arguments specified.

    :param dpath: Directory path to netCDF files to generate dataset from e.g. "/badc/cmip6/data/CMIP6/CMIP/IPSL/IPSL-CM6A-LR/historical/r1i1p1f1/Amon/rlds/gr/v20180803"
    :param force_repickle: If True, the xarray.Dataset object will be repickled. Default is False.
    :param **kwargs: Other keyword arguments that can be used in xarray.open_mfdataset(). Used only for the first time a dataset is pickled or if force_repickle=True.

    :return: xarray.Dataset object
    """

    open_kwargs = CONFIG["open_mfdataset_kwargs"].copy()
    open_kwargs.update(kwargs)

    fpattn = f"{dpath}/*.nc"
    logger.info(f"Reading: {fpattn}")

    pickle_path = _get_pickle_path(dpath)

    if os.path.isfile(pickle_path) and not force_repickle:
        try:
            with open(pickle_path, "rb") as reader:
                return pickle.load(reader)
        except Exception:
            # Assume failure so try to re-read and re-pickle the file
            pass

    ds = xr.open_mfdataset(fpattn, **open_kwargs)
    ds.close()

    logger.info(f"Pickling dataset to: {pickle_path}")
    with open(pickle_path, "wb") as writer:
        pickle.dump(ds, writer, protocol=-1)

    return ds
