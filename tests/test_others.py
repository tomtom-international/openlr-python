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
import openlr

from .openlr_base_test_case import OpenlrBaseTestCase
from .data import LOCATIONS


class TestXMLFormat(OpenlrBaseTestCase):
    __name__ = "testing the rest of the functionalities"

    def test_get_lonlat_list(self):
        for name, _, location in LOCATIONS:
            lonlat_list = openlr.get_lonlat_list(location)
            self.assertNotEqual(len(lonlat_list), 0, msg="no latlon for " + name)

    def test_get_dict(self):
        for name, _, location in LOCATIONS:
            location_dict = openlr.get_dict(location)
            self.assertIsNotNone(location_dict)
