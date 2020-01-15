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
"""
Internal API for binary format conversion.
It provides an extended io.BytesIO stream class to read/write OpenLR binary data.
"""
import sys
from io import BytesIO
import binascii
import numbers
import math

from openlr.utils import j_round, sgn

PY2 = sys.version_info[0] == 2
DECA_MICRO_DEG_FACTOR = 100000.0
DISTANCE_PER_INTERVAL = 58.6
BEAR_SECTOR = 11.25


def deg_to_int(deg, resolution=24):
    r"""converts degree coordinate into integer

    .. math::
        \mathrm{int} = 0.5 \times \mathop{\mathrm{sgn}}(\mathrm{deg}) +
            \frac{\mathrm{deg} \times 2^{\mathrm{resolution}}}{360^{\circ}}

    Parameters
    ----------
    deg : float
        Coordinate Degree
    resolution: int
        Resolution bits of this integer, default: 3 bytes = 24

    Returns
    -------
    val : int
        Coordinate value in integer
    """
    val = sgn(deg) * 0.5 + float(deg * (1 << resolution)) / 360.0
    return j_round(val)


def int_to_deg(val, resolution=24):
    r"""converts degree coordinate into integer

    .. math::
        \DeclareMathOperator{\sgn}{sgn}
        \mathrm{deg} = \frac{
            \left ( \mathrm{int} - 0.5 \times \sgn(\mathrm{int}) \right )
            \times 360^{\circ}
        }{2^{\mathrm{resolution}}}

    Parameters
    ----------
    val : int
        Coordinate value in integer
    resolution : int
        Resolution bits of the returned integer, default: 3 bytes = 24

    Returns
    -------
    deg : float
        Coordinate value in degree
    """
    return ((val - sgn(val) * 0.5) * 360) / (1 << resolution)


def bytes_to_int(b, signed=True):
    """converts big endian bytes to signed/unsigned int"""
    resolution = len(b) * 8

    hex_b = binascii.hexlify(b)
    val = int(hex_b, 16)
    if signed and b[0] >> 7:
        val -= 1 << resolution
    return val


