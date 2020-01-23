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
import decimal
import math

sgn = lambda x: math.copysign(1, x)


def j_round(float_num):
    """java like rounding for complying with the OpenLR java: 2.5 -> 3"""
    num = decimal.Decimal(float_num).to_integral_value(rounding=decimal.ROUND_HALF_UP)
    return int(num)


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


def _namedtuple_to_dict(obj):
    if hasattr(obj, "_fields"):
        dict_obj = {}
        for field in obj._fields:
            dict_obj[field] = _namedtuple_to_dict(getattr(obj, field))
        return dict_obj
    if hasattr(obj, "__iter__"):
        return [_namedtuple_to_dict(o) for o in obj]
    return obj


def get_dict(location):
    """Helper to convert location object to dict"""
    return {
        "type": location.__class__.__name__,
        "properties": _namedtuple_to_dict(location),
    }
