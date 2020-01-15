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

# fmt: off
LOCATIONS = (
("line1","CwRbWyNG9RpsCQCb/jsbtAT/6/+jK1lE",
LineLocation([
LocationReferencePoint(6.1268198,49.6085178,FRC.FRC3,FOW.MULTIPLE_CARRIAGEWAY,141,FRC.FRC3,557),
LocationReferencePoint(6.1283698,49.6039878,FRC.FRC3,FOW.SINGLE_CARRIAGEWAY,231,FRC.FRC5,264),
LocationReferencePoint(6.1281598,49.6030578,FRC.FRC5,FOW.SINGLE_CARRIAGEWAY,287,FRC.FRC7,0),],
0.26757812, 0)),
("line2","CwB67CGukRxiCACyAbwaMXU=",
LineLocation([
LocationReferencePoint(0.6752192,47.3651611,FRC.FRC3,FOW.ROUNDABOUT,28,FRC.FRC3,498),
LocationReferencePoint(0.6769992,47.3696011,FRC.FRC3,FOW.MULTIPLE_CARRIAGEWAY,197,FRC.FRC7,0)],
0, 0.45898438)),
("line3","CwcX6CItqAs6AQAAAAALGg==",
LineLocation([
LocationReferencePoint(9.9750602,48.0632865,FRC.FRC1,FOW.SINGLE_CARRIAGEWAY,298,FRC.FRC1,88),
LocationReferencePoint(9.9750602,48.0632865,FRC.FRC1,FOW.SINGLE_CARRIAGEWAY,298,FRC.FRC7,0)],
0, 0)),
("line4","CwRbWyNG9BpgAACa/jsboAD/6/+kKwA=",
LineLocation([
LocationReferencePoint(6.1268198,49.6084964,FRC.FRC3,FOW.MULTIPLE_CARRIAGEWAY,6,FRC.FRC3,29),
LocationReferencePoint(6.1283598,49.6039664,FRC.FRC3,FOW.SINGLE_CARRIAGEWAY,6,FRC.FRC5,29),
LocationReferencePoint(6.1281498,49.6030464,FRC.FRC5,FOW.SINGLE_CARRIAGEWAY,6,FRC.FRC7,0)],
0,0)),
("geo_coordinate1","I+djotZ9eA==",
GeoCoordinateLocation(Coordinates(-34.6089398, -58.3732688))),
("geo_coordinate2","IyVUdwmSoA==",
GeoCoordinateLocation(Coordinates(52.4952185, 13.4616744))),
("point_along_line1","K/6P+SKSuBJGGAUn/1gSUyM=",
PointAlongLineLocation([
LocationReferencePoint(-2.0216238,48.6184394,FRC.FRC2,FOW.MULTIPLE_CARRIAGEWAY,73,FRC.FRC2,1436),
LocationReferencePoint(-2.0084338,48.6167594,FRC.FRC2,FOW.MULTIPLE_CARRIAGEWAY,219,FRC.FRC7,0)],
0.138671875,Orientation.NO_ORIENTATION_OR_UNKNOWN,SideOfRoad.ON_ROAD_OR_UNKNOWN)),
("point_along_line2","KwBVwSCh+RRXAf/i/9AUXP8=",
PointAlongLineLocation([
LocationReferencePoint(0.4710495,45.8897316,FRC.FRC2,FOW.ROUNDABOUT,264,FRC.FRC2,88),
LocationReferencePoint(0.4707495,45.8892516,FRC.FRC2,FOW.ROUNDABOUT,321,FRC.FRC7,0)],
0.9980469,Orientation.NO_ORIENTATION_OR_UNKNOWN,SideOfRoad.ON_ROAD_OR_UNKNOWN)),
("poi1","KwOg5iUNnCOTAv+D/5QjQ1j/gP/r",
PoiWithAccessPointLocation([
LocationReferencePoint(5.1025807,52.1059978,FRC.FRC4,FOW.SINGLE_CARRIAGEWAY,219,FRC.FRC4,147), # 147
LocationReferencePoint(5.1013307,52.1049178,FRC.FRC4,FOW.SINGLE_CARRIAGEWAY,39,FRC.FRC7,0)],
0.34570312,5.1013007,52.1057878,Orientation.NO_ORIENTATION_OR_UNKNOWN,SideOfRoad.ON_ROAD_OR_UNKNOWN)),
("circle1","AwOgxCUNmwEs",
CircleLocation(Coordinates(5.1018512,52.1059763),300)),
("circle2","A/2lJCfIiAfQ",
CircleLocation(Coordinates(-3.3115947,55.9452903),2000)),
("rectangle_absolute","Qxl5HRKFDR33oB/agA==",
RectangleLocation(
Coordinates(35.8215343, 26.0433590),Coordinates(42.1414840, 44.7939956))),
("rectangle_relative","QwOgcSUNGgGIAX8=",
RectangleLocation(
Coordinates(5.1000702,52.1032083),Coordinates(5.1039902,52.1070383))),
("grid_absolute","Q/xfwiMc5QsGuyx13wILASg=",
GridLocation(
Coordinates(-5.0989758,49.3774616),Coordinates(15.5057108,62.5224745),523,296)),
("grid_relative","QwOgNiUM5wFVANsAAwAC",
GridLocation(
Coordinates(5.0988042,52.1021139),Coordinates(5.1022142,52.1043039),3,2)
),
("polygon1","EwOgUCUNEwJFAH//yAEv/vIAxw==",
PolygonLocation([
Coordinates(5.0993621,52.1030580),Coordinates(5.1051721,52.1043280),
Coordinates(5.1046171,52.1073541),Coordinates(5.1019192,52.1093396)])),
("closed_line1","WwOgrCUNaiOLBiMD",
ClosedLineLocation([
LocationReferencePoint(5.1013362,52.1049249,FRC.FRC4,FOW.SINGLE_CARRIAGEWAY,129,FRC.FRC4,381)],
LineAttributes(FRC.FRC4,FOW.SINGLE_CARRIAGEWAY,39))),
("closed_line2","WwRboCNGfhJrBAAJ/zkb9AgTFQ==",
ClosedLineLocation([
LocationReferencePoint(6.1283004,49.6059644,FRC.FRC2,FOW.MULTIPLE_CARRIAGEWAY,129,FRC.FRC3,264),
LocationReferencePoint(6.1283904,49.6039744,FRC.FRC3,FOW.SINGLE_CARRIAGEWAY,231,FRC.FRC7,498)],
LineAttributes(FRC.FRC2,FOW.SINGLE_CARRIAGEWAY,242))),
)

# fmt: on
