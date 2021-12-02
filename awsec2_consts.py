# File: awsec2_consts.py
#
# Copyright (c) 2019-2021 Splunk Inc.
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
EC2_JSON_SECRET_KEY = "secret_key"
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

EC2_INVALID_LIMIT_MSG = 'Please provide a non-zero positive integer in {param_name}'
EC2_BAD_ASSET_CONFIG_MSG = 'Please provide access keys or select assume role check box in asset configuration'
EC2_ROLE_CREDENTIALS_FAILURE_MSG = 'Failed to retrieve EC2 role credentials from instance'
EC2_RESOURCE_TYPES = ['instance', 'network_interface']
