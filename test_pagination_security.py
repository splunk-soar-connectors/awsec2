# Copyright (c) 2026 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from awsec2_security import record_pagination_token


def test_repeated_pagination_token_is_rejected() -> None:
    seen_tokens = set()
    record_pagination_token("token-1", seen_tokens)

    try:
        record_pagination_token("token-1", seen_tokens)
    except ValueError as exc:
        assert "did not advance" in str(exc)
    else:
        raise AssertionError("Repeated pagination token was accepted")
