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
from xml.dom import minidom
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
from openlr.utils import j_round

NAMESPACE_URI = "http://www.openlr.org/openlr"
# hierarchy = {
#     "XMLLocationReference": {
#         "LineLocationReference": LineLocation,
#         "PointLocationReference": {
#             "GeoCoordinate": GeoCoordinateLocation,
#             "PointAlongLine": PointAlongLineLocation,
#             "PoiWithAccessPoint": PoiWithAccessPointLocation,
#         },
#         "AreaLocationReference": {
#             "CircleLocationReference": CircleLocation,
#             "RectangleLocationReference": RectangleLocation,
#             "GridLocationReference": GridLocation,
#             "PolygonLocationReference": PolygonLocation,
#             "ClosedLineLocationReference": ClosedLineLocation,
#         },
#     }
# }


def xml_decode_file(filename_or_file):
    """Decodes an OpenLR XML from a filename or file object"""
    doc = minidom.parse(filename_or_file)
    return xml_decode_document(doc)


def xml_decode_string(string):
    """Decodes an OpenLR XML from string"""
    doc = minidom.parseString(string)
    return xml_decode_document(doc)


def xml_decode_document(doc):
    """Decodes OpenLR xml minidom Document into a location"""
    el_loc = _get_first_el(_get_first_el(doc, "OpenLR"), "XMLLocationReference")

    for loc_tag, el_child_loc in _iter_children(el_loc):
        if loc_tag == "LineLocationReference":
            return _parse_line(el_child_loc)
        elif loc_tag == "PointLocationReference":
            for point_tag, el_point_loc in _iter_children(el_child_loc):
                if point_tag == "GeoCoordinate":
                    return _parse_geo_coordinate(el_point_loc)
                elif point_tag == "PointAlongLine":
                    return _parse_point_along_line(el_point_loc)
                elif point_tag == "PoiWithAccessPoint":
                    return _parse_poi(el_point_loc)
                else:
                    raise ValueError(
                        "Not a known point location: %r in %r"
                        % (point_tag, el_child_loc)
                    )
        elif loc_tag == "AreaLocationReference":
            for area_tag, el_area_loc in _iter_children(el_child_loc):
                if area_tag == "CircleLocationReference":
                    return _parse_circle(el_area_loc)
                elif area_tag == "RectangleLocationReference":
                    return _parse_rectangle(el_area_loc)
                elif area_tag == "GridLocationReference":
                    return _parse_grid(el_area_loc)
                elif area_tag == "PolygonLocationReference":
                    return _parse_polygon(el_area_loc)
                elif area_tag == "ClosedLineLocationReference":
                    return _parse_closed_line(el_area_loc)
                else:
                    raise ValueError(
                        "Not a known area location: %r in %r" % (area_tag, el_child_loc)
                    )
    raise ValueError("No Valid OpenLR LocationReference found")


def xml_encode_to_string(location, is_pretty=True):
    """Encodes location object into an OpenLR XML string"""
    doc = xml_encode_to_document(location)
    return doc.toprettyxml(indent="  ") if is_pretty else doc.toxml()


