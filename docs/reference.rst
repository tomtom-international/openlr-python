Reference
=========

Locations
----------

Enums
~~~~~

.. autoclass:: openlr.FRC
.. autoclass:: openlr.FOW
.. autoclass:: openlr.SideOfRoad
.. autoclass:: openlr.Orientation

Location Properties
~~~~~~~~~~~~~~~~~~~

.. autofunction:: openlr.Coordinates

.. autoclass:: openlr.LineAttributes
  :exclude-members: frc, fow, bear
.. autoclass:: openlr.PathAttributes
  :exclude-members: lfrcnp, dnp
.. autoclass:: openlr.LocationReferencePoint
  :exclude-members: lon, lat, frc, fow, bear, lfrcnp, dnp

Reference Locations
~~~~~~~~~~~~~~~~~~~

.. autoclass:: openlr.LineLocation
  :exclude-members: points, poffs, noffs
.. autoclass:: openlr.GeoCoordinateLocation
  :exclude-members: point
.. autoclass:: openlr.PointAlongLineLocation
  :exclude-members: points, poffs, orientation, sideOfRoad
.. autoclass:: openlr.PoiWithAccessPointLocation
  :exclude-members: points, poffs, lon, lat, orientation, sideOfRoad
.. autoclass:: openlr.CircleLocation
  :exclude-members: point, radius
.. autoclass:: openlr.RectangleLocation
  :exclude-members: lowerLeft, upperRight
.. autoclass:: openlr.GridLocation
  :exclude-members: lowerLeft, upperRight, n_cols, n_rows
.. autoclass:: openlr.PolygonLocation
  :exclude-members: corners
.. autoclass:: openlr.ClosedLineLocation
  :exclude-members: points, lastLine

XML Format
----------

XML OpenLR physical format conversion methods based on the white paper.

.. autofunction:: openlr.xml_decode_document
.. autofunction:: openlr.xml_decode_file
.. autofunction:: openlr.xml_decode_string
.. autofunction:: openlr.xml_encode_to_document
.. autofunction:: openlr.xml_encode_to_string


Binary Format
-------------

Binary OpenLR physical format conversion methods based on the white paper.

.. autofunction:: openlr.binary_decode
.. autofunction:: openlr.binary_encode

Binary Internal APIs
--------------------

.. automodule:: openlr.openlr_bytes_io
  :member-order: bysource

Helper Functions
----------------

.. autofunction:: openlr.get_dict
.. autofunction:: openlr.get_lonlat_list
