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
