Development
===========

This project uses `tox <https://tox.readthedocs.io/>`_ for running tests and
other things (style check, coverage reports, sphinx docs).

It is recommended to install `conda <https://docs.conda.io/en/latest/miniconda.html>`_
along with `tox-conda <https://github.com/tox-dev/tox-conda>`_ for using tox.
Afterwards, ``tox`` command will run all the steps for you.

This project strictly uses `black <https://github.com/psf/black>`_ as an
opinionated code style.
Any written line should comply with that (don't forget to run ``black .``).

Always add tests for bug fixes and feature developments.

Binary Location Types
---------------------

Location type is determined based on the flags in the first byte and the data size.

+-----------------------+--------------------------------+----+----+----+----+
| Location type         | Data size                      | B6 | B5 | B4 | B3 |
+=======================+================================+====+====+====+====+
| Line                  | 16 + (n-2) * 7 + [0/1/2] bytes | 0  | 0  | 0  | 1  |
+-----------------------+--------------------------------+----+----+----+----+
| Geo-coordinate        | 7 bytes                        | 0  | 1  | 0  | 0  |
+-----------------------+--------------------------------+----+----+----+----+
| Point along line      | 16/17 bytes                    | 0  | 1  | 0  | 1  |
+-----------------------+--------------------------------+----+----+----+----+
| POI with access point | 20/21 bytes                    | 0  | 1  | 0  | 1  |
+-----------------------+--------------------------------+----+----+----+----+
| Circle                | 7 + [1/2/3/4] bytes            | 0  | 0  | 0  | 0  |
+-----------------------+--------------------------------+----+----+----+----+
| Rectangle             | 11/13 bytes                    | 1  | 0  | 0  | 0  |
+-----------------------+--------------------------------+----+----+----+----+
| Grid                  | 15/17 bytes                    | 1  | 0  | 0  | 0  |
+-----------------------+--------------------------------+----+----+----+----+
| Polygon               | 15 + (n-3) * 4 bytes           | 0  | 0  | 1  | 0  |
+-----------------------+--------------------------------+----+----+----+----+
| ClosedLine            | 19 + (n-3) * 7 bytes           | 1  | 0  | 1  | 1  |
+-----------------------+--------------------------------+----+----+----+----+

Flags in the first byte:

- Bit 6 (ArF1) - Area Flag 1
- Bit 5 (no point)
- Bit 4 (ArF0) - Area Flag 0
- Bit 3 (has attributes)
