# File: awsec2_connector.py
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
import ast
import json
import re
import sys
from datetime import datetime

import botocore.response as br
import phantom.app as phantom
import requests
import six
from boto3 import Session, client, resource
from botocore.config import Config
from phantom.action_result import ActionResult
from phantom.base_connector import BaseConnector

from awsec2_consts import *


class RetVal(tuple):
    def __new__(cls, val1, val2=None):
        return tuple.__new__(RetVal, (val1, val2))


class AwsEc2Connector(BaseConnector):

    def __init__(self):

        # Call the BaseConnectors init first
        super(AwsEc2Connector, self).__init__()

        self._state = None
        self._region = None
        self._access_key = None
        self._secret_key = None
        self._session_token = None
        self._proxy = None

    def _get_error_message_from_exception(self, e):
        """
        Get appropriate error message from the exception.
        :param e: Exception object
        :return: error message
        """

        error_code = None
        error_msg = EC2_ERR_MSG_UNAVAILABLE

        try:
            if hasattr(e, "args"):
                if len(e.args) > 1:
                    error_code = e.args[0]
                    error_msg = e.args[1]
                elif len(e.args) == 1:
                    error_msg = e.args[0]
        except Exception as e:
            self.debug_print("Error occurred while fetching exception information. Details: {}".format(str(e)))

        if not error_code:
            error_text = "Error Message: {}".format(error_msg)
        else:
            error_text = "Error Code: {}. Error Message: {}".format(error_code, error_msg)

        return error_text

    def _validate_integer(self, action_result, parameter, key, allow_zero=False):
        """
        Validate an integer.

        :param action_result: Action result or BaseConnector object
        :param parameter: input parameter
        :param key: input parameter message key
        :allow_zero: whether zero should be considered as valid value or not
        :return: status phantom.APP_ERROR/phantom.APP_SUCCESS, integer value of the parameter or None in case of failure
        """
        if parameter is not None:
            try:
                if not float(parameter).is_integer():
                    return action_result.set_status(phantom.APP_ERROR, EC2_VALID_INT_MSG.format(param=key)), None

                parameter = int(parameter)
            except Exception:
                return action_result.set_status(phantom.APP_ERROR, EC2_VALID_INT_MSG.format(param=key)), None

            if parameter < 0:
                return action_result.set_status(phantom.APP_ERROR, EC2_NON_NEG_INT_MSG.format(param=key)), None
            if not allow_zero and parameter == 0:
                return action_result.set_status(phantom.APP_ERROR, EC2_NON_NEG_NON_ZERO_INT_MSG.format(param=key)), None

        return phantom.APP_SUCCESS, parameter

    def _sanitize_data(self, cur_obj):

        try:
            json.dumps(cur_obj)
            return cur_obj
        except Exception:
            pass

        if isinstance(cur_obj, dict):
            new_dict = {}
            for k, v in six.iteritems(cur_obj):
                if isinstance(v, br.StreamingBody):
                    content = v.read()
                    new_dict[k] = json.loads(content)
                else:
                    new_dict[k] = self._sanitize_data(v)
            return new_dict

        # if returning list(ec2.Tag) - example, for add_tag action
        if str(cur_obj).startswith('[ec2.Tag'):
            try:
                return re.findall('.*resource_id=u?\'(.*?)\',.*', str(cur_obj))[0]
            except Exception:
                pass

        if isinstance(cur_obj, list):
            new_list = []
            for v in cur_obj:
                new_list.append(self._sanitize_data(v))
            return new_list

        if isinstance(cur_obj, datetime):
            return cur_obj.strftime("%Y-%m-%d %H:%M:%S")

        return cur_obj

    def _make_boto_call(self, action_result, method, **kwargs):

        self.debug_print(f"Making boto call to '{method}' with arguments: {kwargs}")
        try:
            boto_func = getattr(self._service, method)
        except AttributeError:
            return RetVal(action_result.set_status(phantom.APP_ERROR, "Invalid method: {0}".format(method)), None)

        try:
            resp_json = boto_func(**kwargs)
        except Exception as e:
            error_msg = self._get_error_message_from_exception(e)
            return RetVal(action_result.set_status(
                phantom.APP_ERROR, 'The boto3 call to ec2 failed. {}'.format(error_msg)), None)

        return action_result.set_status(phantom.APP_SUCCESS), self._sanitize_data(resp_json)

    def _handle_get_ec2_role(self):

        session = Session(region_name=self._region)
        credentials = session.get_credentials()
        return credentials

    def _create_client(self, service, action_result, param=None, region=None):

        boto_config = None
        if self._proxy:
            boto_config = Config(proxies=self._proxy)

        # Try getting and using temporary assume role credentials from parameters
        temp_credentials = dict()
        if param and 'credentials' in param:
            try:
                temp_credentials = ast.literal_eval(param['credentials'])
                self._access_key = temp_credentials.get('AccessKeyId', '')
                self._secret_key = temp_credentials.get('SecretAccessKey', '')
                self._session_token = temp_credentials.get('SessionToken', '')

                self.save_progress("Using temporary assume role credentials for action")
            except Exception as e:
                error_msg = self._get_error_message_from_exception(e)
                return action_result.set_status(phantom.APP_ERROR,
                                                "Failed to get temporary credentials: {0}".format(error_msg))

        if not region:
            region = self._region

        try:
            if self._access_key and self._secret_key:
                self.debug_print("Creating boto3 client with API keys")
                self._service = client(
                    service,
                    region_name=region,
                    aws_access_key_id=self._access_key,
                    aws_secret_access_key=self._secret_key,
                    aws_session_token=self._session_token,
                    config=boto_config)
            else:
                self.debug_print("Creating boto3 client without API keys")
                self._service = client(
                    service,
                    region_name=region,
                    config=boto_config)
        except Exception as e:
            error_msg = self._get_error_message_from_exception(e)
            return action_result.set_status(phantom.APP_ERROR, "Could not create boto3 client: {0}".format(error_msg))

        return phantom.APP_SUCCESS

    def _validate_instance_id(self, instance_id, action_result, param):
        if not self._create_client('ec2', action_result, param):
            return action_result.get_status()

        args = {
            'InstanceIds': [instance_id]
        }

        # make rest call
        ret_val, response = self._make_boto_call(action_result, 'describe_instances', **args)

        if phantom.is_fail(ret_val) or not response.get('Reservations'):
            return action_result.set_status(phantom.APP_ERROR, 'Please provide a valid instance ID')

        return action_result.set_status(phantom.APP_SUCCESS)

    def _create_resource(self, action_result, resource_type, identifier=None, param=None):

        if resource_type not in EC2_RESOURCE_TYPES:
            return action_result.set_status(phantom.APP_ERROR,
                                            "Incorrect resource type: {0}".format(resource_type))

        boto_config = None

        # Validate the instance ID
        if resource_type == 'instance' and identifier:
            ret_val = self._validate_instance_id(identifier, action_result, param)

            if phantom.is_fail(ret_val):
                return action_result.get_status()

        if self._proxy:
            boto_config = Config(proxies=self._proxy)

        # Try getting and using temporary assume role credentials from parameters
        temp_credentials = dict()
        if param and 'credentials' in param:
            try:
                temp_credentials = ast.literal_eval(param['credentials'])
                self._access_key = temp_credentials.get('AccessKeyId', '')
                self._secret_key = temp_credentials.get('SecretAccessKey', '')
                self._session_token = temp_credentials.get('SessionToken', '')

                self.save_progress("Using temporary assume role credentials for action")
            except Exception as e:
                error_msg = self._get_error_message_from_exception(e)
                return action_result.set_status(phantom.APP_ERROR,
                                                "Failed to get temporary credentials:{0}".format(error_msg))

        try:
            if self._access_key and self._secret_key:
                self.debug_print("Creating boto3 ec2 resource with API keys")
                ec2 = resource(
                    'ec2',
                    region_name=self._region,
                    aws_access_key_id=self._access_key,
                    aws_secret_access_key=self._secret_key,
                    aws_session_token=self._session_token,
                    config=boto_config)
            else:
                self.debug_print("Creating boto3 ec2 resource without API keys")
                ec2 = resource(
                    'ec2',
                    region_name=self._region,
                    config=boto_config)

            if resource_type == 'instance' and identifier:
                self._service = ec2.Instance(identifier)
            elif resource_type == 'network_interface' and identifier:
                self._service = ec2.NetworkInterface(identifier)
            else:
                return action_result.set_status(phantom.APP_ERROR, "Could not create boto3 instance: incorrect resource parameters")
        except Exception as e:
            error_msg = self._get_error_message_from_exception(e)
            return action_result.set_status(phantom.APP_ERROR, "Could not create boto3 instance: {0}".format(error_msg))

        return phantom.APP_SUCCESS

    def _handle_test_connectivity(self, param):

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        self.save_progress("Querying AWS to check credentials")

        if not self._create_client('ec2', action_result, param):
            return action_result.get_status()

        # make rest call
        ret_val, resp_json = self._make_boto_call(action_result, 'describe_security_groups', MaxResults=5)

        if phantom.is_fail(ret_val):
            self.save_progress("Test Connectivity Failed")
            return action_result.get_status()

        # Return success
        self.save_progress("Test Connectivity Passed")
        return action_result.set_status(phantom.APP_SUCCESS)

    def _paginator(self, method_name, limit, action_result, key="Reservations", **kwargs):
        """
        Handles the pagination
        """

        list_items = list()
        next_token = None

        if self.get_action_identifier() in EC2_PAGINATION_SUPPORTED_ACTIONS and \
                EC2_PAGINATION_SUPPORTED_ACTIONS[self.get_action_identifier()] not in kwargs:
            kwargs['MaxResults'] = EC2_MAX_RESULTS_LIMIT

        while True:
            if next_token:
                ret_val, response = self._make_boto_call(action_result, method_name, NextToken=next_token, **kwargs)
            else:
                ret_val, response = self._make_boto_call(action_result, method_name, **kwargs)
                if phantom.is_fail(ret_val) and 'InvalidParameterCombination' in action_result.get_message():
                    kwargs.pop('MaxResults', None)
                    self.debug_print('Retrying the call without pagination')
                    ret_val, response = self._make_boto_call(action_result, method_name, **kwargs)

            if phantom.is_fail(ret_val):
                return []

            list_items.extend(response.get(key, []))

            if limit and len(list_items) >= limit:
                return list_items[:limit]

            next_token = response.get('NextToken')
            if not next_token:
                break

        return list_items

    def _parse_comma_separated_ids(self, to_comma_sep_list):
        to_list = [x.strip() for x in to_comma_sep_list.split(",")]
        return list(filter(None, to_list))

    def _parse_filter_string(self, filters, action_result):
        try:
            evaluated_filters = list(ast.literal_eval(filters))
            # If only one filter
            if isinstance(evaluated_filters[0], str):
                return phantom.APP_SUCCESS, [ast.literal_eval(filters)]
            else:
                return phantom.APP_SUCCESS, evaluated_filters
        except Exception as e:
            error_msg = self._get_error_message_from_exception(e)
            return action_result.set_status(
                phantom.APP_ERROR, 'Error occurred while parsing filter: {0}'.format(error_msg)), None

    def _parse_tag_specifications(self, tag_specs, action_result):
        try:
            return phantom.APP_SUCCESS, json.loads(tag_specs)
        except Exception as e:
            error_msg = "Error occurred while parsing tag specifications. {}".format(self._get_error_message_from_exception(e))
            return action_result.set_status(phantom.APP_ERROR, error_msg), None

    def _handle_describe_images(self, param):
        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client('ec2', action_result, param):
            return action_result.get_status()

        filters = param.get('filters')
        image_ids = param.get('image_ids')
        dry_run = param.get('dry_run')
        executable_users = param.get('executable_users')
        owners = param.get('owners')

        args = dict()
        if filters:
            ret_val, args['Filters'] = self._parse_filter_string(filters, action_result)
            if phantom.is_fail(ret_val):
                return action_result.get_status()

        if image_ids:
            args['ImageIds'] = self._parse_comma_separated_ids(image_ids)
        if executable_users:
            args['ExecutableUsers'] = self._parse_comma_separated_ids(executable_users)
        if owners:
            args['Owners'] = self._parse_comma_separated_ids(owners)
        if dry_run:
            args['DryRun'] = dry_run

        ret_val, images_response = self._make_boto_call(action_result, 'describe_images', **args)
        if phantom.is_fail(ret_val):
            return action_result.get_status()

        images = images_response.get('Images', [])
        for image in images:
            action_result.add_data(image)

        # Add a dictionary that is made up of the most important values from data into the summary
        summary = action_result.update_summary({})
        summary['num_images'] = action_result.get_data_size()

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_describe_instance(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client('ec2', action_result, param):
            return action_result.get_status()

        filters = param.get('filters')
        instance_ids = param.get('instance_ids')
        dry_run = param.get('dry_run')

        ret_val, limit = self._validate_integer(action_result, param.get('limit'), EC2_LIMIT_KEY)
        if phantom.is_fail(ret_val):
            return action_result.get_status()

        args = dict()
        if filters:
            ret_val, args['Filters'] = self._parse_filter_string(filters, action_result)
            if phantom.is_fail(ret_val):
                return action_result.get_status()

        if instance_ids:
            args['InstanceIds'] = self._parse_comma_separated_ids(instance_ids)
        if dry_run:
            args['DryRun'] = dry_run

        list_reservations = self._paginator('describe_instances', limit, action_result, key="Reservations", **args)
        if action_result.get_message():
            return action_result.get_status()

        response = {'Reservations': list_reservations}
        # Add the response into the data section
        action_result.add_data(response)

        # The instances are obtained from within the reservations list, hence, fetching the correct count of instances
        # Change the structure of the tags based on the ticket PAPP-7613
        reservations_list = response.get('Reservations')
        total_instances = 0
        if reservations_list:
            for reservation in reservations_list:
                instances_list = reservation.get('Instances', [])
                total_instances += len(instances_list)
                for instance in instances_list:
                    tags_list = []
                    if 'Tags' in instance:
                        tags_list = instance.pop('Tags')

                    instance['Tags'] = dict()
                    for tag in tags_list:
                        if tag.get('Key'):
                            instance['Tags'].update({tag.get('Key'): tag.get('Value')})

        # Add a dictionary that is made up of the most important values from data into the summary
        summary = action_result.update_summary({})
        summary['num_instances'] = total_instances

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_describe_subnets(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client('ec2', action_result, param):
            return action_result.get_status()

        filters = param.get('filters')
        subnet_ids = param.get('subnet_ids')
        dry_run = param.get('dry_run')

        ret_val, limit = self._validate_integer(action_result, param.get('limit'), EC2_LIMIT_KEY)
        if phantom.is_fail(ret_val):
            return action_result.get_status()

        args = dict()
        if filters:
            ret_val, args['Filters'] = self._parse_filter_string(filters, action_result)
            if phantom.is_fail(ret_val):
                return action_result.get_status()

        if subnet_ids:
            args['SubnetIds'] = self._parse_comma_separated_ids(subnet_ids)
        if dry_run:
            args['DryRun'] = dry_run

        list_subnets = self._paginator('describe_subnets', limit, action_result, key="Subnets", **args)
        if action_result.get_message():
            return action_result.get_status()

        # Add the response into the data section
        for subnet in list_subnets:
            action_result.add_data(subnet)

        # Add a dictionary that is made up of the most important values from data into the summary
        summary = action_result.update_summary({})
        summary['num_subnets'] = action_result.get_data_size()

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_describe_vpcs(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client('ec2', action_result, param):
            return action_result.get_status()

        filters = param.get('filters')
        vpc_ids = param.get('vpc_ids')
        dry_run = param.get('dry_run')

        ret_val, limit = self._validate_integer(action_result, param.get('limit'), EC2_LIMIT_KEY)
        if phantom.is_fail(ret_val):
            return action_result.get_status()

        args = dict()
        if filters:
            ret_val, args['Filters'] = self._parse_filter_string(filters, action_result)
            if phantom.is_fail(ret_val):
                return action_result.get_status()

        if vpc_ids:
            args['VpcIds'] = self._parse_comma_separated_ids(vpc_ids)
        if dry_run:
            args['DryRun'] = dry_run

        list_vpcs = self._paginator('describe_vpcs', limit, action_result, key="Vpcs", **args)
        if action_result.get_message():
            return action_result.get_status()

        # Add the response into the data section
        for vpc in list_vpcs:
            action_result.add_data(vpc)

        # Add a dictionary that is made up of the most important values from data into the summary
        summary = action_result.update_summary({})
        summary['num_vpcs'] = action_result.get_data_size()

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_describe_network_interfaces(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client('ec2', action_result, param):
            return action_result.get_status()

        filters = param.get('filters')
        network_interface_ids = param.get('network_interface_ids')
        dry_run = param.get('dry_run')

        ret_val, limit = self._validate_integer(action_result, param.get('limit'), EC2_LIMIT_KEY)
        if phantom.is_fail(ret_val):
            return action_result.get_status()

        args = dict()
        if filters:
            ret_val, args['Filters'] = self._parse_filter_string(filters, action_result)
            if phantom.is_fail(ret_val):
                return action_result.get_status()

        if network_interface_ids:
            args['NetworkInterfaceIds'] = self._parse_comma_separated_ids(network_interface_ids)
        if dry_run:
            args['DryRun'] = dry_run

        list_network_interfaces = self._paginator('describe_network_interfaces', limit, action_result, key="NetworkInterfaces", **args)
        if action_result.get_message():
            return action_result.get_status()

        # Add the response into the data section
        for network_interface in list_network_interfaces:
            action_result.add_data(network_interface)

        # Add a dictionary that is made up of the most important values from data into the summary
        summary = action_result.update_summary({})
        summary['num_network_interfaces'] = action_result.get_data_size()

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_start_instance(self, param):
        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client('ec2', action_result, param):
            return action_result.get_status()

        instance_ids = param['instance_ids']
        dry_run = param.get('dry_run', False)

        instance_ids_list = self._parse_comma_separated_ids(instance_ids)

        args = {
            "InstanceIds": instance_ids_list
        }
        if dry_run:
            args['DryRun'] = dry_run

        # make rest call
        ret_val, response = self._make_boto_call(action_result, 'start_instances', **args)

        if phantom.is_fail(ret_val):
            return action_result.get_status()

        if not response:
            return action_result.get_status()

        started_instances = response.get('StartingInstances', [])

        for instance in started_instances:
            action_result.add_data(instance)

        return action_result.set_status(phantom.APP_SUCCESS, 'Instances started successfully')

    def _handle_stop_instance(self, param):
        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client('ec2', action_result, param):
            return action_result.get_status()

        instance_ids = param['instance_ids']
        force = param.get('force', False)
        dry_run = param.get('dry_run', False)

        instance_ids_list = self._parse_comma_separated_ids(instance_ids)

        args = {
            "InstanceIds": instance_ids_list
        }
        if force:
            args['Force'] = force
        if dry_run:
            args['DryRun'] = dry_run

        # make rest call
        ret_val, response = self._make_boto_call(action_result, 'stop_instances', **args)

        if phantom.is_fail(ret_val):
            return action_result.get_status()

        if not response:
            return action_result.get_status()

        stopped_instances = response.get('StoppingInstances', [])

        for instance in stopped_instances:
            action_result.add_data(instance)

        return action_result.set_status(phantom.APP_SUCCESS, 'Instances stopped successfully')

    def _handle_detach_instance(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client('autoscaling', action_result, param):
            return action_result.get_status()

        instance_ids = param.get('instance_ids')
        autoscaling_group_name = param['autoscaling_group_name']
        should_decrement_desired_capacity = param.get('should_decrement_desired_capacity', False)

        args = {
            'AutoScalingGroupName': autoscaling_group_name,
            'ShouldDecrementDesiredCapacity': should_decrement_desired_capacity
        }
        if instance_ids:
            args['InstanceIds'] = self._parse_comma_separated_ids(instance_ids)

        # make rest call
        ret_val, response = self._make_boto_call(action_result, 'detach_instances', **args)

        if phantom.is_fail(ret_val):
            return action_result.get_status()

        # Add the response into the data section
        action_result.add_data(response)

        # Add a dictionary that is made up of the most important values from data into the summary
        summary = action_result.update_summary({})
        summary['status'] = "Successfully detached instance"

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_attach_instance(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client('autoscaling', action_result, param):
            return action_result.get_status()

        instance_ids = param.get('instance_ids')
        autoscaling_group_name = param['autoscaling_group_name']

        args = {
            'AutoScalingGroupName': autoscaling_group_name
        }
        if instance_ids:
            args['InstanceIds'] = self._parse_comma_separated_ids(instance_ids)

        # make rest call
        ret_val, response = self._make_boto_call(action_result, 'attach_instances', **args)

        if phantom.is_fail(ret_val):
            return action_result.get_status()

        # Add the response into the data section
        action_result.add_data(response)

        # Add a dictionary that is made up of the most important values from data into the summary
        summary = action_result.update_summary({})
        summary['status'] = "Successfully attached instance"

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_deregister_instance(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client('elb', action_result, param):
            return action_result.get_status()

        load_balancer_name = param['load_balancer_name']
        instance_ids = param['instance_ids']
        instance_id_dict = [{'InstanceId': item.strip()} for item in instance_ids.split(',') if item]

        args = {
            'LoadBalancerName': load_balancer_name,
            'Instances': instance_id_dict
        }

        # make rest call
        ret_val, response = self._make_boto_call(action_result, 'deregister_instances_from_load_balancer', **args)

        if phantom.is_fail(ret_val):
            return action_result.get_status()

        # Add the response into the data section
        action_result.add_data(response)

        # Add a dictionary that is made up of the most important values from data into the summary
        summary = action_result.update_summary({})
        summary['status'] = "Successfully deregistered instance"

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_register_instance(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client('elb', action_result, param):
            return action_result.get_status()

        load_balancer_name = param['load_balancer_name']
        instance_ids = param['instance_ids']
        instance_id_dict = [{'InstanceId': item.strip()} for item in instance_ids.split(',') if item]

        args = {
            'LoadBalancerName': load_balancer_name,
            'Instances': instance_id_dict
        }

        # make boto call
        ret_val, response = self._make_boto_call(action_result, 'register_instances_with_load_balancer', **args)

        if phantom.is_fail(ret_val):
            return action_result.get_status()

        # Add the response into the data section
        action_result.add_data(response)

        summary = action_result.update_summary({})
        summary['status'] = "Successfully registered instance"

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_create_security_group(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client('ec2', action_result, param):
            return action_result.get_status()

        tag_specifications = param.get('tag_specifications')
        vpc_id = param.get('vpc_id')
        dry_run = param.get('dry_run')

        args = {
            "GroupName": param['group_name'],
            "Description": param['group_description']
        }
        if vpc_id:
            args['VpcId'] = vpc_id
        if dry_run:
            args['DryRun'] = dry_run
        if tag_specifications:
            ret_val, tag_specifications = self._parse_tag_specifications(tag_specifications, action_result)
            if phantom.is_fail(ret_val):
                return action_result.get_status()

            args['TagSpecifications'] = tag_specifications

        # make rest call
        ret_val, response = self._make_boto_call(action_result, 'create_security_group', **args)

        if phantom.is_fail(ret_val):
            return action_result.get_status()

        # Add the response into the data section
        action_result.add_data(response)

        # Add a dictionary that is made up of the most important values from data into the summary
        summary = action_result.update_summary({})
        summary['group_id'] = response.get('GroupId', 'Unavailable')

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_delete_security_group(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client('ec2', action_result, param):
            return action_result.get_status()

        dry_run = param.get('dry_run')
        group_name = param.get('group_name')
        group_id = param.get('group_id')

        args = dict()
        if group_id:
            args['GroupId'] = group_id
        elif group_name:
            args['GroupName'] = group_name
        else:
            return action_result.set_status(phantom.APP_ERROR, "Please provide one of the 'group id' or 'group name' parameter")

        if dry_run:
            args['DryRun'] = dry_run

        # make rest call
        ret_val, response = self._make_boto_call(action_result, 'delete_security_group', **args)

        if phantom.is_fail(ret_val):
            return action_result.get_status()

        # Add the response into the data section
        action_result.add_data(response)

        return action_result.set_status(phantom.APP_SUCCESS, "Successfully deleted the security group")

    def _handle_describe_snapshots(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client('ec2', action_result, param):
            return action_result.get_status()

        filters = param.get('filters')
        snapshot_ids = param.get('snapshot_ids')
        dry_run = param.get('dry_run')
        restorable_by = param.get('restorable_by')
        owners = param.get('owners')

        ret_val, limit = self._validate_integer(action_result, param.get('limit'), EC2_LIMIT_KEY)
        if phantom.is_fail(ret_val):
            return action_result.get_status()

        args = dict()
        if filters:
            ret_val, args['Filters'] = self._parse_filter_string(filters, action_result)
            if phantom.is_fail(ret_val):
                return action_result.get_status()

        if snapshot_ids:
            args['SnapshotIds'] = self._parse_comma_separated_ids(snapshot_ids)
        if restorable_by:
            args['RestorableByUserIds'] = self._parse_comma_separated_ids(restorable_by)
        if owners:
            args['OwnerIds'] = self._parse_comma_separated_ids(owners)
        if dry_run:
            args['DryRun'] = dry_run

        list_snapshots = self._paginator('describe_snapshots', limit, action_result, key="Snapshots", **args)
        if action_result.get_message():
            return action_result.get_status()

        # Add the response into the data section
        for snapshot in list_snapshots:
            action_result.add_data(snapshot)

        # Add a dictionary that is made up of the most important values from data into the summary
        summary = action_result.update_summary({})
        summary['num_snapshots'] = action_result.get_data_size()

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_snapshot_instance(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client('ec2', action_result, param):
            return action_result.get_status()

        volume_id = param['volume_id']
        description = param.get('description')
        tag_specifications = param.get('tag_specifications')
        dry_run = param.get('dry_run')

        args = {
            'VolumeId': volume_id
        }
        if description:
            args['Description'] = description
        if dry_run:
            args['DryRun'] = dry_run
        if tag_specifications:
            pass

        # make rest call
        ret_val, response = self._make_boto_call(action_result, 'create_snapshot', **args)

        if phantom.is_fail(ret_val):
            return action_result.get_status()

        # Add the response into the data section
        action_result.add_data(response)

        # Add a dictionary that is made up of the most important values from data into the summary
        summary = action_result.update_summary({})
        summary['snapshot_id'] = response.get('SnapshotId')

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_copy_snapshot(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        try:
            source_region = EC2_REGION_DICT[param['source_region']]
        except Exception:
            return self.set_status(phantom.APP_ERROR, "Please provide valid value for 'source region' parameter")

        args = {
            'SourceRegion': source_region,
            'SourceSnapshotId': param['source_snapshot_id'],
            'Description': param.get('description', f"[Copied {param['source_snapshot_id']} from {source_region}]")
        }

        if param.get('encrypted', False):
            args['Encrypted'] = param.get('encrypted')

        if param.get('destination_region'):
            try:
                args['DestinationRegion'] = EC2_REGION_DICT[param.get('destination_region')]
            except Exception:
                return self.set_status(phantom.APP_ERROR, "Please provide valid value for 'destination region' parameter")

            # The client should be of the destination region
            if not self._create_client('ec2', action_result, param, region=args['DestinationRegion']):
                return action_result.get_status()
        else:
            if not self._create_client('ec2', action_result, param):
                return action_result.get_status()

        # The parameter is not added in the action as per the discussion in PAPP-26699
        # if param.get('destination_outpost_arn'):
        #     args['DestinationOutpostArn'] = param.get('destination_outpost_arn')

        if param.get('kms_key_id'):
            args['KmsKeyId'] = param.get('kms_key_id')

        if param.get('presigned_url'):
            args['PresignedUrl'] = param.get('presigned_url')

        if param.get('dry_run'):
            args['DryRun'] = param.get('dry_run')

        if param.get('tag_specifications'):
            ret_val, tag_specifications = self._parse_tag_specifications(param.get('tag_specifications'), action_result)
            if phantom.is_fail(ret_val):
                return action_result.get_status()

            args['TagSpecifications'] = tag_specifications

        # make rest call
        ret_val, response = self._make_boto_call(action_result, 'copy_snapshot', **args)

        if phantom.is_fail(ret_val):
            return action_result.get_status()

        # Add the response into the data section
        action_result.add_data(response)

        # Add a dictionary that is made up of the most important values from data into the summary
        summary = action_result.update_summary({})
        summary['snapshot_id'] = response.get('SnapshotId')

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_delete_snapshot(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client('ec2', action_result, param):
            return action_result.get_status()

        snapshot_id = param['snapshot_id']
        dry_run = param.get('dry_run')

        args = {
            'SnapshotId': snapshot_id
        }

        if dry_run:
            args['DryRun'] = dry_run

        # make boto call
        ret_val, response = self._make_boto_call(action_result, 'delete_snapshot', **args)

        if phantom.is_fail(ret_val):
            return action_result.get_status()

        action_result.add_data(response)

        summary = action_result.update_summary({})
        summary['status'] = "Successfully deleted snapshot"

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_add_tag(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        instance_id = param['instance_id']

        if not self._create_resource(action_result, 'instance', instance_id, param):
            return action_result.get_status()

        tag_key = param.get('tag_key')
        tag_value = param.get('tag_value', "")
        dry_run = param.get('dry_run')

        args = {
            "Tags": [
                {
                    "Key": tag_key,
                    "Value": tag_value
                }
            ]
        }
        if dry_run:
            args['DryRun'] = dry_run

        # make rest call
        ret_val, response = self._make_boto_call(action_result, 'create_tags', **args)

        if phantom.is_fail(ret_val):
            return action_result.get_status()

        # Add the response into the data section
        action_result.add_data({'resource_id': response})

        # Add a dictionary that is made up of the most important values from data into the summary
        summary = action_result.update_summary({})
        summary['status'] = "Successfully added tag"

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_get_tag(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        instance_id = param['instance_id']
        tag_key = param['tag_key']
        dry_run = param.get('dry_run', False)

        if not self._create_client('ec2', action_result, param):
            return action_result.get_status()

        args = {
            "Filters": [
                {
                    "Name": "resource-type",
                    "Values": [
                        "instance"
                    ]
                },
                {
                    "Name": "resource-id",
                    "Values": [
                        instance_id
                    ]
                },
                {
                    "Name": "key",
                    "Values": [
                        tag_key
                    ]
                }
            ]
        }
        if dry_run:
            args['DryRun'] = dry_run

        # make rest call
        ret_val, response = self._make_boto_call(action_result, 'describe_tags', **args)

        if phantom.is_fail(ret_val):
            return action_result.get_status()

        if not response:
            return action_result.get_status()

        if not response.get('Tags'):
            resp_message = 'No tags found with the tag key: {0} in the instance with ID: {1}'.format(tag_key, instance_id)
            return action_result.set_status(phantom.APP_ERROR, resp_message)

        # Add the response into the data section
        # The output response will consist of a unique dictionary for given tag
        # Hence, extracting the first element of the tags list
        action_result.add_data(response.get('Tags')[0])

        return action_result.set_status(phantom.APP_SUCCESS, 'Successfully fetched the tag value')

    def _handle_remove_tag(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        instance_id = param['instance_id']

        if not self._create_resource(action_result, 'instance', instance_id, param):
            return action_result.get_status()

        tag_key = param.get('tag_key')
        tag_value = param.get('tag_value')
        dry_run = param.get('dry_run')

        args = dict()
        tags_dict = dict()

        if not tag_key and tag_value:
            return action_result.set_status(phantom.APP_ERROR,
                'Providing tag value without a tag key performs nothing and hence, it is not allowed')

        if tag_key and tag_value is None:
            tags_dict = {
                "Key": tag_key
            }
        elif tag_key:
            tags_dict = {
                "Key": tag_key,
                "Value": tag_value
            }

        if tags_dict:
            args['Tags'] = [tags_dict]

        if dry_run:
            args['DryRun'] = dry_run

        # make rest call
        ret_val, response = self._make_boto_call(action_result, 'delete_tags', **args)

        if phantom.is_fail(ret_val):
            return action_result.get_status()

        # Add the response into the data section
        action_result.add_data(response)

        # Add a dictionary that is made up of the most important values from data into the summary
        summary = action_result.update_summary({})
        summary['status'] = "Successfully removed tag"

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_get_acls(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client('ec2', action_result, param):
            return action_result.get_status()

        filters = param.get('filters')
        dry_run = param.get('dry_run')
        network_acl_ids = param.get('network_acl_ids')

        args = dict()
        if filters:
            ret_val, args['Filters'] = self._parse_filter_string(filters, action_result)
            if phantom.is_fail(ret_val):
                return action_result.get_status()
        if dry_run:
            args['DryRun'] = dry_run
        if network_acl_ids:
            args['NetworkAclIds'] = self._parse_comma_separated_ids(network_acl_ids)

        # make rest call
        ret_val, response = self._make_boto_call(action_result, 'describe_network_acls', **args)

        if phantom.is_fail(ret_val):
            return action_result.get_status()

        # Add the response into the data section
        action_result.add_data(response)

        # Add a dictionary that is made up of the most important values from data into the summary
        summary = action_result.update_summary({})
        summary['num_acls'] = len(response.get('NetworkAcls', {}))

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_add_acl(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client('ec2', action_result, param):
            return action_result.get_status()

        vpc_id = param['vpc_id']
        dry_run = param.get('dry_run')
        args = {
            "VpcId": vpc_id
        }
        if dry_run:
            args['DryRun'] = dry_run

        # make rest call
        ret_val, response = self._make_boto_call(action_result, 'create_network_acl', **args)

        if phantom.is_fail(ret_val):
            return action_result.get_status()

        # Add the response into the data section
        action_result.add_data(response)

        # Add a dictionary that is made up of the most important values from data into the summary
        summary = action_result.update_summary({})
        summary['network_acl_id'] = response.get('NetworkAcl', {}).get('NetworkAclId', 'Unavailable')

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_remove_acl(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client('ec2', action_result, param):
            return action_result.get_status()

        network_acl_id = param['network_acl_id']
        dry_run = param.get('dry_run')

        args = {
            'NetworkAclId': network_acl_id
        }
        if dry_run:
            args['DryRun'] = dry_run

        # make rest call
        ret_val, response = self._make_boto_call(action_result, 'delete_network_acl', **args)

        if phantom.is_fail(ret_val):
            return action_result.get_status()

        # Add the response into the data section
        action_result.add_data(response)

        # Add a dictionary that is made up of the most important values from data into the summary
        summary = action_result.update_summary({})
        summary['status'] = "Successfully removed acl"

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_list_security_groups(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client('ec2', action_result, param):
            return action_result.get_status()

        filters = param.get('filters')
        dry_run = param.get('dry_run')
        group_ids = param.get('group_ids')
        group_names = param.get('group_names')
        next_token = param.get('next_token')

        ret_val, max_results = self._validate_integer(action_result, param.get('max_results'), EC2_LIMIT_KEY)
        if phantom.is_fail(ret_val):
            return action_result.get_status()

        args = dict()
        if filters:
            ret_val, args['Filters'] = self._parse_filter_string(filters, action_result)
            if phantom.is_fail(ret_val):
                return action_result.get_status()
        if group_ids:
            args['GroupIds'] = self._parse_comma_separated_ids(group_ids)
        if group_names:
            args['GroupNames'] = self._parse_comma_separated_ids(group_names)
        if dry_run:
            args['DryRun'] = dry_run
        if next_token:
            args['NextToken'] = next_token
        if max_results is not None:
            args['MaxResults'] = max_results

        # make rest call
        ret_val, response = self._make_boto_call(action_result, 'describe_security_groups', **args)

        if phantom.is_fail(ret_val):
            return action_result.get_status()

        # Add the response into the data section
        action_result.add_data(response)

        # Add a dictionary that is made up of the most important values from data into the summary
        summary = action_result.update_summary({})
        summary['num_security_groups'] = len(response.get('SecurityGroups', {}))

        return action_result.set_status(phantom.APP_SUCCESS)

    def _security_group_helper(self, instance_id, action_result, param):

        # Get original list of security groups associated with network interface id
        if not self._create_client('ec2', action_result, param):
            return action_result.get_status()

        args = {
            'InstanceIds': [instance_id]
        }

        # make rest call
        ret_val, response = self._make_boto_call(action_result, 'describe_instances', **args)

        if phantom.is_fail(ret_val):
            return (action_result.get_status(), None, None)

        group_list = None
        network_interface_id = None
        reservations = response.get('Reservations')
        if reservations and reservations[0].get('Instances'):
            original_groups = reservations[0].get('Instances')[0].get('SecurityGroups')
            if original_groups:
                group_list = [item.get('GroupId') for item in original_groups]

            network_interfaces = reservations[0].get('Instances')[0].get('NetworkInterfaces')
            if network_interfaces:
                network_interface_id = network_interfaces[0].get('NetworkInterfaceId')
        else:
            return (action_result.set_status(phantom.APP_ERROR, 'The provided instance does not exist'), None, None)

        if group_list is None or network_interface_id is None:
            return (action_result.set_status(phantom.APP_ERROR,
                'Error occurred while fetching the group list and network interface ID for given instance ID'), None, None)

        return (phantom.APP_SUCCESS, group_list, network_interface_id)

    def _handle_assign_instance_to_group(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        group_to_add = param['group_id']
        instance_id = param['instance_id']
        ret_val, group_list, network_interface_id = self._security_group_helper(instance_id, action_result, param)
        if phantom.is_fail(ret_val):
            return action_result.get_status()

        # Try to add the parameterized group from the list
        if group_to_add not in group_list:
            group_list.append(group_to_add)
        else:
            return action_result.set_status(phantom.APP_SUCCESS, "Instance already included in security group")

        # Now that you have the list of original groups, remove the one provided by the user and post the new list
        if not self._create_resource(action_result, 'network_interface', network_interface_id, param):
            return action_result.get_status()

        args = {
            'Groups': group_list
        }

        # make rest call
        ret_val, response = self._make_boto_call(action_result, 'modify_attribute', **args)

        if phantom.is_fail(ret_val):
            return action_result.get_status()

        # Add the response into the data section
        action_result.add_data(response)

        # Add a dictionary that is made up of the most important values from data into the summary
        summary = action_result.update_summary({})
        summary['status'] = "Successfully added instance to security group"

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_remove_instance_from_group(self, param):
        '''
            Changes the security groups for the network interface.
            The new set of groups you specify replaces the current set.
            You must specify at least one group, even if it's just the default security group in the VPC.
            You must specify the ID of the security group, not the name.

            Get original group list, create a list of groups without a parameterised group, then update the group list
        '''

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        group_to_remove = param['group_id']
        instance_id = param['instance_id']

        ret_val, group_list, network_interface_id = self._security_group_helper(instance_id, action_result, param)

        if phantom.is_fail(ret_val):
            return action_result.get_status()

        # Try to remove the parameterized group from the list
        try:
            group_list.remove(group_to_remove)
        except Exception:
            return action_result.set_status(phantom.APP_SUCCESS, "Instance already not included in security group")

        # Now that you have the list of original groups, remove the one provided by the user and post the new list
        if not self._create_resource(action_result, 'network_interface', network_interface_id, param):
            return action_result.get_status()

        args = {
            'Groups': group_list
        }

        # make rest call
        ret_val, response = self._make_boto_call(action_result, 'modify_attribute', **args)

        if phantom.is_fail(ret_val):
            return action_result.get_status()

        # Add the response into the data section
        action_result.add_data(response)

        # Add a dictionary that is made up of the most important values from data into the summary
        summary = action_result.update_summary({})
        summary['status'] = "Successfully removed instance from security group"

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_create_vpc(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client('ec2', action_result, param):
            return action_result.get_status()

        cidr_block = param['cidr_block']
        amazon_provided_ipv6_cidr_block = param.get('amazon_provided_ipv6_cidr_block')
        dry_run = param.get('dry_run')
        instance_tenancy = param.get('instance_tenancy')

        args = {
            "CidrBlock": cidr_block
        }
        if amazon_provided_ipv6_cidr_block:
            args['AmazonProvidedIpv6CidrBlock'] = amazon_provided_ipv6_cidr_block
        if dry_run:
            args['DryRun'] = dry_run
        if instance_tenancy:
            args['InstanceTenancy'] = instance_tenancy

        # make rest call
        ret_val, response = self._make_boto_call(action_result, 'create_vpc', **args)

        if phantom.is_fail(ret_val):
            return action_result.get_status()

        # Add the response into the data section
        action_result.add_data(response)

        # Add a dictionary that is made up of the most important values from data into the summary
        summary = action_result.update_summary({})
        summary['vpc_id'] = response.get('Vpc', {}).get('VpcId', 'Unavailable')
        summary['instance_tenancy'] = response.get('Vpc', {}).get('InstanceTenancy', 'Unavailable')

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_delete_vpc(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client('ec2', action_result, param):
            return action_result.get_status()

        vpc_id = param['vpc_id']
        dry_run = param.get('dry_run')

        args = {
            "VpcId": vpc_id
        }

        if dry_run:
            args['DryRun'] = dry_run

        # make boto call
        ret_val, response = self._make_boto_call(action_result, 'delete_vpc', **args)

        if phantom.is_fail(ret_val):
            return action_result.get_status()

        action_result.add_data(response)

        summary = action_result.update_summary({})
        summary['status'] = "Successfully deleted vpc"

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_list_network_interfaces(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client('ec2', action_result, param):
            return action_result.get_status()

        filters = param.get('filters')
        dry_run = param.get('dry_run')
        network_interface_ids = param.get('network_interface_ids')
        next_token = param.get('next_token')

        ret_val, max_results = self._validate_integer(action_result, param.get('max_results'), EC2_LIMIT_KEY)
        if phantom.is_fail(ret_val):
            return action_result.get_status()

        args = dict()
        if filters:
            ret_val, args['Filters'] = self._parse_filter_string(filters, action_result)
            if phantom.is_fail(ret_val):
                return action_result.get_status()
        if dry_run:
            args['DryRun'] = dry_run
        if network_interface_ids:
            args['NetworkInterfaceIds'] = self._parse_comma_separated_ids(network_interface_ids)
        if next_token:
            args['NextToken'] = next_token
        if max_results is not None:
            args['MaxResults'] = max_results

        # make rest call
        ret_val, response = self._make_boto_call(action_result, 'describe_network_interfaces', **args)
        if phantom.is_fail(ret_val):
            return action_result.get_status()

        # Add the response into the data section
        action_result.add_data(response)

        # Add a dictionary that is made up of the most important values from data into the summary
        summary = action_result.update_summary({})
        summary['num_network_interfaces'] = len(response.get('NetworkInterfaces', []))

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_list_autoscaling_groups(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client('autoscaling', action_result, param):
            return action_result.get_status()

        autoscaling_group_names = param.get('autoscaling_group_names')
        next_token = param.get('next_token')

        ret_val, max_results = self._validate_integer(action_result, param.get('max_results'), EC2_LIMIT_KEY)
        if phantom.is_fail(ret_val):
            return action_result.get_status()

        args = dict()
        if autoscaling_group_names:
            args['AutoScalingGroupNames'] = self._parse_comma_separated_ids(autoscaling_group_names)
        if next_token:
            args['NextToken'] = next_token
        # This is a special case where the key is 'MaxRecords' instead of 'MaxResults'
        if max_results is not None:
            args['MaxRecords'] = max_results

        # make rest call
        ret_val, response = self._make_boto_call(action_result, 'describe_auto_scaling_groups', **args)

        if phantom.is_fail(ret_val):
            return action_result.get_status()

        # Add the response into the data section
        action_result.add_data(response)

        # Add a dictionary that is made up of the most important values from data into the summary
        summary = action_result.update_summary({})
        summary['num_autoscaling_groups'] = len(response.get('AutoScalingGroups', []))

        return action_result.set_status(phantom.APP_SUCCESS)

    def handle_action(self, param):

        ret_val = phantom.APP_SUCCESS

        # Get the action that we are supposed to execute for this App Run
        action_id = self.get_action_identifier()

        self.debug_print("action_id", self.get_action_identifier())

        action_mappings = {
            'test_connectivity': self._handle_test_connectivity,
            'describe_instance': self._handle_describe_instance,
            'describe_images': self._handle_describe_images,
            'describe_subnets': self._handle_describe_subnets,
            'describe_network_interfaces': self._handle_describe_network_interfaces,
            'start_instance': self._handle_start_instance,
            'stop_instance': self._handle_stop_instance,
            'detach_instance': self._handle_detach_instance,
            'attach_instance': self._handle_attach_instance,
            'register_instance': self._handle_register_instance,
            'deregister_instance': self._handle_deregister_instance,
            'describe_snapshots': self._handle_describe_snapshots,
            'describe_vpcs': self._handle_describe_vpcs,
            'snapshot_instance': self._handle_snapshot_instance,
            'copy_snapshot': self._handle_copy_snapshot,
            'delete_snapshot': self._handle_delete_snapshot,
            'get_tag': self._handle_get_tag,
            'add_tag': self._handle_add_tag,
            'remove_tag': self._handle_remove_tag,
            'get_acls': self._handle_get_acls,
            'add_acl': self._handle_add_acl,
            'remove_acl': self._handle_remove_acl,
            'list_security_groups': self._handle_list_security_groups,
            'assign_instance_to_group': self._handle_assign_instance_to_group,
            'remove_instance_from_group': self._handle_remove_instance_from_group,
            'create_vpc': self._handle_create_vpc,
            'delete_vpc': self._handle_delete_vpc,
            'list_network_interfaces': self._handle_list_network_interfaces,
            'list_autoscaling_groups': self._handle_list_autoscaling_groups,
            'create_security_group': self._handle_create_security_group,
            'delete_security_group': self._handle_delete_security_group,
        }

        if action_id in action_mappings:
            action_function = action_mappings[action_id]
            ret_val = action_function(param)

        return ret_val

    def initialize(self):

        self._state = self.load_state()
        if not isinstance(self._state, dict):
            self.debug_print("Resetting the state file with the default format")
            self._state = {"app_version": self.get_app_json().get("app_version")}

        # get the asset config
        config = self.get_config()

        self._region = EC2_REGION_DICT.get(config[EC2_JSON_REGION])

        self._proxy = {}
        env_vars = config.get('_reserved_environment_variables', {})
        if 'HTTP_PROXY' in env_vars:
            self._proxy['http'] = env_vars['HTTP_PROXY']['value']
        if 'HTTPS_PROXY' in env_vars:
            self._proxy['https'] = env_vars['HTTPS_PROXY']['value']

        if config.get('use_role'):
            credentials = self._handle_get_ec2_role()
            if not credentials:
                return self.set_status(phantom.APP_ERROR, EC2_ROLE_CREDENTIALS_FAILURE_MSG)
            self._access_key = credentials.access_key
            self._secret_key = credentials.secret_key
            self._session_token = credentials.token

            return phantom.APP_SUCCESS

        self._access_key = config.get(EC2_JSON_ACCESS_KEY)
        self._secret_key = config.get(EC2_JSON_SECRET_KEY)

        if not (self._access_key and self._secret_key):
            return self.set_status(phantom.APP_ERROR, EC2_BAD_ASSET_CONFIG_MSG)

        return phantom.APP_SUCCESS

    def finalize(self):

        # Save the state, this data is saved across actions and app upgrades
        self.save_state(self._state)
        return phantom.APP_SUCCESS


if __name__ == '__main__':

    import argparse

    import pudb

    pudb.set_trace()

    argparser = argparse.ArgumentParser()

    argparser.add_argument('input_test_json', help='Input Test JSON file')
    argparser.add_argument('-u', '--username', help='username', required=False)
    argparser.add_argument('-p', '--password', help='password', required=False)
    argparser.add_argument('-v', '--verify', action='store_true', help='verify', required=False, default=False)

    args = argparser.parse_args()
    session_id = None

    username = args.username
    password = args.password
    verify = args.verify

    if (username is not None and password is None):

        # User specified a username but not a password, so ask
        import getpass
        password = getpass.getpass("Password: ")

    if (username and password):
        try:
            login_url = AwsEc2Connector._get_phantom_base_url() + '/login'

            print("Accessing the Login page")
            r = requests.get(login_url, verify=verify, timeout=EC2_DEFAULT_TIMEOUT)
            csrftoken = r.cookies['csrftoken']

            data = dict()
            data['username'] = username
            data['password'] = password
            data['csrfmiddlewaretoken'] = csrftoken

            headers = dict()
            headers['Cookie'] = 'csrftoken=' + csrftoken
            headers['Referer'] = login_url

            print("Logging into Platform to get the session id")
            r2 = requests.post(login_url, verify=verify, data=data, headers=headers, timeout=EC2_DEFAULT_TIMEOUT)
            session_id = r2.cookies['sessionid']
        except Exception as e:
            print("Unable to get session id from the platform. Error: " + str(e))
            sys.exit(1)

    with open(args.input_test_json) as f:
        in_json = f.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=4))

        connector = AwsEc2Connector()
        connector.print_progress_message = True

        if (session_id is not None):
            in_json['user_session_token'] = session_id
            connector._set_csrf_info(csrftoken, headers['Referer'])

        ret_val = connector._handle_action(json.dumps(in_json), None)
        print(json.dumps(json.loads(ret_val), indent=4))

    sys.exit(0)
