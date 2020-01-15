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
import base64
import binascii
from enum import Enum


from openlr.openlr_bytes_io import OpenLRBytesIO
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


class LocationTypes(Enum):
    """Integer values of location type flags in 4 bits of the first byte:
    Point flag (Bit 5), Area flag (Bit 6 and 4), and Attributes flag (3).
    """

    LineLocation = 1
    GeoCoordinateLocation = 4
    PointAlongLineLocation = 5
    PoiWithAccessPointLocation = 5
    CircleLocation = 0
    RectangleLocation = 8
    GridLocation = 8
    PolygonLocation = 2
    ClosedLineLocation = 11


def binary_decode(data, is_base64=True):
    """Decodes binary data into Location

    Parameters
    -------
    data : str, bytearray, bytes
        A bytes-like object that contains the binary data
    is_base64 : bool
        Boolean flag for base64 encoded string data

    Returns
    -------
    location : NamedTuple
        Location object
    """
    if is_base64:
        data = base64.b64decode(data)

    data_bytes_size = len(data)
    data_bytes = OpenLRBytesIO(data)

    version, location_type = data_bytes.read_status()
    if version != 3:
        raise NotImplementedError(
            "Only version 3 is supported, detected version %s" % version
        )

    if location_type == LocationTypes.LineLocation.value:
        return _parse_line(data_bytes, data_bytes_size)
    elif location_type == LocationTypes.GeoCoordinateLocation.value:
        return _parse_geo_coordinate(data_bytes)
    elif location_type == LocationTypes.PointAlongLineLocation.value:
        if data_bytes_size > 17:
            return _parse_poi(data_bytes)
        else:
            return _parse_point_along_line(data_bytes)
    elif location_type == LocationTypes.CircleLocation.value:
        return _parse_circle(data_bytes)
    elif location_type == LocationTypes.RectangleLocation.value:
        if data_bytes_size > 13:
            return _parse_grid(data_bytes, data_bytes_size)
        else:
            return _parse_rectangle(data_bytes, data_bytes_size)
    elif location_type == LocationTypes.PolygonLocation.value:
        return _parse_polygon(data_bytes, data_bytes_size)
    elif location_type == LocationTypes.ClosedLineLocation.value:
        return _parse_closed_line(data_bytes, data_bytes_size)
    else:
        raise ValueError("Location type cannot be identified.")


def binary_encode(location, is_base64=True):
    """Encodes Location object into binary data

    Parameters
    -------
    location : NamedTuple
        Location object
    is_base64 : bool
        Boolean flag for base64 encoded string data

    Returns
    -------
    data : str, bytearray, bytes
        A bytes-like object that contains the binary data
    """
    data_bytes = OpenLRBytesIO()

    if isinstance(location, LineLocation):
        data_bytes.write_status(3, LocationTypes.LineLocation.value)
        _write_line(location, data_bytes)
    elif isinstance(location, GeoCoordinateLocation):
        data_bytes.write_status(3, LocationTypes.GeoCoordinateLocation.value)
        _write_geo_coordinate(location, data_bytes)
    elif isinstance(location, PointAlongLineLocation):
        data_bytes.write_status(3, LocationTypes.PointAlongLineLocation.value)
        _write_point_along_line(location, data_bytes)
    elif isinstance(location, PoiWithAccessPointLocation):
        data_bytes.write_status(3, LocationTypes.PoiWithAccessPointLocation.value)
        _write_poi(location, data_bytes)
    elif isinstance(location, CircleLocation):
        data_bytes.write_status(3, LocationTypes.CircleLocation.value)
        _write_circle(location, data_bytes)
    elif isinstance(location, RectangleLocation):
        data_bytes.write_status(3, LocationTypes.RectangleLocation.value)
        _write_rectangle(location, data_bytes)
    elif isinstance(location, GridLocation):
        data_bytes.write_status(3, LocationTypes.GridLocation.value)
        _write_grid(location, data_bytes)
    elif isinstance(location, PolygonLocation):
        data_bytes.write_status(3, LocationTypes.PolygonLocation.value)
        _write_polygon(location, data_bytes)
    elif isinstance(location, ClosedLineLocation):
        data_bytes.write_status(3, LocationTypes.ClosedLineLocation.value)
        _write_closed_line(location, data_bytes)
    else:
        raise ValueError("object %r is not a Location type" % (location,))
    if is_base64:
        return base64.b64encode(data_bytes.getvalue()).decode()
    else:
        return data_bytes.getvalue()


def _parse_line(data_buffer, size):
    points = []
    n_relative_points = (size - 9) // 7

    lon, lat = data_buffer.read_coords()
    fow, frc, bear, lfrcnp, _ = data_buffer.read_point_attributes()
    for _ in range(n_relative_points):
        dnp = data_buffer.read_dnp()
        points.append(
            LocationReferencePoint(lon, lat, FRC(frc), FOW(fow), bear, FRC(lfrcnp), dnp)
        )
        lon, lat = data_buffer.read_coords_relative(lon, lat)
        fow, frc, bear, lfrcnp, _ = data_buffer.read_point_attributes()

    points.append(
        LocationReferencePoint(lon, lat, FRC(frc), FOW(fow), bear, FRC.FRC7, 0)
    )

    poffs = data_buffer.read_offset() if lfrcnp & 0b10 else 0
    noffs = data_buffer.read_offset() if lfrcnp & 0b01 else 0
    return LineLocation(points, poffs, noffs)