def xml_encode_to_document(location):
    """Encodes location object to OpenLR xml minidom document"""

    doc = minidom.Document()
    root = doc.createElement("OpenLR")
    root.setAttribute("xmlns", NAMESPACE_URI)
    el_id = doc.createElement("LocationID")
    el_id.appendChild(doc.createTextNode(""))
    el_loc = doc.createElement("XMLLocationReference")
    root.appendChild(el_id)
    root.appendChild(el_loc)
    doc.appendChild(root)

    if isinstance(location, LineLocation):
        el_loc_type = doc.createElement("LineLocationReference")
        el_loc.appendChild(el_loc_type)
        _write_line(doc, el_loc_type, location)
    elif isinstance(location, GeoCoordinateLocation):
        el_loc_type = doc.createElement("PointLocationReference")
        el_loc.appendChild(el_loc_type)
        el_geo = doc.createElement("GeoCoordinate")
        el_loc_type.appendChild(el_geo)
        _write_geo_coordinate(doc, el_geo, location)
    elif isinstance(location, PointAlongLineLocation):
        el_loc_type = doc.createElement("PointLocationReference")
        el_loc.appendChild(el_loc_type)
        el_point_along_line = doc.createElement("PointAlongLine")
        el_loc_type.appendChild(el_point_along_line)
        _write_point_along_line(doc, el_point_along_line, location)
    elif isinstance(location, PoiWithAccessPointLocation):
        el_loc_type = doc.createElement("PointLocationReference")
        el_loc.appendChild(el_loc_type)
        el_poi = doc.createElement("PoiWithAccessPoint")
        el_loc_type.appendChild(el_poi)
        _write_poi(doc, el_poi, location)
    elif isinstance(location, CircleLocation):
        el_loc_type = doc.createElement("AreaLocationReference")
        el_loc.appendChild(el_loc_type)
        el_circle = doc.createElement("CircleLocationReference")
        el_loc_type.appendChild(el_circle)
        _write_circle(doc, el_circle, location)
    elif isinstance(location, RectangleLocation):
        el_loc_type = doc.createElement("AreaLocationReference")
        el_loc.appendChild(el_loc_type)
        el_rectangle = doc.createElement("RectangleLocationReference")
        el_loc_type.appendChild(el_rectangle)
        _write_rectangle(doc, el_rectangle, location)
    elif isinstance(location, GridLocation):
        el_loc_type = doc.createElement("AreaLocationReference")
        el_loc.appendChild(el_loc_type)
        el_grid = doc.createElement("GridLocationReference")
        el_loc_type.appendChild(el_grid)
        _write_grid(doc, el_grid, location)
    elif isinstance(location, PolygonLocation):
        el_loc_type = doc.createElement("AreaLocationReference")
        el_loc.appendChild(el_loc_type)
        el_polygon = doc.createElement("PolygonLocationReference")
        el_loc_type.appendChild(el_polygon)
        _write_polygon(doc, el_polygon, location)
    elif isinstance(location, ClosedLineLocation):
        el_loc_type = doc.createElement("AreaLocationReference")
        el_loc.appendChild(el_loc_type)
        el_closed_line = doc.createElement("ClosedLineLocationReference")
        el_loc_type.appendChild(el_closed_line)
        _write_closed_line(doc, el_closed_line, location)
    else:
        raise ValueError("object %r is not a Location type" % (location,))
    return doc


def _iter_children(el):
    for child in el.childNodes:
        if not isinstance(child, minidom.Element) or not child.childNodes:
            continue
        tag = child.tagName.split(":")[-1]
        yield tag, child


def _get_first_el(el, tag):
    res = el.getElementsByTagNameNS("*", tag)
    if res:
        return res[0]
    else:
        raise ValueError("Tag not found: %r in %r" % (tag, el))


def _get_el_value(el, tag, default=None):
    res = el.getElementsByTagNameNS("*", tag)
    if res:
        return res[0].firstChild.data
    if default is None:
        raise ValueError("Tag not found: %r in %r" % (tag, el))
    return default


def _parse_point(el):
    lon = float(_get_el_value(el, "Longitude"))
    lat = float(_get_el_value(el, "Latitude"))
    frc = FRC[_get_el_value(el, "FRC")]
    fow = FOW[_get_el_value(el, "FOW")]
    bear = int(_get_el_value(el, "BEAR"))
    lfrcnp = FRC[_get_el_value(el, "LFRCNP", "FRC7")]
    dnp = int(_get_el_value(el, "DNP", 0))
    return LocationReferencePoint(lon, lat, frc, fow, bear, lfrcnp, dnp)


def _parse_coordinate(el):
    lon = float(_get_el_value(el, "Longitude"))
    lat = float(_get_el_value(el, "Latitude"))
    return Coordinates(lon, lat)


def _parse_line(el):
    point_elements = el.getElementsByTagNameNS("*", "LocationReferencePoint")
    point_elements += el.getElementsByTagNameNS("*", "LastLocationReferencePoint")
    points = [_parse_point(e) for e in point_elements]
    poffs = float(_get_el_value(el, "PosOff", 0)) / points[0].dnp
    noffs = float(_get_el_value(el, "NegOff", 0)) / points[-2].dnp
    return LineLocation(points, poffs, noffs)


