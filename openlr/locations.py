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
from typing import NamedTuple, List
from enum import Enum


class FRC(Enum):
    """The functional road class is a road classification based on
    the importance of a road."""

    FRC0 = 0  #: Main road, highest importance
    FRC1 = 1  #: First class road
    FRC2 = 2  #: Second class road
    FRC3 = 3  #: Third class road
    FRC4 = 4  #: Fourth class road
    FRC5 = 5  #: Fifth class road
    FRC6 = 6  #: Sixth class road
    FRC7 = 7  #: Other class road, lowest importance


class FOW(Enum):
    """The form of way describes the physical road type."""

    UNDEFINED = 0  #:The physical road type is unknown
    MOTORWAY = 1
    """A Motorway is defined as a road permitted for
    motorized vehicles only in combination with a
    prescribed minimum speed. It has two or more
    physically separated carriageways and no single
    level-crossings."""
    MULTIPLE_CARRIAGEWAY = 2
    """A multiple carriageway is defined as a road with
    physically separated carriageways regardless of the
    number of lanes. If a road is also a motorway, it
    should be coded as such and not as a multiple
    carriageway."""
    SINGLE_CARRIAGEWAY = 3
    """All roads without separate carriageways are
    considered as roads with a single carriageway."""
    ROUNDABOUT = 4
    """A Roundabout is a road which forms a ring on which
    traffic traveling in only one direction is allowed."""
    TRAFFICSQUARE = 5
    """A Traffic Square is an open area (partly) enclosed by
    roads which is used for non-traffic purposes and
    which is not a Roundabout."""
    SLIPROAD = 6
    """A Slip Road is a road especially designed to enter or
    leave a line."""
    OTHER = 7
    """The physical road type is known but does not fit into
    one of the other categories."""


class SideOfRoad(Enum):
    """The side of the road is valid only for point locations and indicates
    on which side of the referenced road the point location is located."""

    ON_ROAD_OR_UNKNOWN = 0
    """Point is directly on (or above) the road, or determination of
    right/left side is not applicable (default)"""
    RIGHT = 1  #: Point is on right side of the road
    LEFT = 2  #: Point is on the left side of the road
    BOTH = 3  #: Point is on both sides of the road


class Orientation(Enum):
    """The orientation is only valid for point locations and indicates
    for which direction the point information is relevant."""

    NO_ORIENTATION_OR_UNKNOWN = 0
    """Point has no sense of orientation, or determination of
    orientation is not applicable (default)"""
    WITH_LINE_DIRECTION = 1
    """Point has orientation from first LRP towards second LRP"""
    AGAINST_LINE_DIRECTION = 2
    """Point has orientation from second LRP towards first LRP"""
    BOTH = 3
    """Point has orientation in both directions"""


Coordinates = NamedTuple("Coordinates", [("lon", float), ("lat", float)])
"""A coordinate pair `longitude` (lon) and `latitude` (lat) represented in
WGS84 coordinates."""
LineAttributes = NamedTuple(
    "LineAttributes", [("frc", FRC), ("fow", FOW), ("bear", int)]
)
"""Line attributes consist of functional road class, form of way, and bearing."""
PathAttributes = NamedTuple("PathAttributes", [("lfrcnp", FRC), ("dnp", int)])
"""Path attributes consist of lowest FRC to next point, and distance to next point."""
LocationReferencePoint = NamedTuple(
    "LocationReferencePoint",
    [
        # Coordinates
        ("lon", float),
        ("lat", float),
        # LineAttributes
        ("frc", FRC),
        ("fow", FOW),
        ("bear", int),
        # PathAttributes
        ("lfrcnp", FRC),
        ("dnp", int),
    ],
)
"""A location reference point consists of coordinate, line attribute and
path attribute data."""
LineLocation = NamedTuple(
    "LineLocation",
    [("points", List[LocationReferencePoint]), ("poffs", int), ("noffs", int)],
)
"""A line location reference describes a path within a map and consists of location
reference point(s), a last location reference point and offset data."""
GeoCoordinateLocation = NamedTuple("GeoCoordinateLocation", [("point", Coordinates)])
"""GeoCoordinate is a point location which consists of exactly one oordinate pair."""
PointAlongLineLocation = NamedTuple(
    "PointAlongLineLocation",
    [
        ("points", List[LocationReferencePoint]),
        ("poffs", int),
        ("orientation", Orientation),
        ("sideOfRoad", SideOfRoad),
    ],
)
"""Point along line is a point location which is defined by a line and an offset value.
The line will be referenced by two location reference points and the concrete position
on that line is referenced using the positive offset. Additionally information about
the side of the road where the point is located and the orientation with respect
to the direction of the line can be added."""
PoiWithAccessPointLocation = NamedTuple(
    "PoiWithAccessPointLocation",
    [
        ("points", List[LocationReferencePoint]),
        ("poffs", int),
        ("lon", float),
        ("lat", float),
        ("orientation", Orientation),
        ("sideOfRoad", SideOfRoad),
    ],
)
"""Point along line with access is a point location which is defined by a line,
an offset value and a coordinate. The line will be referenced by two location reference
points and the concrete position of the access point on that line is referenced using
the positive offset. The point of interest is identified by the coordinate pair.
Additionally information about the side of the road where the point is located and
the orientation with respect to the direction of the line can be added."""
CircleLocation = NamedTuple("CircleLocation", [("point", Coordinates), ("radius", int)])
"""A CircleLocationReference represents a circle area location."""
RectangleLocation = NamedTuple(
    "RectangleLocation", [("lowerLeft", Coordinates), ("upperRight", Coordinates)]
)
"""A RectangleLocationReference represents a rectangular area location."""
GridLocation = NamedTuple(
    "GridLocation",
    [
        ("lowerLeft", Coordinates),
        ("upperRight", Coordinates),
        ("n_cols", int),
        ("n_rows", int),
    ],
)
"""A GridLocationReference represents a rectangular area location
with a grid of n_cols columns and n_rows rows."""
PolygonLocation = NamedTuple("PolygonLocation", [("corners", List[Coordinates])])
"""A PolygonLocationReference represents a polygonal area location."""
ClosedLineLocation = NamedTuple(
    "ClosedLineLocation",
    [("points", List[LocationReferencePoint]), ("lastLine", LineAttributes)],
)
"""A LineLocationReference is defined by an ordered sequence of
location reference points and a terminating last location reference point."""
