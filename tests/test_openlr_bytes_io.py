# Copyright (C) 2012-2021, TomTom (http://tomtom.com).
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
from openlr.openlr_bytes_io import OpenLRBytesIO
from openlr.openlr_bytes_io import deg_to_int, int_to_deg
from openlr.openlr_bytes_io import bytes_to_int, int_to_bytes

from .openlr_base_test_case import OpenlrBaseTestCase, OFFSET_DELTA, DEG_DELTA


class TestOpenLRBytesIO(OpenlrBaseTestCase):
    __name__ = "testing OpenLRBytesIO class and related conversion methods"

    def test_bytes_to_int(self):
        self.assertEqual(bytes_to_int(bytearray(b"\x00\x00")), 0)
        self.assertEqual(bytes_to_int(bytearray(b"\x00\x01")), 1)
        self.assertEqual(bytes_to_int(bytearray(b"\x01\x00")), 256)
        self.assertEqual(bytes_to_int(bytearray(b"\xff\xff\xff")), -1)
        self.assertEqual(bytes_to_int(bytearray(b"\xff\xff")), -1)
        self.assertEqual(bytes_to_int(bytearray(b"\xff")), -1)
        self.assertEqual(bytes_to_int(bytearray(b"\xff"), signed=False), 255)

    def test_int_to_bytes(self):
        # Signed int edge cases
        self.assertEqual(bytearray(b"\x7f\xff"), int_to_bytes(32767, size=2))
        self.assertRaisesRegex(
            ValueError, "signed int requires", int_to_bytes, 32768, size=1
        )
        self.assertEqual(bytearray(b"\x80\x00"), int_to_bytes(-32768, size=2))
        self.assertRaisesRegex(
            ValueError, "signed int requires", int_to_bytes, -32769, size=1
        )
        # Unsigned int edge cases
        self.assertEqual(bytearray(b"\xff"), int_to_bytes(255, size=1, signed=False))
        self.assertRaisesRegex(
            ValueError, "signed int requires", int_to_bytes, 256, size=1, signed=False
        )
        self.assertEqual(bytearray(b"\x00"), int_to_bytes(0, size=1, signed=False))
        self.assertRaisesRegex(
            ValueError, "signed int requires", int_to_bytes, -1, size=1, signed=False
        )
        self.assertRaisesRegex(
            ValueError, "not integer", int_to_bytes, 0.1, size=1, signed=False
        )
        # additional examples
        self.assertEqual(bytearray(b"\x80\x01"), int_to_bytes(-32767, size=2))
        self.assertEqual(bytearray(b"\x80\x80"), int_to_bytes(-32640, size=2))
        self.assertEqual(bytearray(b"\xff"), int_to_bytes(-1, size=1))
        self.assertEqual(bytearray(b"\xff\xff"), int_to_bytes(-1, size=2))
        self.assertEqual(bytearray(b"\xff\xff\xff"), int_to_bytes(-1, size=3))
        self.assertEqual(bytearray(b"\xff\xff\xff\xff"), int_to_bytes(-1, size=4))
        self.assertEqual(bytes_to_int(int_to_bytes(31468)), 31468)
        self.assertEqual(bytes_to_int(int_to_bytes(237680)), 237680)

    def test_deg_int_conversion(self):
        self.assertEqual(deg_to_int(int_to_deg(31468)), 31468)
        self.assertEqual(deg_to_int(int_to_deg(237680)), 237680)
        self.assertEqual(deg_to_int(int_to_deg(-3445632)), -3445632)
        self.assertEqual(deg_to_int(int_to_deg(-1)), -1)
        for x in [52.5200066, 13.404954, -5.0989758, 40.730610, -73.935242]:
            self.assertAlmostEqual(int_to_deg(deg_to_int(x)), x, delta=DEG_DELTA)

    def assert_write_and_read(self, function_name, size, *args):
        """
        Asserting writing given args and reading back

        Parameters
        ----------
        function_name : str
            function name to call read_function_name(*args) and read_function_name()
        size : int
            number of bytes for this read and write operation
        """
        stream = OpenLRBytesIO()
        getattr(stream, "write_" + function_name)(*args)
        self.assertEqual(stream.tell(), size, msg="written byte size is not matching")
        stream.seek(0)
        if len(args) == 1:
            args = args[0]
        result = getattr(stream, "read_" + function_name)()
        self.assertEqual(result, args)

    def test_status(self):
        # rfu=0, location=1011, version=011
        s = OpenLRBytesIO(bytes([0b01011011]))
        self.assertEqual(s.read_status(), (3, 11))
        self.assert_write_and_read("status", 1, 3, 11)
        self.assert_write_and_read("status", 1, 3, 8)
        self.assert_write_and_read("status", 1, 2, 1)
        self.assert_write_and_read("status", 1, 2, 7)

    def test_offset(self):
        s = OpenLRBytesIO(bytes(b"\x55"))
        self.assertAlmostEqual(s.read_offset(), 0.33398438)
        # not allowed offset
        with self.assertRaises(ValueError) as cm:
            s = OpenLRBytesIO()
            s.write_offset(1)
        for i in range(0, 1000, 1):
            offset = float(i) / 1000.0
            s = OpenLRBytesIO()
            s.write_offset(offset)
            s.seek(0)
            self.assertAlmostEqual(offset, s.read_offset(), delta=OFFSET_DELTA)

    def test_dnp(self):
        s = OpenLRBytesIO(bytes(b"\x09"))
        self.assertEqual(s.read_dnp(), 557)
        for dnp in [147, 440, 615, 674, 733, 1729, 2725, 6475, 11339, 13156, 14562]:
            self.assert_write_and_read("dnp", 1, dnp)

    def test_point_attributes(self):
        # test reading
        s = OpenLRBytesIO(b"\x1a\x6c")
        self.assertEqual(s.read_point_attributes(), (2, 3, 141, 3, 0))
        s = OpenLRBytesIO(b"\x1c\x62")
        self.assertEqual(s.read_point_attributes(), (4, 3, 28, 3, 0))
        # test reading & writing
        self.assert_write_and_read("point_attributes", 2, 2, 3, 141, 3, 0)
        self.assert_write_and_read("point_attributes", 2, 4, 3, 6, 2, 1)
        self.assert_write_and_read("point_attributes", 2, 1, 2, 354, 3, 3)
        # not allowed bearing
        with self.assertRaises(ValueError) as cm:
            s = OpenLRBytesIO()
            s.write_point_attributes(1, 2, 360, 3, 3)

    def test_coords(self):
        # test reading
        examples = [
            (b"\x03\xa0\x71\x25\x0d\x1a", 5.100070238089084, 52.10320830320309),
            (b"\xfd\xa5\x24\x27\xc8\x88", -3.3115947246393604, 55.94529032680538),
            (b"\xfc\x5f\xc2\x23\x1c\xe5", -5.098975896811013, 49.37746167159377),
            (b"\x00\x7a\xec\x21\xae\x91", 0.675219297405838, 47.36516118027036),
        ]
        for b, expected_lon, expected_lat in examples:
            s = OpenLRBytesIO(bytes(b))
            lon, lat = s.read_coords()
            self.assertAlmostEqual(lon, expected_lon)
            self.assertAlmostEqual(lat, expected_lat)
        # test writing & reading back
        examples = [
            (41.030143, 28.977417),
            (50.749673, 7.099048),
            (21.173398, -86.828102),
            (43.259594, 76.940854),
            (-27.22775, 153.11216),
            (48.068831, 12.858026),
            (-33.22979, -60.32423),
        ]
        for expected_lon, expected_lat in examples:
            s = OpenLRBytesIO()
            s.write_coords(expected_lon, expected_lat)
            self.assertEqual(s.tell(), 6)
            s.seek(0)
            lon, lat = s.read_coords()
            self.assertAlmostEqual(lon, expected_lon, delta=DEG_DELTA)
            self.assertAlmostEqual(lat, expected_lat, delta=DEG_DELTA)

    def test_relative_coords(self):
        # relative coordinate presicion is logarithmically  coralated to
        # the distance from the previous coordinate
        example_line = [
            (b"\xd5\x17\x20\x43", 6.4856483, 48.1540304),
            (b"\xff\xbb\x05\xd4", 6.4849583, 48.1689504),
            (b"\xdb\x5f\x24\x03", 6.3911883, 48.2611404),
            (b"\xfe\x91\x01\xf0", 6.3875183, 48.2661004),
            (b"\xff\xeb\x00\x1d", 6.3873083, 48.2663904),
            (b"\xe2\xeb\x1d\xcb", 6.3128583, 48.3426604),
            (b"\xf7\xfc\x07\xd8", 6.2923383, 48.3627404),
            (b"\xfb\x5d\x02\x38", 6.2804683, 48.3684204),
            (b"\xfd\x44\x00\x86", 6.2734683, 48.3697604),
            (b"\xf0\x2e\x10\xdd", 6.2329683, 48.4129304),
            (b"\x03\xde\x1b\xd9", 6.2428683, 48.4842204),
            (b"\xfe\xd0\x02\x56", 6.2398283, 48.4902004),
            (b"\xeb\x65\x19\xd9", 6.1870783, 48.5563704),
        ]
        example_first_lon, example_first_lat = 6.5954983, 48.0714404
        # test reading from bytes
        prev_lon, prev_lat = example_first_lon, example_first_lat
        for b, expected_lon, expected_lat in example_line:
            s = OpenLRBytesIO(bytes(b))
            lon, lat = s.read_coords_relative(prev_lon, prev_lat)
            self.assertAlmostEqual(lon, expected_lon)
            self.assertAlmostEqual(lat, expected_lat)
            prev_lon, prev_lat = expected_lon, expected_lat
        # test write & read
        prev_lon, prev_lat = example_first_lon, example_first_lat
        for _, expected_lon, expected_lat in example_line:
            s = OpenLRBytesIO()
            s.write_coords_relative(expected_lon, expected_lat, prev_lon, prev_lat)
            self.assertEqual(s.tell(), 4)
            s.seek(0)
            lon, lat = s.read_coords_relative(prev_lon, prev_lat)
            self.assertAlmostEqual(lon, expected_lon)
            self.assertAlmostEqual(lat, expected_lat)
            prev_lon, prev_lat = expected_lon, expected_lat
        # max bound 0.32767 = 10^5 x 2^15
        OpenLRBytesIO().write_coords_relative(0.32767, 0, 0, 0)
        with self.assertRaises(ValueError):
            OpenLRBytesIO().write_coords_relative(0.32768, 0, 0, 0)
        # min bound -0.32768
        OpenLRBytesIO().write_coords_relative(0, -0.32768, 0, 0)
        with self.assertRaises(ValueError):
            OpenLRBytesIO().write_coords_relative(0, -0.32769, 0, 0)

    def test_radius(self):
        with self.assertRaises(ValueError) as cm:
            s = OpenLRBytesIO()
            s.write_radius(-1)
        self.assert_write_and_read("radius", 1, 0)
        self.assert_write_and_read("radius", 1, 255)
        self.assert_write_and_read("radius", 2, 256)
        self.assert_write_and_read("radius", 2, 65535)
        self.assert_write_and_read("radius", 3, 65536)
        self.assert_write_and_read("radius", 3, 16777215)
        self.assert_write_and_read("radius", 4, 16777216)
        self.assert_write_and_read("radius", 4, 4294967295)
        with self.assertRaises(ValueError) as cm:
            s = OpenLRBytesIO()
            s.write_radius(4294967296)

    def test_cols_rows(self):
        # test reading
        s = OpenLRBytesIO(b"\x00\x00\xff\xff")
        cols, rows = s.read_cols_rows()
        self.assertEqual(cols, 0)
        self.assertEqual(rows, 65535)
        self.assertEqual(s.tell(), 4)
        # test Reading & writing
        self.assert_write_and_read("cols_rows", 4, 266, 65535)
        self.assert_write_and_read("cols_rows", 4, 0, 1)
        self.assert_write_and_read("cols_rows", 4, 0, 1)
