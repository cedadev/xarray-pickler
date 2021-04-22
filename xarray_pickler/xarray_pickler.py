"""Main module."""

__author__ = """Elle Smith"""
__contact__ = 'eleanor.smith@stfc.ac.uk'
__copyright__ = "Copyright 2020 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"

import glob
import os
import xarray as xr
import pickle

from xarray_pickler import CONFIG, logging

logger = logging.getLogger(__file__)

def _get_pickle_path(dpath):
    """
    Define a "grouped" path that splits facets across directories and then groups
    the final set into a file path, based on dir_grouping_level value in CONFIG
    """
    cache = CONFIG['paths']['cache_base_dir']
    gl = CONFIG['paths']['dir_grouping_level']

    if not os.path.isdir(cache):
        os.makedirs(cache)

    parts = dpath.split("/")
    grouped_path = "/".join(parts[:-gl]) + "/" + ".".join(parts[-gl:])

    pickle_path = os.path.join(cache, grouped_path + ".pickle")

    return pickle_path


def open_dset(dpath, force_repickle=False, **kwargs):

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

    logger.info(f"Pickling dataset to: {pickle_path}")
    with open(pickle_path, 'wb') as writer:
        pkl = pickle.dump(ds, writer, protocol=-1)

    return ds