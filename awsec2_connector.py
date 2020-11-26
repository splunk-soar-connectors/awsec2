# File: awsec2_connector.py
# Copyright (c) 2019-2020 Splunk Inc.
#
# SPLUNK CONFIDENTIAL - Use or disclosure of this material in whole or in part
# without a valid written license from Splunk Inc. is PROHIBITED.
# Phantom App imports
import phantom.app as phantom
from phantom.base_connector import BaseConnector
from phantom.action_result import ActionResult

# Usage of the consts file is recommended
from awsec2_consts import *
from boto3 import client, resource
from datetime import datetime
from botocore.config import Config
from bs4 import UnicodeDammit
import botocore.response as br
import requests
import json
import re
import ast
import sys

import six


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
        self._proxy = None
        self._python_version = None

    def _handle_py_ver_compat_for_input_str(self, input_str):
        """
        This method returns the encoded|original string based on the Python version.
        :param input_str: Input string to be processed
        :return: input_str (Processed input string based on following logic 'input_str - Python 3; encoded input_str - Python 2')
        """
        try:
            if input_str and self._python_version < 3:
                input_str = UnicodeDammit(input_str).unicode_markup.encode('utf-8')
        except:
            self.debug_print("Error occurred while handling python 2to3 compatibility for the input string")

        return input_str

    def _get_error_message_from_exception(self, e):
        """ This function is used to get appropriate error message from the exception.
        :param e: Exception object
        :return: error message
        """
        error_msg = "Unknown error occurred. Please check the asset configuration and|or action parameters."
        error_code = "Error code unavailable"
        try:
            if e.args:
                if len(e.args) > 1:
                    error_code = e.args[0]
                    error_msg = e.args[1]
                elif len(e.args) == 1:
                    error_code = "Error code unavailable"
                    error_msg = e.args[0]
            else:
                error_code = "Error code unavailable"
                error_msg = "Unknown error occurred. Please check the asset configuration and|or action parameters."
        except:
            error_code = "Error code unavailable"
            error_msg = "Unknown error occurred. Please check the asset configuration and|or action parameters."

        try:
            error_msg = self._handle_py_ver_compat_for_input_str(error_msg)
        except TypeError:
            error_msg = "Error occurred while connecting to the AWS EC2. Please check the asset configuration and|or the action parameters."
        except:
            error_msg = "Unknown error occurred. Please check the asset configuration and|or action parameters."

        return "Error Code: {0}. Error Message: {1}".format(error_code, error_msg)

    def _sanitize_data(self, cur_obj):

        try:
            json.dumps(cur_obj)
            return cur_obj
        except:
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
                return re.findall('.*resource_id=\'(.*?)\',.*', str(cur_obj))[0]
            except:
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

        try:
            boto_func = getattr(self._service, method)
        except AttributeError:
            return RetVal(action_result.set_status(phantom.APP_ERROR, "Invalid method: {0}".format(method)), None)

        try:
            resp_json = boto_func(**kwargs)
        except Exception as e:
            return RetVal(action_result.set_status(phantom.APP_ERROR, 'boto3 call to ec2 failed', e), None)

        return phantom.APP_SUCCESS, self._sanitize_data(resp_json)

    def _create_client(self, service, action_result):

        boto_config = None
        if self._proxy:
            boto_config = Config(proxies=self._proxy)

        try:
            if self._access_key and self._secret_key:
                self.debug_print("Creating boto3 client with API keys")
                self._service = client(
                    service,
                    region_name=self._region,
                    aws_access_key_id=self._access_key,
                    aws_secret_access_key=self._secret_key,
                    config=boto_config)
            else:
                self.debug_print("Creating boto3 client without API keys")
                self._service = client(
                    service,
                    region_name=self._region,
                    config=boto_config)
        except Exception as e:
            error_message = self._get_error_message_from_exception(e)
            return action_result.set_status(phantom.APP_ERROR, "Could not create boto3 client: {0}".format(error_message))

        return phantom.APP_SUCCESS

    def _validate_instance_id(self, instance_id, action_result):
        if not self._create_client('ec2', action_result):
            return action_result.get_status()

        args = {
            'InstanceIds': [instance_id]
        }

        # make rest call
        ret_val, response = self._make_boto_call(action_result, 'describe_instances', **args)

        if phantom.is_fail(ret_val) or not response.get('Reservations'):
            return action_result.set_status(phantom.APP_ERROR, 'Please provide a valid instance ID')

        return action_result.set_status(phantom.APP_SUCCESS)

    def _create_instance(self, identifier, action_result):

        boto_config = None

        # Validate the instance ID
        ret_val = self._validate_instance_id(identifier, action_result)

        if phantom.is_fail(ret_val):
            return action_result.get_status()

        if self._proxy:
            boto_config = Config(proxies=self._proxy)

        try:
            if self._access_key and self._secret_key:
                self.debug_print("Creating boto3 client with API keys")
                ec2 = resource(
                    'ec2',
                    region_name=self._region,
                    aws_access_key_id=self._access_key,
                    aws_secret_access_key=self._secret_key,
                    config=boto_config)
                self._service = ec2.Instance(identifier)
            else:
                self.debug_print("Creating boto3 client without API keys")
                ec2 = resource(
                    'ec2',
                    region_name=self._region,
                    config=boto_config)
                self._service = ec2.Instance(identifier)
        except Exception as e:
            error_message = self._get_error_message_from_exception(e)
            return action_result.set_status(phantom.APP_ERROR, "Could not create boto3 instance: {0}".format(error_message))

        return phantom.APP_SUCCESS

    def _create_network_interface(self, identifier, action_result):

        boto_config = None
        if self._proxy:
            boto_config = Config(proxies=self._proxy)

        try:
            if self._access_key and self._secret_key:
                self.debug_print("Creating boto3 client with API keys")
                ec2 = resource(
                    'ec2',
                    region_name=self._region,
                    aws_access_key_id=self._access_key,
                    aws_secret_access_key=self._secret_key,
                    config=boto_config)
                self._service = ec2.NetworkInterface(identifier)
            else:
                self.debug_print("Creating boto3 client without API keys")
                ec2 = resource(
                    'ec2',
                    region_name=self._region,
                    config=boto_config)
                self._service = ec2.NetworkInterface(identifier)
        except Exception as e:
            error_message = self._get_error_message_from_exception(e)
            return action_result.set_status(phantom.APP_ERROR, "Could not create boto3 network interface: {0}".format(error_message))

        return phantom.APP_SUCCESS

    def _create_vpc(self, vpc_id, action_result):

        boto_config = None
        if self._proxy:
            boto_config = Config(proxies=self._proxy)

        try:
            if self._access_key and self._secret_key:
                self.debug_print("Creating boto3 client with API keys")
                ec2 = resource(
                    'ec2',
                    region_name=self._region,
                    aws_access_key_id=self._access_key,
                    aws_secret_access_key=self._secret_key,
                    config=boto_config)
                self._service = ec2.Vpc(vpc_id)
            else:
                self.debug_print("Creating boto3 client without API keys")
                ec2 = resource(
                    'ec2',
                    region_name=self._region,
                    config=boto_config)
                self._service = ec2.Vpc(vpc_id)
        except Exception as e:
            error_message = self._get_error_message_from_exception(e)
            return action_result.set_status(phantom.APP_ERROR, "Could not create boto3 security group: {0}".format(error_message))

        return phantom.APP_SUCCESS

    def _handle_test_connectivity(self, param):

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        self.save_progress("Querying AWS to check credentials")

        if not self._create_client('ec2', action_result):
            return action_result.get_status()

        # make rest call
        ret_val, resp_json = self._make_boto_call(action_result, 'describe_security_groups', MaxResults=5)

        if (phantom.is_fail(ret_val)):
            self.save_progress("Test Connectivity Failed")
            return action_result.get_status()

        # Return success
        self.save_progress("Test Connectivity Passed")
        return action_result.set_status(phantom.APP_SUCCESS)

    def _paginator(self, method_name, limit, action_result, **kwargs):
        """
        Handles the pagination
        """

        list_items = list()
        next_token = None

        if self.get_action_identifier() == 'describe_instance' and 'InstanceIds' not in kwargs:
            kwargs['MaxResults'] = EC2_MAX_RESULTS_LIMIT

        while True:
            if next_token:
                ret_val, response = self._make_boto_call(action_result, method_name, NextToken=next_token, **kwargs)
            else:
                ret_val, response = self._make_boto_call(action_result, method_name, **kwargs)

            if phantom.is_fail(ret_val):
                return None

            list_items.extend(response.get('Reservations'))

            if limit and len(list_items) >= limit:
                return list_items[:limit]

            next_token = response.get('NextToken')
            if not next_token:
                break

        return list_items

    def _handle_describe_instance(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client('ec2', action_result):
            return action_result.get_status()

        filters = self._handle_py_ver_compat_for_input_str(param.get('filters'))
        instance_ids = self._handle_py_ver_compat_for_input_str(param.get('instance_ids'))
        dry_run = param.get('dry_run')
        limit = param.get('limit')

        if (limit and not str(limit).isdigit()) or limit == 0:
            return action_result.set_status(phantom.APP_ERROR, EC2_INVALID_LIMIT_MSG.format(param_name='limit'))

        args = dict()
        if filters:
            try:
                evaluated_filters = list(ast.literal_eval(filters))
                # If only one filter
                if type(evaluated_filters[0]) == str:
                    args['Filters'] = [ast.literal_eval(filters)]
                else:
                    args['Filters'] = evaluated_filters
            except Exception as e:
                error_message = self._get_error_message_from_exception(e)
                return action_result.set_status(phantom.APP_ERROR, 'Error occured while parsing filter : {0}'.format(error_message))

        if instance_ids:
            args['InstanceIds'] = [item.strip() for item in instance_ids.split(',')]
        if dry_run:
            args['DryRun'] = dry_run

        list_reservations = self._paginator('describe_instances', limit, action_result, **args)

        if list_reservations is None:
            self.save_progress('No reservations found')
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

    def _handle_start_instance(self, param):
        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client('ec2', action_result):
            return action_result.get_status()

        instance_ids = self._handle_py_ver_compat_for_input_str(param['instance_ids'])
        dry_run = param.get('dry_run', False)

        instance_ids_list = [x.strip() for x in instance_ids.split(',')]
        instance_ids_list = ' '.join(instance_ids_list).split()

        args = {
            "InstanceIds": instance_ids_list
        }
        if dry_run:
            args['DryRun'] = dry_run

        # make rest call
        ret_val, response = self._make_boto_call(action_result, 'start_instances', **args)

        if (phantom.is_fail(ret_val)):
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

        if not self._create_client('ec2', action_result):
            return action_result.get_status()

        instance_ids = self._handle_py_ver_compat_for_input_str(param['instance_ids'])
        force = param.get('force', False)
        dry_run = param.get('dry_run', False)

        instance_ids_list = [x.strip() for x in instance_ids.split(',')]
        instance_ids_list = ' '.join(instance_ids_list).split()

        args = {
            "InstanceIds": instance_ids_list
        }
        if force:
            args['Force'] = force
        if dry_run:
            args['DryRun'] = dry_run

        # make rest call
        ret_val, response = self._make_boto_call(action_result, 'stop_instances', **args)

        if (phantom.is_fail(ret_val)):
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

        if not self._create_client('autoscaling', action_result):
            return action_result.get_status()

        instance_ids = self._handle_py_ver_compat_for_input_str(param.get('instance_ids'))
        autoscaling_group_name = self._handle_py_ver_compat_for_input_str(param['autoscaling_group_name'])
        should_decrement_desired_capacity = param.get('should_decrement_desired_capacity', False)

        args = {
            'AutoScalingGroupName': autoscaling_group_name,
            'ShouldDecrementDesiredCapacity': should_decrement_desired_capacity
        }
        if instance_ids:
            args['InstanceIds'] = [item.strip() for item in instance_ids.split(',')]

        # make rest call
        ret_val, response = self._make_boto_call(action_result, 'detach_instances', **args)

        if (phantom.is_fail(ret_val)):
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

        if not self._create_client('autoscaling', action_result):
            return action_result.get_status()

        instance_ids = self._handle_py_ver_compat_for_input_str(param.get('instance_ids'))
        autoscaling_group_name = self._handle_py_ver_compat_for_input_str(param['autoscaling_group_name'])

        args = {
            'AutoScalingGroupName': autoscaling_group_name
        }
        if instance_ids:
            args['InstanceIds'] = [item.strip() for item in instance_ids.split(',')]

        # make rest call
        ret_val, response = self._make_boto_call(action_result, 'attach_instances', **args)

        if (phantom.is_fail(ret_val)):
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

        if not self._create_client('elb', action_result):
            return action_result.get_status()

        load_balancer_name = self._handle_py_ver_compat_for_input_str(param['load_balancer_name'])
        instance_ids = self._handle_py_ver_compat_for_input_str(param['instance_ids'])
        instance_id_dict = [{'InstanceId': item.strip()} for item in instance_ids.split(',')]

        args = {
            'LoadBalancerName': load_balancer_name,
            'Instances': instance_id_dict
        }

        # make rest call
        ret_val, response = self._make_boto_call(action_result, 'deregister_instances_from_load_balancer', **args)

        if (phantom.is_fail(ret_val)):
            return action_result.get_status()

        # Add the response into the data section
        action_result.add_data(response)

        # Add a dictionary that is made up of the most important values from data into the summary
        summary = action_result.update_summary({})
        summary['status'] = "Successfully deregistered instance"

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_snapshot_instance(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client('ec2', action_result):
            return action_result.get_status()

        volume_id = self._handle_py_ver_compat_for_input_str(param['volume_id'])
        description = self._handle_py_ver_compat_for_input_str(param.get('description'))
        tag_specifications = self._handle_py_ver_compat_for_input_str(param.get('tag_specifications'))
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

        if (phantom.is_fail(ret_val)):
            return action_result.get_status()

        # Add the response into the data section
        action_result.add_data(response)

        # Add a dictionary that is made up of the most important values from data into the summary
        summary = action_result.update_summary({})
        summary['snapshot_id'] = len(response.get('SnapshotId', {}))

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_add_tag(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        instance_id = self._handle_py_ver_compat_for_input_str(param['instance_id'])

        if not self._create_instance(instance_id, action_result):
            return action_result.get_status()

        tag_key = self._handle_py_ver_compat_for_input_str(param.get('tag_key'))
        tag_value = self._handle_py_ver_compat_for_input_str(param.get('tag_value', ""))
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

        if (phantom.is_fail(ret_val)):
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

        instance_id = self._handle_py_ver_compat_for_input_str(param['instance_id'])
        tag_key = self._handle_py_ver_compat_for_input_str(param['tag_key'])
        dry_run = param.get('dry_run', False)

        if not self._create_client('ec2', action_result):
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

        if (phantom.is_fail(ret_val)):
            return action_result.get_status()

        if not response:
            return action_result.get_status()

        if not response.get('Tags'):
            return action_result.set_status(phantom.APP_ERROR, 'No tags found with the tag key: {0} in the instance with ID: {1}'.format(tag_key, instance_id))

        # Add the response into the data section
        # The output response will consist of a unique dictionary for given tag
        # Hence, extracting the first element of the tags list
        action_result.add_data(response.get('Tags')[0])

        return action_result.set_status(phantom.APP_SUCCESS, 'Successfully fetched the tag value')

    def _handle_remove_tag(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        instance_id = self._handle_py_ver_compat_for_input_str(param['instance_id'])

        if not self._create_instance(instance_id, action_result):
            return action_result.get_status()

        tag_key = self._handle_py_ver_compat_for_input_str(param.get('tag_key'))
        tag_value = self._handle_py_ver_compat_for_input_str(param.get('tag_value'))
        dry_run = param.get('dry_run')

        args = dict()
        tags_dict = dict()

        if not tag_key and tag_value:
            return action_result.set_status(phantom.APP_ERROR, 'Providing tag value without a tag key performs nothing and hence, it is not allowed')

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

        if (phantom.is_fail(ret_val)):
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

        if not self._create_client('ec2', action_result):
            return action_result.get_status()

        filters = self._handle_py_ver_compat_for_input_str(param.get('filters'))
        dry_run = param.get('dry_run')
        network_acl_ids = self._handle_py_ver_compat_for_input_str(param.get('network_acl_ids'))

        args = dict()
        if filters:
            try:
                evaluated_filters = list(ast.literal_eval(filters))
                # If only one filter
                if type(evaluated_filters[0]) == str:
                    args['Filters'] = [ast.literal_eval(filters)]
                else:
                    args['Filters'] = evaluated_filters
            except Exception as e:
                error_message = self._get_error_message_from_exception(e)
                return action_result.set_status(phantom.APP_ERROR, 'Error occured while parsing filter : {}'.format(error_message))
        if dry_run:
            args['DryRun'] = dry_run
        if network_acl_ids:
            args['NetworkAclIds'] = [item.strip() for item in network_acl_ids.split(',')]

        # make rest call
        ret_val, response = self._make_boto_call(action_result, 'describe_network_acls', **args)

        if (phantom.is_fail(ret_val)):
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

        if not self._create_client('ec2', action_result):
            return action_result.get_status()

        vpc_id = self._handle_py_ver_compat_for_input_str(param['vpc_id'])
        dry_run = param.get('dry_run')
        args = {
            "VpcId": vpc_id
        }
        if dry_run:
            args['DryRun'] = dry_run

        # make rest call
        ret_val, response = self._make_boto_call(action_result, 'create_network_acl', **args)

        if (phantom.is_fail(ret_val)):
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

        if not self._create_client('ec2', action_result):
            return action_result.get_status()

        network_acl_id = self._handle_py_ver_compat_for_input_str(param['network_acl_id'])
        dry_run = param.get('dry_run')

        args = {
            'NetworkAclId': network_acl_id
        }
        if dry_run:
            args['DryRun'] = dry_run

        # make rest call
        ret_val, response = self._make_boto_call(action_result, 'delete_network_acl', **args)

        if (phantom.is_fail(ret_val)):
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

        if not self._create_client('ec2', action_result):
            return action_result.get_status()

        filters = self._handle_py_ver_compat_for_input_str(param.get('filters'))
        dry_run = param.get('dry_run')
        group_ids = self._handle_py_ver_compat_for_input_str(param.get('group_ids'))
        group_names = self._handle_py_ver_compat_for_input_str(param.get('group_names'))
        next_token = self._handle_py_ver_compat_for_input_str(param.get('next_token'))
        max_results = param.get('max_results')

        args = dict()
        if filters:
            try:
                evaluated_filters = list(ast.literal_eval(filters))
                # If only one filter
                if type(evaluated_filters[0]) == str:
                    args['Filters'] = [ast.literal_eval(filters)]
                else:
                    args['Filters'] = evaluated_filters
            except Exception as e:
                error_message = self._get_error_message_from_exception(e)
                return action_result.set_status(phantom.APP_ERROR, 'Error occured while parsing filter : {}'.format(error_message))
        if group_ids:
            args['GroupIds'] = group_ids.split(',')
        if group_names:
            args['GroupNames'] = group_names.split(',')
        if dry_run:
            args['DryRun'] = dry_run
        if next_token:
            args['NextToken'] = next_token
        if max_results is not None:
            args['MaxResults'] = max_results

        # make rest call
        ret_val, response = self._make_boto_call(action_result, 'describe_security_groups', **args)

        if (phantom.is_fail(ret_val)):
            return action_result.get_status()

        # Add the response into the data section
        action_result.add_data(response)

        # Add a dictionary that is made up of the most important values from data into the summary
        summary = action_result.update_summary({})
        summary['num_security_groups'] = len(response.get('SecurityGroups', {}))

        return action_result.set_status(phantom.APP_SUCCESS)

    def _security_group_helper(self, instance_id, action_result):

        # Get original list of security groups associated with network interface id
        if not self._create_client('ec2', action_result):
            return action_result.get_status()

        args = {
            'InstanceIds': [instance_id]
        }

        # make rest call
        ret_val, response = self._make_boto_call(action_result, 'describe_instances', **args)

        if (phantom.is_fail(ret_val)):
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
            return (action_result.set_status(phantom.APP_ERROR, 'Error occurred while fetching the group list and network interface ID for given instance ID'), None, None)

        return (phantom.APP_SUCCESS, group_list, network_interface_id)

    def _handle_assign_instance_to_group(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        group_to_add = self._handle_py_ver_compat_for_input_str(param['group_id'])
        instance_id = self._handle_py_ver_compat_for_input_str(param['instance_id'])
        ret_val, group_list, network_interface_id = self._security_group_helper(instance_id, action_result)
        if (phantom.is_fail(ret_val)):
            return action_result.get_status()

        # Try to add the parameterized group from the list
        if group_to_add not in group_list:
            group_list.append(group_to_add)
        else:
            return action_result.set_status(phantom.APP_SUCCESS, "Instance already included in security group")

        # Now that you have the list of original groups, remove the one provided by the user and post the new list
        if not self._create_network_interface(network_interface_id, action_result):
            return action_result.get_status()

        args = {
            'Groups': group_list
        }

        # make rest call
        ret_val, response = self._make_boto_call(action_result, 'modify_attribute', **args)

        if (phantom.is_fail(ret_val)):
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

            Get original group list, create list of groups without parameterized group, then update group list
        '''

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        group_to_remove = self._handle_py_ver_compat_for_input_str(param['group_id'])
        instance_id = self._handle_py_ver_compat_for_input_str(param['instance_id'])

        ret_val, group_list, network_interface_id = self._security_group_helper(instance_id, action_result)

        if (phantom.is_fail(ret_val)):
            return action_result.get_status()

        # Try to remove the parameterized group from the list
        try:
            group_list.remove(group_to_remove)
        except:
            return action_result.set_status(phantom.APP_SUCCESS, "Instance already not included in security group")

        # Now that you have the list of original groups, remove the one provided by the user and post the new list
        if not self._create_network_interface(network_interface_id, action_result):
            return action_result.get_status()

        args = {
            'Groups': group_list
        }

        # make rest call
        ret_val, response = self._make_boto_call(action_result, 'modify_attribute', **args)

        if (phantom.is_fail(ret_val)):
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

        if not self._create_client('ec2', action_result):
            return action_result.get_status()

        cidr_block = self._handle_py_ver_compat_for_input_str(param['cidr_block'])
        amazon_provided_ipv6_cidr_block = param.get('amazon_provided_ipv6_cidr_block')
        dry_run = param.get('dry_run')
        instance_tenancy = self._handle_py_ver_compat_for_input_str(param.get('instance_tenancy'))

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

        if (phantom.is_fail(ret_val)):
            return action_result.get_status()

        # Add the response into the data section
        action_result.add_data(response)

        # Add a dictionary that is made up of the most important values from data into the summary
        summary = action_result.update_summary({})
        summary['vpc_id'] = response.get('Vpc', {}).get('VpcId', 'Unavailable')
        summary['instance_tenancy'] = response.get('Vpc', {}).get('InstanceTenancy', 'Unavailable')

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_list_network_interfaces(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client('ec2', action_result):
            return action_result.get_status()

        filters = self._handle_py_ver_compat_for_input_str(param.get('filters'))
        dry_run = param.get('dry_run')
        network_interface_ids = self._handle_py_ver_compat_for_input_str(param.get('network_interface_ids'))
        next_token = self._handle_py_ver_compat_for_input_str(param.get('next_token'))
        max_results = param.get('max_results')

        args = dict()
        if filters:
            try:
                evaluated_filters = list(ast.literal_eval(filters))
                # If only one filter
                if type(evaluated_filters[0]) == str:
                    args['Filters'] = [ast.literal_eval(filters)]
                else:
                    args['Filters'] = evaluated_filters
            except Exception as e:
                error_message = self._get_error_message_from_exception(e)
                return action_result.set_status(phantom.APP_ERROR, 'Error occured while parsing filter : {}'.format(error_message))
        if dry_run:
            args['DryRun'] = dry_run
        if network_interface_ids:
            args['NetworkInterfaceIds'] = [item.strip() for item in network_interface_ids.split(',')]
        if next_token:
            args['NextToken'] = next_token
        if max_results is not None:
            args['MaxResults'] = max_results

        # make rest call
        ret_val, response = self._make_boto_call(action_result, 'describe_network_interfaces', **args)
        if (phantom.is_fail(ret_val)):
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

        if not self._create_client('autoscaling', action_result):
            return action_result.get_status()

        autoscaling_group_names = self._handle_py_ver_compat_for_input_str(param.get('autoscaling_group_names'))
        next_token = self._handle_py_ver_compat_for_input_str(param.get('next_token'))
        max_results = param.get('max_results')

        args = dict()
        if autoscaling_group_names:
            args['AutoScalingGroupNames'] = [item.strip() for item in autoscaling_group_names.split(',')]
        if next_token:
            args['NextToken'] = next_token
        # This is a special case where the key is 'MaxRecords' instead of 'MaxResults'
        if max_results is not None:
            args['MaxRecords'] = max_results

        # make rest call
        ret_val, response = self._make_boto_call(action_result, 'describe_auto_scaling_groups', **args)

        if (phantom.is_fail(ret_val)):
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

        if action_id == 'test_connectivity':
            ret_val = self._handle_test_connectivity(param)

        elif action_id == 'describe_instance':
            ret_val = self._handle_describe_instance(param)

        elif action_id == 'start_instance':
            ret_val = self._handle_start_instance(param)

        elif action_id == 'stop_instance':
            ret_val = self._handle_stop_instance(param)

        elif action_id == 'detach_instance':
            ret_val = self._handle_detach_instance(param)

        elif action_id == 'attach_instance':
            ret_val = self._handle_attach_instance(param)

        elif action_id == 'deregister_instance':
            ret_val = self._handle_deregister_instance(param)

        elif action_id == 'snapshot_instance':
            ret_val = self._handle_snapshot_instance(param)

        elif action_id == 'get_tag':
            ret_val = self._handle_get_tag(param)

        elif action_id == 'add_tag':
            ret_val = self._handle_add_tag(param)

        elif action_id == 'remove_tag':
            ret_val = self._handle_remove_tag(param)

        elif action_id == 'get_acls':
            ret_val = self._handle_get_acls(param)

        elif action_id == 'add_acl':
            ret_val = self._handle_add_acl(param)

        elif action_id == 'remove_acl':
            ret_val = self._handle_remove_acl(param)

        elif action_id == 'list_security_groups':
            ret_val = self._handle_list_security_groups(param)

        elif action_id == 'assign_instance_to_group':
            ret_val = self._handle_assign_instance_to_group(param)

        elif action_id == 'remove_instance_from_group':
            ret_val = self._handle_remove_instance_from_group(param)

        elif action_id == 'create_vpc':
            ret_val = self._handle_create_vpc(param)

        elif action_id == 'list_network_interfaces':
            ret_val = self._handle_list_network_interfaces(param)

        elif action_id == 'list_autoscaling_groups':
            ret_val = self._handle_list_autoscaling_groups(param)

        return ret_val

    def initialize(self):

        # Load the state in initialize, use it to store data
        # that needs to be accessed across actions
        try:
            self._python_version = int(sys.version_info[0])
        except:
            return self.set_status(phantom.APP_ERROR, "Error occurred while getting the Phantom server's Python major version.")

        self._state = self.load_state()

        # get the asset config
        config = self.get_config()

        if EC2_JSON_ACCESS_KEY in config:
            self._access_key = self._handle_py_ver_compat_for_input_str(config.get(EC2_JSON_ACCESS_KEY))
        if EC2_JSON_SECRET_KEY in config:
            self._secret_key = self._handle_py_ver_compat_for_input_str(config.get(EC2_JSON_SECRET_KEY))

        self._region = EC2_REGION_DICT.get(config[EC2_JSON_REGION])

        self._proxy = {}
        env_vars = config.get('_reserved_environment_variables', {})
        if 'HTTP_PROXY' in env_vars:
            self._proxy['http'] = env_vars['HTTP_PROXY']['value']
        if 'HTTPS_PROXY' in env_vars:
            self._proxy['https'] = env_vars['HTTPS_PROXY']['value']

        return phantom.APP_SUCCESS

    def finalize(self):

        # Save the state, this data is saved across actions and app upgrades
        self.save_state(self._state)
        return phantom.APP_SUCCESS


if __name__ == '__main__':

    import pudb
    import argparse

    pudb.set_trace()

    argparser = argparse.ArgumentParser()

    argparser.add_argument('input_test_json', help='Input Test JSON file')
    argparser.add_argument('-u', '--username', help='username', required=False)
    argparser.add_argument('-p', '--password', help='password', required=False)

    args = argparser.parse_args()
    session_id = None

    username = args.username
    password = args.password

    if (username is not None and password is None):

        # User specified a username but not a password, so ask
        import getpass
        password = getpass.getpass("Password: ")

    if (username and password):
        try:
            login_url = AwsEc2Connector._get_phantom_base_url() + '/login'

            print("Accessing the Login page")
            r = requests.get(login_url, verify=False)
            csrftoken = r.cookies['csrftoken']

            data = dict()
            data['username'] = username
            data['password'] = password
            data['csrfmiddlewaretoken'] = csrftoken

            headers = dict()
            headers['Cookie'] = 'csrftoken=' + csrftoken
            headers['Referer'] = login_url

            print("Logging into Platform to get the session id")
            r2 = requests.post(login_url, verify=False, data=data, headers=headers)
            session_id = r2.cookies['sessionid']
        except Exception as e:
            print("Unable to get session id from the platform. Error: " + str(e))
            exit(1)

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

    exit(0)
