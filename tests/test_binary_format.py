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
from openlr import binary_decode, binary_encode

from .openlr_base_test_case import OpenlrBaseTestCase
from .data import LOCATIONS


class TestBinaryFormat(OpenlrBaseTestCase):
    __name__ = "testing binary physical format for encode/decode"

    def test_decoding_binary_examples(self):
        for _, data, location in LOCATIONS:
            result = binary_decode(data)
            try:
                self.assert_locations(result, location)
            except AssertionError:
                print("failed input: " + data)
                raise

    def test_decoding_raise_exception_openlr_version1(self):
        # version 1 from the whitepaper
        self.assertRaisesRegex(
            NotImplementedError,
            "detected version 1",
            binary_decode,
            "CQcm6yX4vTPGFwM7AskzCw==",
        )

    def test_decoding_raise_exception_openlr_version2(self):
        # version 2 from the whitepaper
        self.assertRaisesRegex(
            NotImplementedError,
            "detected version 2",
            binary_decode,
            "CgRbWyNG9BpsCQCb/jsbtAT/6/+jK1kC",
        )

    def test_decoding_raise_exception_unknown_location_type(self):
        self.assertRaisesRegex(
            ValueError, "cannot be identified", binary_decode, "ewGkNSK5Wg=="
        )

    def test_encoding_binary_examples(self):
        for name, data, location in LOCATIONS:
            result = binary_encode(location, is_base64=False)
            try:
                self.assert_locations(binary_decode(result, is_base64=False), location)
            except AssertionError:
                print("failed input: " + name)
                raise
