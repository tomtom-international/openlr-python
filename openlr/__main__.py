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
import argparse

from openlr import binary_decode, xml_encode_to_string, __version__


parser = argparse.ArgumentParser(
    description="Decode an OpenLR binary location reference"
)
parser.add_argument("lr", help="the base 64 binary location reference string")
parser.add_argument("--version", "-v", action="version", version=__version__)
args = parser.parse_args()

location = binary_decode(args.lr)
print(xml_encode_to_string(location, is_pretty=True))
