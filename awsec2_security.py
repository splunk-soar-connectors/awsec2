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
"""Security-focused helpers for AWS EC2 connector actions."""


def collect_network_interface_groups(instance):
    """Return each network interface ID with its own security-group IDs."""
    interfaces = instance.get("NetworkInterfaces") or []
    if not interfaces:
        raise ValueError("The instance has no network interfaces")

    collected = []
    for interface in interfaces:
        interface_id = interface.get("NetworkInterfaceId")
        group_ids = [group.get("GroupId") for group in interface.get("Groups") or [] if group.get("GroupId")]
        if not interface_id or not group_ids:
            raise ValueError("A network interface is missing its ID or security groups")
        collected.append((interface_id, group_ids))

    return collected


def record_pagination_token(next_token, seen_tokens):
    """Record a pagination token, rejecting tokens that do not advance."""
    if not next_token:
        return
    if next_token in seen_tokens:
        raise ValueError("The upstream pagination token did not advance")
    seen_tokens.add(next_token)
