# xarray-pickler
Simple package to speed up "multi-file open" operations for xarray datasets. Uses a cache of pickle files to store the metadata in the `xarray.Dataset` object.