def _parse_geo_coordinate(data_buffer):
    lon, lat = data_buffer.read_coords()
    point = Coordinates(lon, lat)
    return GeoCoordinateLocation(point)


def _parse_point_along_line(data_buffer):
    points = []

    lon, lat = data_buffer.read_coords()
    fow, frc, bear, lfrcnp, orientation = data_buffer.read_point_attributes()
    dnp = data_buffer.read_dnp()
    points.append(
        LocationReferencePoint(lon, lat, FRC(frc), FOW(fow), bear, FRC(lfrcnp), dnp)
    )

    lon, lat = data_buffer.read_coords_relative(lon, lat)
    fow, frc, bear, lfrcnp, side_of_road = data_buffer.read_point_attributes()
    points.append(
        LocationReferencePoint(lon, lat, FRC(frc), FOW(fow), bear, FRC.FRC7, 0)
    )

    poffs = 0
    if lfrcnp & 0b10:
        poffs = data_buffer.read_offset()
    return PointAlongLineLocation(
        points, poffs, Orientation(orientation), SideOfRoad(side_of_road)
    )


def _parse_poi(data_buffer):
    points = []

    lon, lat = data_buffer.read_coords()
    fow, frc, bear, lfrcnp, orientation = data_buffer.read_point_attributes()
    dnp = data_buffer.read_dnp()
    points.append(
        LocationReferencePoint(lon, lat, FRC(frc), FOW(fow), bear, FRC(lfrcnp), dnp)
    )

    lon, lat = data_buffer.read_coords_relative(lon, lat)
    fow, frc, bear, lfrcnp, side_of_road = data_buffer.read_point_attributes()
    points.append(
        LocationReferencePoint(lon, lat, FRC(frc), FOW(fow), bear, FRC.FRC7, 0)
    )

    poffs = 0
    if lfrcnp & 0b10:
        poffs = data_buffer.read_offset()

    lon, lat = data_buffer.read_coords_relative(points[0].lon, points[0].lat)
    return PoiWithAccessPointLocation(
        points, poffs, lon, lat, Orientation(orientation), SideOfRoad(side_of_road)
    )


def _parse_circle(data_buffer):
    lon, lat = data_buffer.read_coords()
    point = Coordinates(lon, lat)
    radius = data_buffer.read_radius()
    return CircleLocation(point, radius)


def _parse_rectangle(data_buffer, size):
    lon, lat = data_buffer.read_coords()
    lowerLeft = Coordinates(lon, lat)
    if size > 11:  # absolute
        lon, lat = data_buffer.read_coords()
    else:  # relative
        lon, lat = data_buffer.read_coords_relative(lon, lat)
    upperRight = Coordinates(lon, lat)
    return RectangleLocation(lowerLeft, upperRight)


def _parse_grid(data_buffer, size):
    lon, lat = data_buffer.read_coords()
    lowerLeft = Coordinates(lon, lat)
    if size > 15:  # absolute
        lon, lat = data_buffer.read_coords()
    else:  # relative
        lon, lat = data_buffer.read_coords_relative(lon, lat)
    upperRight = Coordinates(lon, lat)
    cols, rows = data_buffer.read_cols_rows()
    return GridLocation(lowerLeft, upperRight, cols, rows)


def _parse_polygon(data_buffer, size):
    n_relative_corners = (size - 7) // 4

    corners = []
    lon, lat = data_buffer.read_coords()
    corners.append(Coordinates(lon, lat))
    for _ in range(n_relative_corners):
        lon, lat = data_buffer.read_coords_relative(lon, lat)
        corners.append(Coordinates(lon, lat))

    return PolygonLocation(corners)


def _parse_closed_line(data_buffer, size):
    n_relative_points = (size - 12) // 7

    points = []
    lon, lat = data_buffer.read_coords()
    fow, frc, bear, lfrcnp, _ = data_buffer.read_point_attributes()
    dnp = data_buffer.read_dnp()
    points.append(
        LocationReferencePoint(lon, lat, FRC(frc), FOW(fow), bear, FRC(lfrcnp), dnp)
    )

    for _ in range(n_relative_points):
        lon, lat = data_buffer.read_coords_relative(lon, lat)
        fow, frc, bear, lfrcnp, _ = data_buffer.read_point_attributes()
        dnp = data_buffer.read_dnp()
        points.append(
            LocationReferencePoint(lon, lat, FRC(frc), FOW(fow), bear, FRC(lfrcnp), dnp)
        )

    fow, frc, bear, lfrcnp, _ = data_buffer.read_point_attributes()

    return ClosedLineLocation(points, LineAttributes(FRC(frc), FOW(fow), bear))


