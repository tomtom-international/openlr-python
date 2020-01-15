# Copyright (C) 2012-2020, TomTom (http://tomtom.com).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""OpenLR physical format encoder/decoder"""
from ._version import (
    __title__,
    __description__,
    __url__,
    __version__,
    __author__,
    __author_email__,
    __license__,
)
from openlr.locations import (
    FRC,
    FOW,
    SideOfRoad,
    Orientation,
    Coordinates,
    LineAttributes,
    PathAttributes,
    LocationReferencePoint,
    LineLocation,
    GeoCoordinateLocation,
    PointAlongLineLocation,
    PoiWithAccessPointLocation,
    CircleLocation,
    RectangleLocation,
    GridLocation,
    PolygonLocation,
    ClosedLineLocation,
)
from openlr.binary_format import binary_decode, binary_encode
from openlr.xml_format import (
    xml_decode_document,
    xml_decode_file,
    xml_decode_string,
    xml_encode_to_document,
    xml_encode_to_string,
)


def get_lonlat_list(location):
    """Helper to return a list of lonlat tuples of coordinates in a location"""
    lonlat_list = []
    if hasattr(location, "lon") and hasattr(location, "lat"):
        lonlat_list.append((location.lon, location.lat))
    if hasattr(location, "point"):
        lonlat_list.append((location.point.lon, location.point.lat))
    if hasattr(location, "points"):
        lonlat_list.extend([(p.lon, p.lat) for p in location.points])
    if hasattr(location, "corners"):
        lonlat_list.extend([(c.lon, c.lat) for c in location.corners])
    if hasattr(location, "lowerLeft") and hasattr(location, "upperRight"):
        lonlat_list.append((location.lowerLeft.lon, location.lowerLeft.lat))
        lonlat_list.append((location.upperRight.lon, location.upperRight.lat))
    return lonlat_list
