==================================================
WARNING: xarray-pickler is likely to be superseded
==================================================

...by https://grantjenks.com/docs/diskcache/ - as demonstrated in Carsten's notebook here:

https://github.com/roocs/rook/blob/dev-op-concat/notebooks/concat_with_cache.ipynb

See previous notes below.

==============
xarray-pickler
==============


.. image:: https://img.shields.io/pypi/v/xarray_pickler.svg
        :target: https://pypi.python.org/pypi/xarray-pickler

.. image:: https://github.com/cedadev/xarray-pickler/workflows/build/badge.svg
        :target: https://github.com/cedadev/xarray-pickler/actions
        :alt: Build Status

.. image:: https://readthedocs.org/projects/xarray-pickler/badge/?version=latest
        :target: https://xarray-pickler.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Simple package to speed up 'multi-file open' operations for xarray datasets. Uses a cache of pickle files to store the metadata in the `xarray.Dataset` object.


* Free software: BSD - see LICENSE file in top-level package directory
* Documentation: https://xarray-pickler.readthedocs.io.



Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