def _write_line(location, data_buffer):
    # type: (LineLocation, OpenLRBytesIO) -> None
    point = location.points[0]
    data_buffer.write_coords(point.lon, point.lat)
    data_buffer.write_point_attributes(
        point.fow.value, point.frc.value, point.bear, point.lfrcnp.value, 0
    )
    data_buffer.write_dnp(point.dnp)
    prev_lon, prev_lat = point.lon, point.lat
    for point in location.points[1:-1]:
        data_buffer.write_coords_relative(point.lon, point.lat, prev_lon, prev_lat)
        data_buffer.write_point_attributes(
            point.fow.value, point.frc.value, point.bear, point.lfrcnp.value, 0
        )
        data_buffer.write_dnp(point.dnp)
        prev_lon, prev_lat = point.lon, point.lat
    point = location.points[-1]
    data_buffer.write_coords_relative(point.lon, point.lat, prev_lon, prev_lat)
    offset_flags = ((location.poffs > 0) << 1) + int(location.noffs > 0)
    data_buffer.write_point_attributes(
        point.fow.value, point.frc.value, point.bear, offset_flags, 0
    )
    if location.poffs > 0:
        data_buffer.write_offset(location.poffs)
    if location.noffs > 0:
        data_buffer.write_offset(location.noffs)


def _write_geo_coordinate(location, data_buffer):
    # type: (GeoCoordinateLocation, OpenLRBytesIO) -> None
    data_buffer.write_coords(location.point.lon, location.point.lat)


def _write_point_along_line(location, data_buffer):
    # type: (PointAlongLineLocation, OpenLRBytesIO) -> None
    point = location.points[0]
    data_buffer.write_coords(point.lon, point.lat)
    data_buffer.write_point_attributes(
        point.fow.value,
        point.frc.value,
        point.bear,
        point.lfrcnp.value,
        location.orientation.value,
    )
    data_buffer.write_dnp(point.dnp)
    prev_lon, prev_lat = point.lon, point.lat
    point = location.points[-1]
    offset_flags = (location.poffs > 0) << 1
    data_buffer.write_coords_relative(point.lon, point.lat, prev_lon, prev_lat)
    data_buffer.write_point_attributes(
        point.fow.value,
        point.frc.value,
        point.bear,
        offset_flags,
        location.sideOfRoad.value,
    )
    if location.poffs > 0:
        data_buffer.write_offset(location.poffs)


def _write_poi(location, data_buffer):
    # type: (PoiWithAccessPointLocation, OpenLRBytesIO) -> None
    _write_point_along_line(location, data_buffer)
    prev_lon, prev_lat = location.points[0].lon, location.points[0].lat
    data_buffer.write_coords_relative(location.lon, location.lat, prev_lon, prev_lat)


def _write_circle(location, data_buffer):
    # type: (CircleLocation, OpenLRBytesIO) -> None
    data_buffer.write_coords(location.point.lon, location.point.lat)
    data_buffer.write_radius(location.radius)


def _write_rectangle(location, data_buffer):
    # type: (RectangleLocation, OpenLRBytesIO) -> None
    data_buffer.write_coords(location.lowerLeft.lon, location.lowerLeft.lat)
    try:
        data_buffer.write_coords_relative(
            location.upperRight.lon,
            location.upperRight.lat,
            location.lowerLeft.lon,
            location.lowerLeft.lat,
        )
    except ValueError:
        data_buffer.write_coords(location.upperRight.lon, location.upperRight.lat)


def _write_grid(location, data_buffer):
    # type: (GridLocation, OpenLRBytesIO) -> None
    _write_rectangle(location, data_buffer)
    data_buffer.write_cols_rows(location.n_cols, location.n_rows)


def _write_polygon(location, data_buffer):
    # type: (PolygonLocation, OpenLRBytesIO) -> None
    point = location.corners[0]
    data_buffer.write_coords(point.lon, point.lat)
    prev_lon, prev_lat = point.lon, point.lat
    for point in location.corners[1:]:
        data_buffer.write_coords_relative(point.lon, point.lat, prev_lon, prev_lat)
        prev_lon, prev_lat = point.lon, point.lat


def _write_closed_line(location, data_buffer):
    # type: (ClosedLineLocation, OpenLRBytesIO) -> None
    point = location.points[0]
    data_buffer.write_coords(point.lon, point.lat)
    data_buffer.write_point_attributes(
        point.fow.value, point.frc.value, point.bear, point.lfrcnp.value, 0
    )
    data_buffer.write_dnp(point.dnp)
    prev_lon, prev_lat = point.lon, point.lat
    for point in location.points[1:]:
        data_buffer.write_coords_relative(point.lon, point.lat, prev_lon, prev_lat)
        data_buffer.write_point_attributes(
            point.fow.value, point.frc.value, point.bear, point.lfrcnp.value, 0
        )
        data_buffer.write_dnp(point.dnp)
        prev_lon, prev_lat = point.lon, point.lat

    data_buffer.write_point_attributes(
        location.lastLine.fow.value,
        location.lastLine.frc.value,
        location.lastLine.bear,
        0,
        0,
    )