def _parse_geo_coordinate(el):
    point = _parse_coordinate(_get_first_el(el, "Coordinates"))
    return GeoCoordinateLocation(point)


def _parse_point_along_line(el):
    point_elements = el.getElementsByTagNameNS("*", "LocationReferencePoint")
    point_elements += el.getElementsByTagNameNS("*", "LastLocationReferencePoint")
    points = [_parse_point(e) for e in point_elements]
    poffs = float(_get_el_value(el, "PosOff", 0)) / points[0].dnp
    orientation = Orientation[_get_el_value(el, "Orientation")]
    sideOfRoad = SideOfRoad[_get_el_value(el, "SideOfRoad")]
    return PointAlongLineLocation(points, poffs, orientation, sideOfRoad)


def _parse_poi(el):
    pal = _parse_point_along_line(el)
    for child_tag, el_child in _iter_children(el):
        if child_tag == "Coordinates":
            lon = float(_get_el_value(el_child, "Longitude"))
            lat = float(_get_el_value(el_child, "Latitude"))
            break
    else:
        raise ValueError("no Coordinates element found for PoiWithAccessPoint")
    return PoiWithAccessPointLocation(
        pal.points, pal.poffs, lon, lat, pal.orientation, pal.sideOfRoad
    )


def _parse_circle(el):
    point = _parse_coordinate(_get_first_el(el, "Coordinates"))
    radius = int(_get_el_value(el, "Radius"))
    return CircleLocation(point, radius)


def _parse_rectangle(el):
    lowerLeft = _parse_coordinate(_get_first_el(el, "LowerLeft"))
    upperRight = _parse_coordinate(_get_first_el(el, "UpperRight"))
    return RectangleLocation(lowerLeft, upperRight)


def _parse_grid(el):
    rectangle = _parse_rectangle(el)
    cols = int(_get_el_value(el, "NumColumns"))
    rows = int(_get_el_value(el, "NumRows"))
    return GridLocation(rectangle.lowerLeft, rectangle.upperRight, cols, rows)


def _parse_polygon(el):
    corner_elements = el.getElementsByTagNameNS("*", "Coordinates")
    corners = [_parse_coordinate(e) for e in corner_elements]
    return PolygonLocation(corners)


def _parse_closed_line(el):
    point_elements = el.getElementsByTagNameNS("*", "LocationReferencePoint")
    points = [_parse_point(e) for e in point_elements]
    el_last_line = _get_first_el(el, "LastLine")
    frc = FRC[_get_el_value(el_last_line, "FRC")]
    fow = FOW[_get_el_value(el_last_line, "FOW")]
    bear = int(_get_el_value(el_last_line, "BEAR"))
    return ClosedLineLocation(points, LineAttributes(frc, fow, bear))


def _create_data_el(doc, tag, data):
    el = doc.createElement(tag)
    el.appendChild(doc.createTextNode(str(data)))
    return el


def _create_coordinate_el(doc, coord):
    el_coord = doc.createElement("Coordinates")
    el_coord.appendChild(_create_data_el(doc, "Longitude", coord.lon))
    el_coord.appendChild(_create_data_el(doc, "Latitude", coord.lat))
    return el_coord


def _create_point_el(doc, point):
    el_point = doc.createElement("LocationReferencePoint")
    el_point.appendChild(_create_coordinate_el(doc, point))
    el_line_attr = doc.createElement("LineAttributes")
    el_line_attr.appendChild(_create_data_el(doc, "FRC", point.frc.name))
    el_line_attr.appendChild(_create_data_el(doc, "FOW", point.fow.name))
    el_line_attr.appendChild(_create_data_el(doc, "BEAR", point.bear))
    el_point.appendChild(el_line_attr)
    el_path_attr = doc.createElement("PathAttributes")
    el_path_attr.appendChild(_create_data_el(doc, "LFRCNP", point.lfrcnp.name))
    el_path_attr.appendChild(_create_data_el(doc, "DNP", point.dnp))
    el_point.appendChild(el_path_attr)
    return el_point


