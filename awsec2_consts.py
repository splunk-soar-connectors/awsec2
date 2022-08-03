# File: awsec2_consts.py
#
# Copyright (c) 2019-2022 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.
#
#
# Define your constants here
EC2_JSON_ACCESS_KEY = "access_key"
EC2_JSON_SECRET_KEY = "secret_key"  # pragma: allowlist secret
EC2_JSON_REGION = "region"
EC2_MAX_RESULTS_LIMIT = 1000

EC2_REGION_DICT = {
    "US East (Ohio)": "us-east-2",
    "US East (N. Virginia)": "us-east-1",
    "US West (N. California)": "us-west-1",
    "US West (Oregon)": "us-west-2",
    "Asia Pacific (Mumbai)": "ap-south-1",
    "Asia Pacific (Osaka-Local)": "ap-northeast-3",
    "Asia Pacific (Seoul)": "ap-northeast-2",
    "Asia Pacific (Singapore)": "ap-southeast-1",
    "Asia Pacific (Sydney)": "ap-southeast-2",
    "Asia Pacific (Hong Kong)": "ap-east-1",
    "Asia Pacific (Tokyo)": "ap-northeast-1",
    "Canada (Central)": "ca-central-1",
    "China (Beijing)": "cn-north-1",
    "China (Ningxia)": "cn-northwest-1",
    "EU (Frankfurt)": "eu-central-1",
    "EU (Ireland)": "eu-west-1",
    "EU (London)": "eu-west-2",
    "EU (Paris)": "	eu-west-3",
    "EU (Stockholm)": "eu-north-1",
    "South America (Sao Paulo)": "sa-east-1",
    "AWS GovCloud (US-East)": "us-gov-east-1",
    "AWS GovCloud (US)": "us-gov-west-1"
}

EC2_PAGINATION_SUPPORTED_ACTIONS = {
    'describe_instance': 'InstanceIds',
    'describe_subnets': 'SubnetIds',
    'describe_network_interfaces': 'NetworkInterfaceIds',
    'describe_snapshots': 'SnapshotIds',
    'describe_vpcs': 'VpcIds',
}

EC2_INVALID_LIMIT_MSG = 'Please provide a non-zero positive integer in {param_name}'
EC2_BAD_ASSET_CONFIG_MSG = 'Please provide access keys or select assume role check box in asset configuration'
EC2_ROLE_CREDENTIALS_FAILURE_MSG = 'Failed to retrieve EC2 role credentials from instance'

EC2_ERR_MSG_UNAVAILABLE = "Error message unavailable. Please check the asset configuration and|or action parameters"
EC2_VALID_INT_MSG = "Please provide a valid integer value in the '{param}' parameter"
EC2_NON_NEG_NON_ZERO_INT_MSG = "Please provide a valid non-zero positive integer value in '{param}' parameter"
EC2_NON_NEG_INT_MSG = "Please provide a valid non-negative integer value in the '{param}' parameter"

EC2_RESOURCE_TYPES = ['instance', 'network_interface']
EC2_DEFAULT_TIMEOUT = 30

EC2_LIMIT_KEY = "'limit' action parameter"
EC2_MAX_RESULTS_KEY = "'max_results' action parameter"
