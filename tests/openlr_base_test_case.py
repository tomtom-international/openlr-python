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
from unittest import TestCase

if not hasattr(TestCase, "assertRaisesRegex"):
    TestCase.assertRaisesRegex = TestCase.assertRaisesRegexp

DEG_DELTA = 180.0 / (1 << 24)  # 3 bytes signed int in [-180,180]
OFFSET_DELTA = 0.5 / (1 << 8)  # 1 byte int in [0,1]


class OpenlrBaseTestCase(TestCase):

    __name__ = "base test case for OpenLR specific utilities"

    def _assert_coordinate(self, first, second):
        self.assertAlmostEqual(first.lon, second.lon, delta=DEG_DELTA)
        self.assertAlmostEqual(first.lat, second.lat, delta=DEG_DELTA)

    def _assert_line_attributes(self, first, second):
        self.assertEqual(first.frc, second.frc)
        self.assertEqual(first.fow, second.fow)
        self.assertEqual(first.bear, second.bear)

    def _assert_location_reference_point(self, first, second):
        self._assert_coordinate(first, second)
        self._assert_line_attributes(first, second)
        self.assertEqual(first.lfrcnp, second.lfrcnp)
        self.assertAlmostEqual(first.dnp, second.dnp, delta=0)

    def assert_locations(self, first, second):
        """asserts two locations are equal based on the defined accuracy"""
        self.assertIs(type(first), type(second))
        if hasattr(first, "points"):
            self.assertEqual(
                len(first.points),
                len(second.points),
                msg="len(first.points) != len(second.points)",
            )
            for f, s in zip(first.points, second.points):
                self._assert_location_reference_point(f, s)
        if hasattr(first, "point"):
            self._assert_coordinate(first.point, second.point)
        if hasattr(first, "poffs"):
            self.assertAlmostEqual(first.poffs, second.poffs, delta=OFFSET_DELTA)
        if hasattr(first, "noffs"):
            self.assertAlmostEqual(first.noffs, second.noffs, delta=OFFSET_DELTA)
        if hasattr(first, "orientation"):
            self.assertEqual(first.orientation, second.orientation)
        if hasattr(first, "sideOfRoad"):
            self.assertEqual(first.sideOfRoad, second.sideOfRoad)
        if hasattr(first, "lon"):
            self._assert_coordinate(first, second)
        if hasattr(first, "radius"):
            self.assertEqual(first.radius, second.radius)
        if hasattr(first, "lowerLeft"):
            self._assert_coordinate(first.lowerLeft, second.lowerLeft)
        if hasattr(first, "upperRight"):
            self._assert_coordinate(first.upperRight, second.upperRight)
        if hasattr(first, "n_cols"):
            self.assertEqual(first.n_cols, second.n_cols)
        if hasattr(first, "n_rows"):
            self.assertEqual(first.n_rows, second.n_rows)
        if hasattr(first, "corners"):
            self.assertEqual(
                len(first.corners),
                len(second.corners),
                msg="len(first.corners) != len(second.corners)",
            )
            for f, s in zip(first.corners, second.corners):
                self._assert_coordinate(f, s)

        if hasattr(first, "lastLine"):
            self._assert_line_attributes(first.lastLine, second.lastLine)
