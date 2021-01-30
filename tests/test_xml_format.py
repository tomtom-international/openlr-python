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
import os

from openlr import xml_decode_file, xml_decode_string, xml_encode_to_string

from .openlr_base_test_case import OpenlrBaseTestCase
from .data import LOCATIONS


class TestXMLFormat(OpenlrBaseTestCase):
    __name__ = "testing XML physical format for encoder/decoder"

    def test_decoding_xml_examples(self):
        for name, _, location in LOCATIONS:
            filename = os.path.join(
                os.path.dirname(__file__), "xml_data", name + ".xml"
            )
            result = xml_decode_file(filename)
            try:
                self.assert_locations(result, location)
            except AssertionError:
                print("failed input: " + name)
                raise

    def test_encoding_xml_examples(self):
        example_folder = os.path.join(os.path.dirname(__file__), "xml_data")
        for name, _, location in LOCATIONS:
            try:
                xml_string = xml_encode_to_string(location, is_pretty=False)
                parsed_location = xml_decode_string(xml_string)
                self.assert_locations(location, parsed_location)
            except AssertionError:
                print("failed input: " + name)
                print(xml_string)
                print(parsed_location)
                raise

    def test_encoding_xml_pretty(self):
        location = LOCATIONS[0][2]
        xml_string = xml_encode_to_string(location, is_pretty=True)
        parsed_location = xml_decode_string(xml_string)
        self.assert_locations(location, parsed_location)