def int_to_bytes(val, size=3, signed=True):
    """positive/negative int values to big endian"""
    if not isinstance(val, numbers.Integral):
        raise ValueError("%s is not integer" % val)
    max_range = 1 << 8 * size
    if signed:
        if val >= (max_range / 2) or val < -(max_range / 2):
            raise ValueError(
                "%s bytes signed int requires %s <= number <= %s but number = %s"
                % (size, -(max_range // 2), (max_range // 2) - 1, val)
            )
    else:
        if val < 0 or val >= max_range:
            raise ValueError(
                "%s byte(s) unsigned int requires 0 <= number <= %s but number = %s"
                % (size, max_range - 1, val)
            )
    if val < 0:
        val += max_range
    arr = []
    for i in range(size):
        val, reminder = divmod(val, 256)
        arr.append(reminder)
    return bytearray(reversed(arr))


class OpenLRBytesIO(BytesIO):
    """In-memory binary stream for reading/writing OpenLR data"""

    def read(self, size=-1):
        """Python 2 compatibility for str -> bytes"""
        bytes = super(OpenLRBytesIO, self).read(size)
        if PY2:
            return bytearray(bytes)
        else:
            return bytes

    def read_status(self):
        """Reads status from the first byte: version & location type

        Returns
        -------
        version : int
            OpenLR version: 3 bit
        location_type : int
            Combination of Point flag, Area flag & Attributes flag: 4 bit
        """
        status = self.read(1)[0]
        version = status & 7
        location_type = (status >> 3) & 0b1111
        return version, location_type

    def read_offset(self):
        """Reads offset rate from the stream, 1 byte

        Returns
        -------
        offset : float
            offset rate in [0,1] range
        """
        bucket_index = bytes_to_int(self.read(1), signed=False)
        offset = (float(bucket_index) + 0.5) / 256
        return offset

    def read_dnp(self):
        """Reads distance to next point from the buffer, 1 byte

        Returns
        -------
        dnp : int
            Distance to next point
        """
        interval = bytes_to_int(self.read(1), signed=False)
        dnp = (float(interval) + 0.5) * DISTANCE_PER_INTERVAL
        dnp = j_round(dnp)
        return dnp

    def read_point_attributes(self):
        """Reads point attributes from the buffer, 2 bytes

        Returns
        -------
        fow : int
            form of way (3 bits)
        frc : int
            functional road class (3 bits)
        bear : int
            Bearing (5 bits)
        lfrcnp : int
            Lowest FRC to next point or offset flags (3 bits)
        reserved : int
            mostly reserved for future use or Orientation/SideOfRoad (2 bits)
        """
        first_b, second_b = self.read(2)
        fow = first_b & 0b111
        frc = (first_b >> 3) & 0b111
        reserved = (first_b >> 6) & 0b11
        bear = (second_b & 0b11111) * BEAR_SECTOR + BEAR_SECTOR / 2
        bear = j_round(bear)
        lfrcnp = (second_b >> 5) & 0b111
        return fow, frc, bear, lfrcnp, reserved

    def read_coords(self):
        """Reads absolute coordinates from the buffer, 6 bytes

        Returns
        -------
        lon : float
            Longitude
        lat : float
            Latitude
        """
        lon_int = bytes_to_int(self.read(3))
        lat_int = bytes_to_int(self.read(3))
        lon = int_to_deg(lon_int)
        lat = int_to_deg(lat_int)
        return lon, lat

    def read_coords_relative(self, prev_lon, prev_lat):
        """Reads coordinates from the buffer relative to the previous ones, 4 bytes

        Parameters
        ----------
        prev_lon : float
            Previous Longitude
        prev_lat : float
            Previous Latitude

        Returns
        -------
        lon : float
            Longitude
        lat : float
            Latitude
        """
        rel_lon = bytes_to_int(self.read(2))
        rel_lat = bytes_to_int(self.read(2))
        lon = prev_lon + rel_lon / DECA_MICRO_DEG_FACTOR
        lat = prev_lat + rel_lat / DECA_MICRO_DEG_FACTOR
        return lon, lat

    def read_radius(self):
        """Reads an integer from the remaining bytes till the end

        Returns
        -------
        radius : int
            integer value
        """
        return bytes_to_int(self.read(-1), signed=False)

    def read_cols_rows(self):
        """Reads the number of columns and rows, 4 bytes

        Returns
        -------
        cols : int
        rows : int
        """
        cols = bytes_to_int(self.read(2), signed=False)
        rows = bytes_to_int(self.read(2), signed=False)
        return cols, rows

    def write_status(self, version, location_type):
        """Writes status byte to the stream

        Parameters
        ----------
        version : int
            OpenLR version (3 bit)
        location_type : int
            Combination of Point, Area and Attribute flags (4 bit)
        """
        version &= 0b111
        location_type &= 0b1111
        byte_int = version + (location_type << 3)
        self.write(int_to_bytes(byte_int, size=1, signed=False))

    def write_offset(self, offset):
        """Writes offset rate to the stream, 1 byte

        Parameters
        ----------
        offset : float
            offset rate in [0,1] range
        """
        if offset < 0 or offset >= 1:
            raise ValueError("offset requires 0 <= x < 1 but %s is given" % offset)
        elif offset == 0:
            bucket_index = 0
        else:
            bucket_index = float(offset) * 256 - 0.5
            bucket_index = j_round(bucket_index)
        self.write(int_to_bytes(bucket_index, size=1, signed=False))

    def write_dnp(self, dnp):
        """Writes distance to next point to the stream, 1 byte

        Parameters
        ----------
        dnp : int
            distance to next point
        """
        interval = float(dnp) / DISTANCE_PER_INTERVAL - 0.5
        interval = j_round(interval)
        self.write(int_to_bytes(interval, size=1, signed=False))

    def write_point_attributes(self, fow, frc, bear, lfrcnp, reserved):
        """Writes 2 bytes point attributes to the stream

        Parameters
        ----------
        fow :
            form of way (3 bits)
        frc : int
            functional road class (3 bits)
        bear : int
            Bearing (5 bits)
        lfrcnp : int
            Lowest FRC to next point or offset flags (3 bits)
        reserved : int
            mostly reserved for future use or Orientation/SideOfRoad (2 bits)
        """
        if bear < 0 or bear >= 360:
            raise ValueError(
                "Bearing angle requires 0 <= x < 360 but %s is given" % bear
            )
        bear = (bear - BEAR_SECTOR / 2) / BEAR_SECTOR
        bear = j_round(bear)
        fow = fow & 0b111
        frc = frc & 0b111
        bear = bear & 0b11111
        lfrcnp = lfrcnp & 0b111
        reserved = reserved & 0b11
        byte_int = fow + (frc << 3) + (reserved << 6)
        self.write(int_to_bytes(byte_int, size=1, signed=False))
        byte_int = bear + (lfrcnp << 5)
        self.write(int_to_bytes(byte_int, size=1, signed=False))

    def write_coords(self, lon, lat):
        """Writes the absolute coordinates to the stream, 6 bytes

        Parameters
        ----------
        lon : float
            Longitude to be written
        lat : float
            Latitude to be written
        """
        lon_int = deg_to_int(lon)
        lat_int = deg_to_int(lat)
        self.write(int_to_bytes(lon_int, size=3) + int_to_bytes(lat_int, size=3))

    def write_coords_relative(self, lon, lat, prev_lon, prev_lat):
        """Writes the relative coordinates to the stream, 4 bytes

        Parameters
        ----------
        lon : float
            Longitude to be written
        lat : float
            Latitude to be written
        prev_lon : float
            Previous Longitude
        prev_lat : float
            Previous Latitude
        """
        rel_lon = j_round(DECA_MICRO_DEG_FACTOR * (lon - prev_lon))
        rel_lat = j_round(DECA_MICRO_DEG_FACTOR * (lat - prev_lat))
        self.write(int_to_bytes(rel_lon, size=2) + int_to_bytes(rel_lat, size=2))

    def write_radius(self, radius):
        """Writes the radius, 1-4 bytes depending on the value size

        Parameters
        ----------
        radius : int
            Radius value in [0, 4294967295] range
        """
        if radius < 0:
            raise ValueError("Radius cannot be negative, given value %s" % radius)
        elif radius == 0:
            size = 1
        elif radius > 4294967295:
            raise ValueError(
                "Radius cannot be larger than 4294967295, given value %s" % radius
            )
        else:
            size = 1 + int(math.log(radius, 2) // 8)
        self.write(int_to_bytes(radius, size=size, signed=False))

    def write_cols_rows(self, cols, rows):
        """Writes the number of columns and rows, 4 bytes

        Parameters
        ----------
        cols : int
        rows : int
        """
        int_to_bytes(cols, size=2, signed=False)
        self.write(
            int_to_bytes(cols, size=2, signed=False)
            + int_to_bytes(rows, size=2, signed=False)
        )