def _create_last_point_el(doc, point):
    el_point = doc.createElement("LastLocationReferencePoint")
    el_point.appendChild(_create_coordinate_el(doc, point))
    el_line_attr = doc.createElement("LineAttributes")
    el_line_attr.appendChild(_create_data_el(doc, "FRC", point.frc.name))
    el_line_attr.appendChild(_create_data_el(doc, "FOW", point.fow.name))
    el_line_attr.appendChild(_create_data_el(doc, "BEAR", point.bear))
    el_point.appendChild(el_line_attr)
    return el_point


def _create_offset_el(doc, el_loc):

    if el_loc.poffs > 0:
        poffs = j_round(float(el_loc.points[0].dnp) * el_loc.poffs)
    else:
        poffs = 0

    if hasattr(el_loc, "noffs") and el_loc.noffs > 0:
        noffs = j_round(float(el_loc.points[-2].dnp) * el_loc.noffs)
    else:
        noffs = 0

    el_offset = doc.createElement("Offsets")
    el_offset.appendChild(_create_data_el(doc, "PosOff", poffs))
    el_offset.appendChild(_create_data_el(doc, "NegOff", noffs))
    return el_offset


def _write_line(doc, el_loc, location):
    for point in location.points[0:-1]:
        point_element = _create_point_el(doc, point)
        el_loc.appendChild(point_element)

    last_point_element = _create_last_point_el(doc, location.points[-1])
    el_loc.appendChild(last_point_element)
    el_offset = _create_offset_el(doc, location)
    el_loc.appendChild(el_offset)


def _write_geo_coordinate(doc, el_loc, location):
    el_loc.appendChild(_create_coordinate_el(doc, location.point))


def _write_point_along_line(doc, el_loc, location):
    first_point_element = _create_point_el(doc, location.points[0])
    el_loc.appendChild(first_point_element)
    last_point_element = _create_last_point_el(doc, location.points[-1])
    el_loc.appendChild(last_point_element)
    el_offset = _create_offset_el(doc, location)
    el_loc.appendChild(el_offset)
    el_loc.appendChild(_create_data_el(doc, "SideOfRoad", location.sideOfRoad.name))
    el_loc.appendChild(_create_data_el(doc, "Orientation", location.orientation.name))


def _write_poi(doc, el_loc, location):
    _write_point_along_line(doc, el_loc, location)
    el_loc.appendChild(_create_coordinate_el(doc, location))


def _write_circle(doc, el_loc, location):
    el_coord = doc.createElement("GeoCoordinate")
    el_coord.appendChild(_create_coordinate_el(doc, location.point))
    el_loc.appendChild(el_coord)
    el_loc.appendChild(_create_data_el(doc, "Radius", location.radius))


def _write_polygon(doc, el_loc, location):
    el_corners = doc.createElement("PolygonCorners")
    for corner in location.corners:
        el_corners.appendChild(_create_coordinate_el(doc, corner))
    el_loc.appendChild(el_corners)


def _write_rectangle(doc, el_loc, location):
    el_lowerLeft = _create_coordinate_el(doc, location.lowerLeft)
    el_lowerLeft.tagName = "LowerLeft"
    el_loc.appendChild(el_lowerLeft)
    el_upperRight = _create_coordinate_el(doc, location.upperRight)
    el_upperRight.tagName = "UpperRight"
    el_loc.appendChild(el_upperRight)


def _write_grid(doc, el_loc, location):
    el_rectangle = doc.createElement("Rectangle")
    _write_rectangle(doc, el_rectangle, location)
    el_loc.appendChild(el_rectangle)
    el_loc.appendChild(_create_data_el(doc, "NumColumns", location.n_cols))
    el_loc.appendChild(_create_data_el(doc, "NumRows", location.n_rows))


def _write_closed_line(doc, el_loc, location):
    for point in location.points:
        point_element = _create_point_el(doc, point)
        el_loc.appendChild(point_element)
    el_line_attr = doc.createElement("LastLine")
    el_line_attr.appendChild(_create_data_el(doc, "FRC", location.lastLine.frc.name))
    el_line_attr.appendChild(_create_data_el(doc, "FOW", location.lastLine.fow.name))
    el_line_attr.appendChild(_create_data_el(doc, "BEAR", location.lastLine.bear))
    el_loc.appendChild(el_line_attr)
