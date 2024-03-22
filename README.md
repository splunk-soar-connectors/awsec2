[comment]: # "Auto-generated SOAR connector documentation"
# AWS EC2

Publisher: Splunk  
Connector Version: 2.4.3  
Product Vendor: AWS  
Product Name: EC2  
Product Version Supported (regex): ".\*"  
Minimum Product Version: 5.3.5  

This app integrates with AWS Elastic Compute Cloud (EC2) to perform virtualization actions

[comment]: # " File: README.md"
[comment]: # "  Copyright (c) 2019-2024 Splunk Inc."
[comment]: # ""
[comment]: # "Licensed under the Apache License, Version 2.0 (the 'License');"
[comment]: # "you may not use this file except in compliance with the License."
[comment]: # "You may obtain a copy of the License at"
[comment]: # ""
[comment]: # "    http://www.apache.org/licenses/LICENSE-2.0"
[comment]: # ""
[comment]: # "Unless required by applicable law or agreed to in writing, software distributed under"
[comment]: # "the License is distributed on an 'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,"
[comment]: # "either express or implied. See the License for the specific language governing permissions"
[comment]: # "and limitations under the License."
[comment]: # ""
Dry Run parameter when enabled, checks whether the user has the required permissions for the action,
without actually making the request, and provides an error response in every scenario. If the user
has the required permissions, the error response is **DryRunOperation** , otherwise, it is
**UnauthorizedOperation.**

## Asset Configuration

There are two ways to configure an AWS EC2 asset. The first is to configure the **access_key** ,
**secret_key** and **region** variables. If it is preferred to use a role and Phantom is running as
an EC2 instance, the **use_role** check box can be checked instead. This will allow the role that is
attached to the instance to be used. Please see the [AWS EC2 and IAM
documentation](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html)
for more information. Note that checking the **use_role** check box in the asset configuration will
*override* the access and secret keys if they are already set.

## Assumed Role Credentials

The optional **credentials** action parameter consists of temporary **assumed role** credentials
that will be used to perform the action instead of those that are configured in the **asset** . The
parameter is not designed to be configured manually, but should be used in conjunction with the
Phantom AWS Security Token Service app. The output of the **assume_role** action of the STS app with
data path **assume_role\_\<number>:action_result.data.\*.Credentials** consists of a dictionary
containing the **AccessKeyId** , **SecretAccessKey** , **SessionToken** and **Expiration** key/value
pairs. This dictionary can be passed directly into the credentials parameter in any of the following
actions within a playbook. For more information, please see the [AWS Identity and Access Management
documentation](https://docs.aws.amazon.com/iam/index.html) .


### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a EC2 asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**access_key** |  optional  | password | Access Key
**secret_key** |  optional  | password | Secret Key
**region** |  required  | string | Default Region
**use_role** |  optional  | boolean | Use attached role when running Phantom in EC2

### Supported Actions  
[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity using supplied configuration  
[start instance](#action-start-instance) - Start one or more instances  
[stop instance](#action-stop-instance) - Stop one or more instances  
[describe instance](#action-describe-instance) - Describe one or more instances  
[create security group](#action-create-security-group) - Creates a security group  
[delete security group](#action-delete-security-group) - Deletes a security group  
[describe snapshots](#action-describe-snapshots) - Describe one or more snapshots  
[copy snapshot](#action-copy-snapshot) - Copies a point-in-time snapshot of an EBS volume and stores it in Amazon S3  
[describe vpcs](#action-describe-vpcs) - Describe one or more vpcs  
[describe images](#action-describe-images) - Describe one or more images  
[describe subnets](#action-describe-subnets) - Describe one or more subnets  
[detach instance](#action-detach-instance) - Detach an instance from an autoscaling group  
[attach instance](#action-attach-instance) - Attach an instance to an autoscaling group  
[delete vpc](#action-delete-vpc) - Delete a VPC  
[register instance](#action-register-instance) - Register an instance to a Classic AWS Elastic Load Balancer  
[deregister instance](#action-deregister-instance) - Deregister an instance from a Classic AWS Elastic Load Balancer  
[delete snapshot](#action-delete-snapshot) - Delete snapshot of given AWS instance  
[snapshot instance](#action-snapshot-instance) - Snapshot AWS instance that has the given IP address or instance ID  
[get tag](#action-get-tag) - Get the value of a tag for the given instance ID  
[add tag](#action-add-tag) - Add a tag to an instance  
[remove tag](#action-remove-tag) - Remove specified tag from an instance  
[get acls](#action-get-acls) - Get one or more network ACLs  
[add acl](#action-add-acl) - Add ACL to an instance  
[remove acl](#action-remove-acl) - Remove ACL from an instance. The default network ACL and ACLs associated with any subnets cannot be deleted  
[list security groups](#action-list-security-groups) - Describe one or more security groups  
[assign instance](#action-assign-instance) - Assign an instance to a security group  
[remove instance](#action-remove-instance) - Removes an instance from a security group  
[create vpc](#action-create-vpc) - Create a VPC with the specified IPv4 CIDR block  
[list network interfaces](#action-list-network-interfaces) - Display network interfaces  
[list autoscaling groups](#action-list-autoscaling-groups) - Display autoscaling groups  

## action: 'test connectivity'
Validate the asset configuration for connectivity using supplied configuration

Type: **test**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output  

## action: 'start instance'
Start one or more instances

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**instance_ids** |  required  | One or more instance IDs, separated by commas | string |  `aws ec2 instance id` 
**dry_run** |  optional  | Check if asset has required permissions for the action | boolean | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.credentials | string |  `aws credentials`  |   {'AccessKeyId': 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration': '2020-12-09 22:28:04', 'SecretAccessKey': 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken': 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ+yY5Qk2QpWctS2BGn4n+G8cD6zEweCCMj+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='} 
action_result.parameter.dry_run | boolean |  |   True  False 
action_result.parameter.instance_ids | string |  `aws ec2 instance id`  |   i-0d872de1de2ea7640,i-059d3667cb8b94f39 
action_result.data.\*.CurrentState.Code | numeric |  |   0 
action_result.data.\*.CurrentState.Name | string |  |   pending 
action_result.data.\*.InstanceId | string |  `aws ec2 instance id`  |   i-0d872de1de2ea7640 
action_result.data.\*.PreviousState.Code | numeric |  |   80 
action_result.data.\*.PreviousState.Name | string |  |   stopped 
action_result.summary | string |  |  
action_result.message | string |  |   Instances started successfully 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'stop instance'
Stop one or more instances

Type: **generic**  
Read only: **False**

If the force parameter is enabled, the instances do not have an opportunity to flush file system caches or file system metadata. If this option is enabled, you must perform file system check and repair procedures. This option is not recommended for Windows instances.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**instance_ids** |  required  | One or more instance IDs, separated by commas | string |  `aws ec2 instance id` 
**force** |  optional  | Forces the instances to stop | boolean | 
**dry_run** |  optional  | Check if asset has required permissions for the action | boolean | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.credentials | string |  `aws credentials`  |   {'AccessKeyId': 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration': '2020-12-09 22:28:04', 'SecretAccessKey': 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken': 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ+yY5Qk2QpWctS2BGn4n+G8cD6zEweCCMj+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='} 
action_result.parameter.dry_run | boolean |  |   True  False 
action_result.parameter.force | boolean |  |   True  False 
action_result.parameter.instance_ids | string |  `aws ec2 instance id`  |   i-0d872de1de2ea7640,i-059d3667cb8b94f39 
action_result.data.\*.CurrentState.Code | numeric |  |   64 
action_result.data.\*.CurrentState.Name | string |  |   stopping 
action_result.data.\*.InstanceId | string |  `aws ec2 instance id`  |   i-0d872de1de2ea7640 
action_result.data.\*.PreviousState.Code | numeric |  |   16 
action_result.data.\*.PreviousState.Name | string |  |   running 
action_result.summary | string |  |  
action_result.message | string |  |   Instances stopped successfully 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'describe instance'
Describe one or more instances

Type: **investigate**  
Read only: **True**

It is not suggested to use the limit parameter when 'instance ids' parameter is used or instance-id is used as filter criteria in the filters parameter. But, if the limit parameter is used along with the above-mentioned parameters, the number of instances fetched will be driven by the limit parameter value.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**filters** |  optional  | One or more filters, separated by commas | string | 
**instance_ids** |  optional  | One or more instance IDs, separated by commas | string |  `aws ec2 instance id` 
**limit** |  optional  | The maximum number of results to be fetched | numeric | 
**dry_run** |  optional  | Check if asset has required permissions for the action | boolean | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.credentials | string |  `aws credentials`  |   {'AccessKeyId': 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration': '2020-12-09 22:28:04', 'SecretAccessKey': 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken': 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ+yY5Qk2QpWctS2BGn4n+G8cD6zEweCCMj+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='} 
action_result.parameter.dry_run | boolean |  |   True  False 
action_result.parameter.filters | string |  |   { "Name": "vpc-id", "Values": [ "vpc-0840e9850b3f02915"]} 
action_result.parameter.instance_ids | string |  `aws ec2 instance id`  |   i-002f4885c00dd08cf0 
action_result.parameter.limit | numeric |  |   35 
action_result.data.\*.NextToken | string |  `aws ec2 next token`  |   eyJ2IjoiMiIsImMiOiJxTVBvSm9GZmpOVFhrc2RYL0RDK3htaytZR0luRDhuTWR6SnN6VWNHcStSWGRwWTJ2cWtxZlBUWjY1QjJ3VzZRNlFqRkZaUzVrRDQ2V1lzTVpsY2dPSS9mVWNqVlVIbCtpaHV6b1dybnJWbXoxclp0T25YR3NvWVJRQkFuamhqaDlEN2o2dEtvcjB6bDBoeVo3clB2eGZOUlZxQUYzdWo5WnJKbTRRSmZqbHQzS0h1REhkWFI1Q1VmZnRLU2k2RkxhTkhaaUVkbXNPUlMwYnNYbkhVSHEwT0x1SmhEb2thTkc3R0tORkhaeWtIZCIsInMiOiIxIn0= 
action_result.data.\*.Reservations.\*.Instances.\*.AmiLaunchIndex | numeric |  |   0 
action_result.data.\*.Reservations.\*.Instances.\*.Architecture | string |  |   x86_64 
action_result.data.\*.Reservations.\*.Instances.\*.BlockDeviceMappings.\*.DeviceName | string |  |   /dev/xvda 
action_result.data.\*.Reservations.\*.Instances.\*.BlockDeviceMappings.\*.Ebs.AttachTime | string |  |   2019-02-13 23:20:22 
action_result.data.\*.Reservations.\*.Instances.\*.BlockDeviceMappings.\*.Ebs.DeleteOnTermination | boolean |  |   True  False 
action_result.data.\*.Reservations.\*.Instances.\*.BlockDeviceMappings.\*.Ebs.Status | string |  |   attached 
action_result.data.\*.Reservations.\*.Instances.\*.BlockDeviceMappings.\*.Ebs.VolumeId | string |  |   vol-0d8d4d266ac6ea76f 
action_result.data.\*.Reservations.\*.Instances.\*.CapacityReservationSpecification.CapacityReservationPreference | string |  |   open 
action_result.data.\*.Reservations.\*.Instances.\*.ClientToken | string |  |   155010001974811618 
action_result.data.\*.Reservations.\*.Instances.\*.CpuOptions.CoreCount | numeric |  |   2 
action_result.data.\*.Reservations.\*.Instances.\*.CpuOptions.ThreadsPerCore | numeric |  |   1 
action_result.data.\*.Reservations.\*.Instances.\*.EbsOptimized | boolean |  |   True  False 
action_result.data.\*.Reservations.\*.Instances.\*.EnaSupport | boolean |  |   True  False 
action_result.data.\*.Reservations.\*.Instances.\*.EnclaveOptions.Enabled | boolean |  |   True  False 
action_result.data.\*.Reservations.\*.Instances.\*.HibernationOptions.Configured | boolean |  |   True  False 
action_result.data.\*.Reservations.\*.Instances.\*.Hypervisor | string |  |   xen 
action_result.data.\*.Reservations.\*.Instances.\*.IamInstanceProfile.Arn | string |  |   arn:aws:iam::849257271967:instance-profile/test-1 
action_result.data.\*.Reservations.\*.Instances.\*.IamInstanceProfile.Id | string |  |   AIPAJBUYA2ZYFKHJ7WJJ4 
action_result.data.\*.Reservations.\*.Instances.\*.ImageId | string |  |   ami-061573a27231c6d25 
action_result.data.\*.Reservations.\*.Instances.\*.InstanceId | string |  `aws ec2 instance id`  |   i-074f52e85356829a3 
action_result.data.\*.Reservations.\*.Instances.\*.InstanceType | string |  |   t2.medium 
action_result.data.\*.Reservations.\*.Instances.\*.KeyName | string |  |   test-lab-ssh-keypair 
action_result.data.\*.Reservations.\*.Instances.\*.LaunchTime | string |  |   2019-02-13 23:20:21 
action_result.data.\*.Reservations.\*.Instances.\*.MetadataOptions.HttpEndpoint | string |  |   enabled 
action_result.data.\*.Reservations.\*.Instances.\*.MetadataOptions.HttpPutResponseHopLimit | numeric |  |   1 
action_result.data.\*.Reservations.\*.Instances.\*.MetadataOptions.HttpTokens | string |  |   optional 
action_result.data.\*.Reservations.\*.Instances.\*.MetadataOptions.State | string |  |   applied 
action_result.data.\*.Reservations.\*.Instances.\*.Monitoring.State | string |  |   disabled 
action_result.data.\*.Reservations.\*.Instances.\*.NetworkInterfaces.\*.Association.IpOwnerId | string |  |   amazon 
action_result.data.\*.Reservations.\*.Instances.\*.NetworkInterfaces.\*.Association.PublicDnsName | string |  |   ec2-122-122-122-122.compute-1.amazonaws.com 
action_result.data.\*.Reservations.\*.Instances.\*.NetworkInterfaces.\*.Association.PublicIp | string |  `ip`  |   122.122.122.122 
action_result.data.\*.Reservations.\*.Instances.\*.NetworkInterfaces.\*.Attachment.AttachTime | string |  |   2019-02-13 23:20:21 
action_result.data.\*.Reservations.\*.Instances.\*.NetworkInterfaces.\*.Attachment.AttachmentId | string |  |   eni-attach-06d2e082fd98083ca 
action_result.data.\*.Reservations.\*.Instances.\*.NetworkInterfaces.\*.Attachment.DeleteOnTermination | boolean |  |   True  False 
action_result.data.\*.Reservations.\*.Instances.\*.NetworkInterfaces.\*.Attachment.DeviceIndex | numeric |  |   0 
action_result.data.\*.Reservations.\*.Instances.\*.NetworkInterfaces.\*.Attachment.NetworkCardIndex | numeric |  |  
action_result.data.\*.Reservations.\*.Instances.\*.NetworkInterfaces.\*.Attachment.Status | string |  |   attached 
action_result.data.\*.Reservations.\*.Instances.\*.NetworkInterfaces.\*.Description | string |  |   Primary network interface 
action_result.data.\*.Reservations.\*.Instances.\*.NetworkInterfaces.\*.Groups.\*.GroupId | string |  `aws ec2 group id`  |   sg-07987bf5b796b5261 
action_result.data.\*.Reservations.\*.Instances.\*.NetworkInterfaces.\*.Groups.\*.GroupName | string |  `url`  |   Test-7-2-0-AutogenByAWSMP-4 
action_result.data.\*.Reservations.\*.Instances.\*.NetworkInterfaces.\*.InterfaceType | string |  |   interface 
action_result.data.\*.Reservations.\*.Instances.\*.NetworkInterfaces.\*.MacAddress | string |  |   12:1d:c2:5a:82:e6 
action_result.data.\*.Reservations.\*.Instances.\*.NetworkInterfaces.\*.NetworkInterfaceId | string |  `aws ec2 network interface id`  |   eni-09579cbf4e49f8f65 
action_result.data.\*.Reservations.\*.Instances.\*.NetworkInterfaces.\*.OwnerId | string |  `aws ec2 owner id`  |   849257271967 
action_result.data.\*.Reservations.\*.Instances.\*.NetworkInterfaces.\*.PrivateDnsName | string |  |   ip-122-122-122-122.ec2.internal 
action_result.data.\*.Reservations.\*.Instances.\*.NetworkInterfaces.\*.PrivateIpAddress | string |  `ip`  |   122.122.122.122 
action_result.data.\*.Reservations.\*.Instances.\*.NetworkInterfaces.\*.PrivateIpAddresses.\*.Association.IpOwnerId | string |  |   amazon 
action_result.data.\*.Reservations.\*.Instances.\*.NetworkInterfaces.\*.PrivateIpAddresses.\*.Association.PublicDnsName | string |  |   ec2-122-122-122-122.compute-1.amazonaws.com 
action_result.data.\*.Reservations.\*.Instances.\*.NetworkInterfaces.\*.PrivateIpAddresses.\*.Association.PublicIp | string |  `ip`  |   122.122.122.122 
action_result.data.\*.Reservations.\*.Instances.\*.NetworkInterfaces.\*.PrivateIpAddresses.\*.Primary | boolean |  |   True  False 
action_result.data.\*.Reservations.\*.Instances.\*.NetworkInterfaces.\*.PrivateIpAddresses.\*.PrivateDnsName | string |  |   ip-122-122-122-122.ec2.internal 
action_result.data.\*.Reservations.\*.Instances.\*.NetworkInterfaces.\*.PrivateIpAddresses.\*.PrivateIpAddress | string |  `ip`  |   122.122.122.122 
action_result.data.\*.Reservations.\*.Instances.\*.NetworkInterfaces.\*.SourceDestCheck | boolean |  |   True  False 
action_result.data.\*.Reservations.\*.Instances.\*.NetworkInterfaces.\*.Status | string |  |   in-use 
action_result.data.\*.Reservations.\*.Instances.\*.NetworkInterfaces.\*.SubnetId | string |  `aws ec2 subnet id`  |   subnet-d8782cf7 
action_result.data.\*.Reservations.\*.Instances.\*.NetworkInterfaces.\*.VpcId | string |  `aws ec2 vpc id`  |   vpc-5113dc2a 
action_result.data.\*.Reservations.\*.Instances.\*.Placement.AvailabilityZone | string |  |   us-east-1d 
action_result.data.\*.Reservations.\*.Instances.\*.Placement.GroupName | string |  |   7-2-0-Auto-Test-Group 
action_result.data.\*.Reservations.\*.Instances.\*.Placement.Tenancy | string |  |   default 
action_result.data.\*.Reservations.\*.Instances.\*.Platform | string |  |   windows 
action_result.data.\*.Reservations.\*.Instances.\*.PrivateDnsName | string |  |   ip-122-122-122-122.ec2.internal 
action_result.data.\*.Reservations.\*.Instances.\*.PrivateIpAddress | string |  `ip`  |   122.122.122.122 
action_result.data.\*.Reservations.\*.Instances.\*.ProductCodes.\*.ProductCodeId | string |  |   7azvchdfh74dcxoiwjhztgpel 
action_result.data.\*.Reservations.\*.Instances.\*.ProductCodes.\*.ProductCodeType | string |  |   marketplace 
action_result.data.\*.Reservations.\*.Instances.\*.PublicDnsName | string |  |   ec2-122-122-122-122.compute-1.amazonaws.com 
action_result.data.\*.Reservations.\*.Instances.\*.PublicIpAddress | string |  `ip`  |   122.122.122.122 
action_result.data.\*.Reservations.\*.Instances.\*.RootDeviceName | string |  |   /dev/xvda 
action_result.data.\*.Reservations.\*.Instances.\*.RootDeviceType | string |  |   ebs 
action_result.data.\*.Reservations.\*.Instances.\*.SecurityGroups.\*.GroupId | string |  `aws ec2 group id`  |   sg-07987bf5b796b5261 
action_result.data.\*.Reservations.\*.Instances.\*.SecurityGroups.\*.GroupName | string |  `aws ec2 group name`  |   Test-7-2-0-AutogenByAWSMP-4 
action_result.data.\*.Reservations.\*.Instances.\*.SourceDestCheck | boolean |  |   True  False 
action_result.data.\*.Reservations.\*.Instances.\*.State.Code | numeric |  |   16 
action_result.data.\*.Reservations.\*.Instances.\*.State.Name | string |  |   running 
action_result.data.\*.Reservations.\*.Instances.\*.StateReason.Code | string |  |  
action_result.data.\*.Reservations.\*.Instances.\*.StateReason.Message | string |  |  
action_result.data.\*.Reservations.\*.Instances.\*.StateTransitionReason | string |  |  
action_result.data.\*.Reservations.\*.Instances.\*.SubnetId | string |  `aws ec2 subnet id`  |   subnet-d8782cf7 
action_result.data.\*.Reservations.\*.Instances.\*.Tags.ASG | string |  |   ASG_value 
action_result.data.\*.Reservations.\*.Instances.\*.Tags.BMC | string |  |   TICKET-632 
action_result.data.\*.Reservations.\*.Instances.\*.Tags.JIRA | string |  |   TICKET-408 
action_result.data.\*.Reservations.\*.Instances.\*.Tags.Name | string |  |   proyer-xoltdjq-test-v45-backup 
action_result.data.\*.Reservations.\*.Instances.\*.Tags.Project | string |  |   TestProject 
action_result.data.\*.Reservations.\*.Instances.\*.Tags.aws:cloudformation:logical-id | string |  |   EDAInstance1100VTrace 
action_result.data.\*.Reservations.\*.Instances.\*.Tags.aws:cloudformation:stack-id | string |  |   arn:aws:cloudformation:us-east-1:157568067690:stack/test-extrahop-sensor/0e24e140-bfd5-11ec-a04d-0aac273a061b 
action_result.data.\*.Reservations.\*.Instances.\*.Tags.aws:cloudformation:stack-name | string |  |   test-extrahop-sensor 
action_result.data.\*.Reservations.\*.Instances.\*.Tags.proyer-lab | string |  |   xoltdjq 
action_result.data.\*.Reservations.\*.Instances.\*.Tags.proyer-schedule | string |  |   night-shutoff 
action_result.data.\*.Reservations.\*.Instances.\*.Tags.purpose | string |  |   apps-testing 
action_result.data.\*.Reservations.\*.Instances.\*.Tags.team | string |  |   test-plugin-team 
action_result.data.\*.Reservations.\*.Instances.\*.Tags.windows-hostname | string |  |   EC2AMAZ-4CQ1DK7 
action_result.data.\*.Reservations.\*.Instances.\*.VirtualizationType | string |  |   hvm 
action_result.data.\*.Reservations.\*.Instances.\*.VpcId | string |  `aws ec2 vpc id`  |   vpc-5113dc2a 
action_result.data.\*.Reservations.\*.OwnerId | string |  `aws ec2 owner id`  |   849257271967 
action_result.data.\*.Reservations.\*.RequesterId | string |  |   086189789714 
action_result.data.\*.Reservations.\*.ReservationId | string |  |   r-05ef1ae0985a72df5 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-length | string |  |   230 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-type | string |  |   text/xml;charset=UTF-8 
action_result.data.\*.ResponseMetadata.HTTPHeaders.date | string |  |   Wed, 27 Feb 2019 18:39:01 GMT 
action_result.data.\*.ResponseMetadata.HTTPHeaders.server | string |  |   AmazonEC2 
action_result.data.\*.ResponseMetadata.HTTPHeaders.transfer-encoding | string |  |   chunked 
action_result.data.\*.ResponseMetadata.HTTPHeaders.vary | string |  |   Accept-Encoding 
action_result.data.\*.ResponseMetadata.HTTPStatusCode | numeric |  |   200 
action_result.data.\*.ResponseMetadata.RequestId | string |  |   146815a0-5918-4305-8a77-540704c88939 
action_result.data.\*.ResponseMetadata.RetryAttempts | numeric |  |   0 
action_result.summary.num_instances | numeric |  |   3 
action_result.message | string |  |   Num instances: 3 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'create security group'
Creates a security group

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**group_name** |  required  | The name of the security group | string |  `aws ec2 group name` 
**group_description** |  required  | A description for the security group | string | 
**tag_specifications** |  optional  | The tags to assign to the security group | string | 
**vpc_id** |  optional  | The ID of the VPC | string |  `aws ec2 vpc id` 
**dry_run** |  optional  | Check if asset has required permissions for the action | boolean | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.credentials | string |  `aws credentials`  |   {'AccessKeyId': 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration': '2020-12-09 22:28:04', 'SecretAccessKey': 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken': 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ+yY5Qk2QpWctS2BGn4n+G8cD6zEweCCMj+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='} 
action_result.parameter.dry_run | boolean |  |   True  False 
action_result.parameter.group_description | string |  |   Test Group Description 
action_result.parameter.group_name | string |  `aws ec2 group name`  |   Test Group Name 
action_result.parameter.tag_specifications | string |  |   [{"ResourceType": "security-group","Tags": [{"Key": "test-key", "Value": "test-value"}]}] 
action_result.parameter.vpc_id | string |  `aws ec2 vpc id`  |   vpc-04a9ace96009f1141 
action_result.data.\*.GroupId | string |  `aws ec2 group id`  |   sg-082268bbc0b1c7a6a 
action_result.data.\*.ResponseMetadata.HTTPHeaders.cache-control | string |  |   no-cache, no-store 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-length | string |  |   283 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-type | string |  |   text/xml;charset=UTF-8 
action_result.data.\*.ResponseMetadata.HTTPHeaders.date | string |  |   Mon, 01 Aug 2022 06:13:25 GMT 
action_result.data.\*.ResponseMetadata.HTTPHeaders.server | string |  |   AmazonEC2 
action_result.data.\*.ResponseMetadata.HTTPHeaders.strict-transport-security | string |  |   max-age=31536000; includeSubDomains 
action_result.data.\*.ResponseMetadata.HTTPHeaders.x-amzn-requestid | string |  |   d103997b-3fc6-4cfa-a3bd-e3200005c1b9 
action_result.data.\*.ResponseMetadata.HTTPStatusCode | numeric |  |   200 
action_result.data.\*.ResponseMetadata.RequestId | string |  |   d103997b-3fc6-4cfa-a3bd-e3200005c1b9 
action_result.data.\*.ResponseMetadata.RetryAttempts | numeric |  |   0 
action_result.data.\*.Tags.\*.Key | string |  |   test-key 
action_result.data.\*.Tags.\*.Value | string |  |   test-value 
action_result.summary.group_id | string |  `aws ec2 group id`  |   sg-082268bbc0b1c7a6a 
action_result.message | string |  |   Group id: sg-082268bbc0b1c7a6a 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'delete security group'
Deletes a security group

Type: **generic**  
Read only: **False**

You can specify either the security group name or the security group ID. If both parameters are provided, the 'group id' will be considered.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**group_id** |  optional  | The ID of the security group | string |  `aws ec2 group id` 
**group_name** |  optional  | The name of the security group | string |  `aws ec2 group name` 
**dry_run** |  optional  | Check if asset has required permissions for the action | boolean | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.credentials | string |  `aws credentials`  |   {'AccessKeyId': 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration': '2020-12-09 22:28:04', 'SecretAccessKey': 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken': 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ+yY5Qk2QpWctS2BGn4n+G8cD6zEweCCMj+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='} 
action_result.parameter.dry_run | boolean |  |   True  False 
action_result.parameter.group_id | string |  `aws ec2 group id`  |   sg-00dae13e516e82136 
action_result.parameter.group_name | string |  `aws ec2 group name`  |   Test Group Name 
action_result.data.\*.ResponseMetadata.HTTPHeaders.cache-control | string |  |   no-cache, no-store 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-length | string |  |   239 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-type | string |  |   text/xml;charset=UTF-8 
action_result.data.\*.ResponseMetadata.HTTPHeaders.date | string |  |   Mon, 01 Aug 2022 06:06:41 GMT 
action_result.data.\*.ResponseMetadata.HTTPHeaders.server | string |  |   AmazonEC2 
action_result.data.\*.ResponseMetadata.HTTPHeaders.strict-transport-security | string |  |   max-age=31536000; includeSubDomains 
action_result.data.\*.ResponseMetadata.HTTPHeaders.x-amzn-requestid | string |  |   c5ada32e-8c4d-4f4a-b9aa-d53efd210aba 
action_result.data.\*.ResponseMetadata.HTTPStatusCode | numeric |  |   200 
action_result.data.\*.ResponseMetadata.RequestId | string |  |   c5ada32e-8c4d-4f4a-b9aa-d53efd210aba 
action_result.data.\*.ResponseMetadata.RetryAttempts | numeric |  |   0 
action_result.summary | string |  |  
action_result.message | string |  |   Successfully deleted the security group 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'describe snapshots'
Describe one or more snapshots

Type: **investigate**  
Read only: **True**

The snapshots available to you include public snapshots, private snapshots that you own, and private snapshots owned by other AWS accounts for which you have explicit create volume permissions.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**filters** |  optional  | One or more filters, separated by commas | string | 
**snapshot_ids** |  optional  | One or more snapshot IDs, separated by commas | string |  `aws ec2 snapshot id` 
**restorable_by** |  optional  | The IDs of the AWS accounts that can create volumes from the snapshot | string |  `aws ec2 owner id` 
**owners** |  optional  | Scopes the results to snapshots with the specified owners. You can specify a combination of AWS account IDs, self, and amazon | string |  `aws ec2 owner id` 
**limit** |  optional  | The maximum number of results to be fetched | numeric | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 
**dry_run** |  optional  | Check if asset has required permissions for the action | boolean | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.credentials | string |  `aws credentials`  |   {'AccessKeyId': 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration': '2020-12-09 22:28:04', 'SecretAccessKey': 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken': 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ+yY5Qk2QpWctS2BGn4n+G8cD6zEweCCMj+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='} 
action_result.parameter.dry_run | boolean |  |   True  False 
action_result.parameter.filters | string |  |   { 'Name': 'name_1', 'Values': [ 'val_1' ]} 
action_result.parameter.limit | numeric |  |   100 
action_result.parameter.owners | string |  `aws ec2 owner id`  |   575461648593 
action_result.parameter.restorable_by | string |  `aws ec2 owner id`  |   575461648593 
action_result.parameter.snapshot_ids | string |  `aws ec2 snapshot id`  |   snap-08391e1d0fe151035 
action_result.data.\*.Description | string |  |   snapshot of image.vmdk 
action_result.data.\*.Encrypted | boolean |  |   True  False 
action_result.data.\*.KmsKeyId | string |  `kms key id`  |   arn:aws:kms:us-east-1:157568067690:key/cabd6f9c-4bd4-4f88-80ef-5509e5d23551 
action_result.data.\*.OwnerAlias | string |  |   amazon 
action_result.data.\*.OwnerId | string |  `aws ec2 owner id`  |   099720109477 
action_result.data.\*.Progress | string |  |   100% 
action_result.data.\*.SnapshotId | string |  `aws ec2 snapshot id`  |   snap-08391e1d0fe151035 
action_result.data.\*.StartTime | string |  |   2017-02-08 12:14:09 
action_result.data.\*.State | string |  |   completed 
action_result.data.\*.StateMessage | string |  |   Source snapshot is not found 
action_result.data.\*.Tags.\*.Key | string |  |   proyer-lab 
action_result.data.\*.Tags.\*.Value | string |  |   xoltdjq 
action_result.data.\*.VolumeId | string |  |   vol-ffffffff 
action_result.data.\*.VolumeSize | numeric |  |   8 
action_result.summary.num_snapshots | numeric |  |   53805 
action_result.message | string |  |   Num snapshots: 53805 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'copy snapshot'
Copies a point-in-time snapshot of an EBS volume and stores it in Amazon S3

Type: **generic**  
Read only: **False**

For more information regarding the action parameters, please refer to <a href="https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CopySnapshot.html" target="_blank">Copy Snapshot API Documentation</a>.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**source_region** |  required  | The ID of the region that contains the snapshot to be copied | string | 
**source_snapshot_id** |  required  | The ID of the EBS snapshot to copy | string |  `aws ec2 snapshot id` 
**destination_region** |  optional  | The destination region to use in the 'presigned url' parameter of a snapshot copy operation | string | 
**kms_key_id** |  optional  | The identifier of the AWS Key Management Service (AWS KMS) KMS key to use for Amazon EBS encryption | string |  `kms key id` 
**presigned_url** |  optional  | When you copy an encrypted source snapshot using the Amazon EC2 Query API, you must supply a pre-signed URL | string | 
**encrypted** |  optional  | To encrypt a copy of an unencrypted snapshot if encryption by default is not enabled, enable encryption using this parameter | boolean | 
**description** |  optional  | A description for the EBS snapshot | string | 
**tag_specifications** |  optional  | The tags to apply to the snapshot during creation, separated by commas | string | 
**dry_run** |  optional  | Check if asset has required permissions for the action | boolean | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.credentials | string |  `aws credentials`  |   {'AccessKeyId': 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration': '2020-12-09 22:28:04', 'SecretAccessKey': 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken': 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ+yY5Qk2QpWctS2BGn4n+G8cD6zEweCCMj+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='} 
action_result.parameter.description | string |  |   [Copied snap-00f74e7eba4a187e from us-east-1] 
action_result.parameter.destination_region | string |  |   eu-central-1 
action_result.parameter.dry_run | boolean |  |   True  False 
action_result.parameter.encrypted | boolean |  |   True  False 
action_result.parameter.kms_key_id | string |  `kms key id`  |   cabd6f9c-4bd4-4f88-80ef-5509e5d23551 
action_result.parameter.presigned_url | string |  |   https://ec2.us-west-1.amazonaws.com/?Action=CopySnapshot&Version=2016-11-15&SourceRegion=us-east-1&DestinationRegion=us-west-1&SourceSnapshotId=snap-0b99123fc9e155567&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIASGL4J5BVFVKH54QI%2F20210804%2Fus-west-1%2Fec2%2Faws4_request&X-Amz-Date=20210804T104319Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=908638c4bbe2464ab4f01526cc0db19b2c17582171916aad42fa31f6bc69e86f 
action_result.parameter.source_region | string |  |   us-east-1 
action_result.parameter.source_snapshot_id | string |  `aws ec2 snapshot id`  |   snap-00f74e7e5ba4a187e 
action_result.parameter.tag_specifications | string |  |   [{"ResourceType": "security-group","Tags": [{"Key": "test-key", "Value": "test-value"}]}] 
action_result.data.\*.ResponseMetadata.HTTPHeaders.cache-control | string |  |   no-cache, no-store 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-length | string |  |   251 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-type | string |  |   text/xml;charset=UTF-8 
action_result.data.\*.ResponseMetadata.HTTPHeaders.date | string |  |   Thu, 28 Jul 2022 13:04:52 GMT 
action_result.data.\*.ResponseMetadata.HTTPHeaders.server | string |  |   AmazonEC2 
action_result.data.\*.ResponseMetadata.HTTPHeaders.strict-transport-security | string |  |   max-age=31536000; includeSubDomains 
action_result.data.\*.ResponseMetadata.HTTPHeaders.x-amzn-requestid | string |  |   ea754bd2-f8de-4460-a45b-972c6f6295e0 
action_result.data.\*.ResponseMetadata.HTTPStatusCode | numeric |  |   200 
action_result.data.\*.ResponseMetadata.RequestId | string |  |   ea754bd2-f8de-4460-a45b-972c6f6295e0 
action_result.data.\*.ResponseMetadata.RetryAttempts | numeric |  |   0 
action_result.data.\*.SnapshotId | string |  `aws ec2 snapshot id`  |   snap-061d898454a25d946 
action_result.data.\*.Tags.\*.Key | string |  |   test-key 
action_result.data.\*.Tags.\*.Value | string |  |   test-value 
action_result.summary.snapshot_id | string |  |   snap-061d898454a25d946 
action_result.message | string |  |   Snapshot id: snap-061d898454a25d946 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'describe vpcs'
Describe one or more vpcs

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**filters** |  optional  | One or more filters, separated by commas | string | 
**vpc_ids** |  optional  | One or more vpc IDs, separated by commas | string |  `aws ec2 vpc id` 
**limit** |  optional  | The maximum number of results to be fetched | numeric | 
**dry_run** |  optional  | Check if asset has required permissions for the action | boolean | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.credentials | string |  `aws credentials`  |   {'AccessKeyId': 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration': '2020-12-09 22:28:04', 'SecretAccessKey': 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken': 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ+yY5Qk2QpWctS2BGn4n+G8cD6zEweCCMj+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='} 
action_result.parameter.dry_run | boolean |  |   True  False 
action_result.parameter.filters | string |  |   { 'Name': 'name_1', 'Values': [ 'val_1' ]} 
action_result.parameter.limit | numeric |  |   100 
action_result.parameter.vpc_ids | string |  `aws ec2 vpc id`  |   vpc-0606b5757a86faaaa, vpc-1706b5757b86facaa 
action_result.data.\*.CidrBlock | string |  `aws cidr block`  |   172.31.0.0/16 
action_result.data.\*.CidrBlockAssociationSet.\*.AssociationId | string |  |   vpc-cidr-assoc-bb3fd4d3 
action_result.data.\*.CidrBlockAssociationSet.\*.CidrBlock | string |  |   172.31.0.0/16 
action_result.data.\*.CidrBlockAssociationSet.\*.CidrBlockState.State | string |  |   associated 
action_result.data.\*.DhcpOptionsId | string |  |   dopt-1be7197c 
action_result.data.\*.InstanceTenancy | string |  |   default 
action_result.data.\*.Ipv6CidrBlockAssociationSet.\*.AssociationId | string |  |   vpc-cidr-assoc-0f3eccfc9e5929eca 
action_result.data.\*.Ipv6CidrBlockAssociationSet.\*.Ipv6CidrBlock | string |  `aws cidr ipv6 block`  |   2600:1f18:e56:7e00::/56 
action_result.data.\*.Ipv6CidrBlockAssociationSet.\*.Ipv6CidrBlockState.State | string |  |   associated 
action_result.data.\*.Ipv6CidrBlockAssociationSet.\*.Ipv6Pool | string |  |   Amazon 
action_result.data.\*.Ipv6CidrBlockAssociationSet.\*.NetworkBorderGroup | string |  |   us-east-1 
action_result.data.\*.IsDefault | boolean |  |   True  False 
action_result.data.\*.OwnerId | string |  `aws ec2 owner id`  |   157568067690 
action_result.data.\*.State | string |  |   available 
action_result.data.\*.VpcId | string |  `aws ec2 vpc id`  |   vpc-b962a3df 
action_result.summary.num_vpcs | numeric |  |   4 
action_result.message | string |  |   Num vpc: 4 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'describe images'
Describe one or more images

Type: **investigate**  
Read only: **True**

The images available to you include public images, private images that you own, and private images owned by other AWS accounts for which you have explicit launch permissions.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**filters** |  optional  | One or more filters, separated by commas | string | 
**image_ids** |  optional  | One or more images IDs, separated by commas | string |  `aws ec2 image id` 
**executable_users** |  optional  | Scopes the images by users with explicit launch permissions | string | 
**owners** |  optional  | Scopes the results to images with the specified owners | string |  `aws ec2 owner id` 
**dry_run** |  optional  | Check if asset has required permissions for the action | boolean | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.credentials | string |  `aws credentials`  |   {'AccessKeyId': 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration': '2020-12-09 22:28:04', 'SecretAccessKey': 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken': 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ+yY5Qk2QpWctS2BGn4n+G8cD6zEweCCMj+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='} 
action_result.parameter.dry_run | boolean |  |   True  False 
action_result.parameter.executable_users | string |  |   self 
action_result.parameter.filters | string |  |   { 'Name': 'name_1', 'Values': [ 'val_1' ]} 
action_result.parameter.image_ids | string |  `aws ec2 image id`  |   aki-10f41769 
action_result.parameter.owners | string |  `aws ec2 owner id`  |   575461648593 
action_result.data.\*.Architecture | string |  |   i386 
action_result.data.\*.BlockDeviceMappings.\*.DeviceName | string |  |   /dev/xvda 
action_result.data.\*.BlockDeviceMappings.\*.Ebs.DeleteOnTermination | boolean |  |   True  False 
action_result.data.\*.BlockDeviceMappings.\*.Ebs.Encrypted | boolean |  |   True  False 
action_result.data.\*.BlockDeviceMappings.\*.Ebs.Iops | numeric |  |   200 
action_result.data.\*.BlockDeviceMappings.\*.Ebs.SnapshotId | string |  |   snap-080a0957ea8635473 
action_result.data.\*.BlockDeviceMappings.\*.Ebs.Throughput | numeric |  |   125 
action_result.data.\*.BlockDeviceMappings.\*.Ebs.VolumeSize | numeric |  |   8 
action_result.data.\*.BlockDeviceMappings.\*.Ebs.VolumeType | string |  |   gp2 
action_result.data.\*.BlockDeviceMappings.\*.VirtualName | string |  |   ephemeral0 
action_result.data.\*.CreationDate | string |  |   2019-04-11T12:30:47.000Z 
action_result.data.\*.Description | string |  |   shared-with-public-executable-by-description 
action_result.data.\*.EnaSupport | boolean |  |   True  False 
action_result.data.\*.Hypervisor | string |  |   xen 
action_result.data.\*.ImageId | string |  `aws ec2 image id`  |   aki-00896a69 
action_result.data.\*.ImageLocation | string |  |   karmic-kernel-zul/ubuntu-kernel-2.6.31-300-ec2-i386-20091002-test-04.manifest.xml 
action_result.data.\*.ImageOwnerAlias | string |  |   aws-marketplace 
action_result.data.\*.ImageType | string |  |   kernel 
action_result.data.\*.KernelId | string |  |   aki-8f9dcae6 
action_result.data.\*.Name | string |  |   shared-with-public-executable-by 
action_result.data.\*.OwnerId | string |  `aws ec2 owner id`  |   099720109477 
action_result.data.\*.Platform | string |  |   windows 
action_result.data.\*.PlatformDetails | string |  |   Linux/UNIX 
action_result.data.\*.ProductCodes.\*.ProductCodeId | string |  |   6njl1pau431dv1qxipg63mvah 
action_result.data.\*.ProductCodes.\*.ProductCodeType | string |  |   marketplace 
action_result.data.\*.Public | boolean |  |   True  False 
action_result.data.\*.RootDeviceName | string |  |   /dev/xvda 
action_result.data.\*.RootDeviceType | string |  |   instance-store 
action_result.data.\*.SriovNetSupport | string |  |   simple 
action_result.data.\*.State | string |  |   available 
action_result.data.\*.UsageOperation | string |  |   RunInstances 
action_result.data.\*.VirtualizationType | string |  |   paravirtual 
action_result.summary | string |  |  
action_result.summary.num_images | numeric |  |   6 
action_result.message | string |  |   Num images: 6 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'describe subnets'
Describe one or more subnets

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**filters** |  optional  | One or more filters, separated by commas | string | 
**subnet_ids** |  optional  | One or more subnet IDs, separated by commas | string |  `aws ec2 subnet id` 
**limit** |  optional  | The maximum number of results to be fetched | numeric | 
**dry_run** |  optional  | Check if asset has required permissions for the action | boolean | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.credentials | string |  `aws credentials`  |   {'AccessKeyId': 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration': '2020-12-09 22:28:04', 'SecretAccessKey': 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken': 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ+yY5Qk2QpWctS2BGn4n+G8cD6zEweCCMj+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='} 
action_result.parameter.dry_run | boolean |  |   True  False 
action_result.parameter.filters | string |  |   { 'Name': 'name_1', 'Values': [ 'val_1' ]} 
action_result.parameter.limit | numeric |  |   100 
action_result.parameter.subnet_ids | string |  `aws ec2 subnet id`  |   subnet-e541c2c8 
action_result.data.\*.AssignIpv6AddressOnCreation | boolean |  |   True  False 
action_result.data.\*.AvailabilityZone | string |  |   us-east-1a 
action_result.data.\*.AvailabilityZoneId | string |  |   use1-az2 
action_result.data.\*.AvailableIpAddressCount | numeric |  |   4073 
action_result.data.\*.CidrBlock | string |  `aws cidr block`  |   172.31.48.0/20 
action_result.data.\*.DefaultForAz | boolean |  |   True  False 
action_result.data.\*.MapCustomerOwnedIpOnLaunch | boolean |  |   True  False 
action_result.data.\*.MapPublicIpOnLaunch | boolean |  |   True  False 
action_result.data.\*.OwnerId | string |  `aws ec2 owner id`  |   157568067690 
action_result.data.\*.State | string |  |   available 
action_result.data.\*.SubnetArn | string |  |   arn:aws:ec2:us-east-1:157568067690:subnet/subnet-e541c2c8 
action_result.data.\*.SubnetId | string |  `aws ec2 subnet id`  |   subnet-e541c2c8 
action_result.data.\*.VpcId | string |  `aws ec2 vpc id`  |   vpc-b962a3df 
action_result.summary | string |  |  
action_result.summary.num_subnets | numeric |  |   6 
action_result.message | string |  |   Num subnets: 6 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'detach instance'
Detach an instance from an autoscaling group

Type: **contain**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**instance_ids** |  required  | Up to 20 IDs of the instances, separated by commas | string |  `aws ec2 instance id` 
**autoscaling_group_name** |  required  | The name of the autoscaling group | string |  `aws ec2 autoscaling group name` 
**should_decrement_desired_capacity** |  optional  | Decrement the desired capacity value by the number of instances being detached | boolean | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.autoscaling_group_name | string |  `aws ec2 autoscaling group name`  |   new-test-group1 
action_result.parameter.credentials | string |  `aws credentials`  |   {'AccessKeyId': 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration': '2020-12-09 22:28:04', 'SecretAccessKey': 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken': 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ+yY5Qk2QpWctS2BGn4n+G8cD6zEweCCMj+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='} 
action_result.parameter.instance_ids | string |  `aws ec2 instance id`  |   i-0fc20335d5bd6a222 
action_result.parameter.should_decrement_desired_capacity | boolean |  |   False  True 
action_result.data.\*.Activities.\*.ActivityId | string |  |   f4b5a82f-9649-3b08-ba77-8d7e25d70277 
action_result.data.\*.Activities.\*.AutoScalingGroupName | string |  `aws ec2 autoscaling group name`  |   new-test-group1 
action_result.data.\*.Activities.\*.Cause | string |  |   At 2019-04-11T10:15:55Z instance i-0fc20335d5bd6a222 was detached in response to a user request, shrinking the capacity from 7 to 6 
action_result.data.\*.Activities.\*.Description | string |  |   Detaching EC2 instance: i-0fc20335d5bd6a222 
action_result.data.\*.Activities.\*.Details | string |  |   {"Subnet ID":"subnet-160c5929","Availability Zone":"us-east-1e"} 
action_result.data.\*.Activities.\*.Progress | numeric |  |   50 
action_result.data.\*.Activities.\*.StartTime | string |  |   2019-04-11 10:15:55 
action_result.data.\*.Activities.\*.StatusCode | string |  |   InProgress 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-length | string |  |   974 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-type | string |  |   text/xml 
action_result.data.\*.ResponseMetadata.HTTPHeaders.date | string |  |   Thu, 11 Apr 2019 10:15:54 GMT 
action_result.data.\*.ResponseMetadata.HTTPHeaders.x-amzn-requestid | string |  |   cafdaca7-5c42-11e9-8ad4-a356e03ce0f0 
action_result.data.\*.ResponseMetadata.HTTPStatusCode | numeric |  |   200 
action_result.data.\*.ResponseMetadata.RequestId | string |  |   cafdaca7-5c42-11e9-8ad4-a356e03ce0f0 
action_result.data.\*.ResponseMetadata.RetryAttempts | numeric |  |   0 
action_result.summary.status | string |  |   Successfully detached instance 
action_result.message | string |  |   Status: Successfully detached instance 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'attach instance'
Attach an instance to an autoscaling group

Type: **correct**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**instance_ids** |  required  | Up to 20 IDs of the instances, separated by commas | string |  `aws ec2 instance id` 
**autoscaling_group_name** |  required  | The name of the autoscaling group | string |  `aws ec2 autoscaling group name` 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.autoscaling_group_name | string |  `aws ec2 autoscaling group name`  |   new-test-group1 
action_result.parameter.credentials | string |  `aws credentials`  |   {'AccessKeyId': 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration': '2020-12-09 22:28:04', 'SecretAccessKey': 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken': 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ+yY5Qk2QpWctS2BGn4n+G8cD6zEweCCMj+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='} 
action_result.parameter.instance_ids | string |  `aws ec2 instance id`  |   i-0fc20335d5bd6a222 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-length | string |  |   217 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-type | string |  |   text/xml 
action_result.data.\*.ResponseMetadata.HTTPHeaders.date | string |  |   Thu, 11 Apr 2019 10:15:08 GMT 
action_result.data.\*.ResponseMetadata.HTTPHeaders.x-amzn-requestid | string |  |   ae9444b2-5c42-11e9-99f6-eb3d1c5d5f57 
action_result.data.\*.ResponseMetadata.HTTPStatusCode | numeric |  |   200 
action_result.data.\*.ResponseMetadata.RequestId | string |  |   ae9444b2-5c42-11e9-99f6-eb3d1c5d5f57 
action_result.data.\*.ResponseMetadata.RetryAttempts | numeric |  |   0 
action_result.summary.status | string |  |   Successfully attached instance 
action_result.message | string |  |   Status: Successfully attached instance 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'delete vpc'
Delete a VPC

Type: **contain**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**vpc_id** |  required  | VPC id | string |  `aws ec2 vpc id` 
**dry_run** |  optional  | Check if asset has required permissions for the action | boolean | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.credentials | string |  `aws credentials`  |   {'AccessKeyId': 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration': '2020-12-09 22:28:04', 'SecretAccessKey': 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken': 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ+yY5Qk2QpWctS2BGn4n+G8cD6zEweCCMj+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='} 
action_result.parameter.dry_run | numeric |  |   False 
action_result.parameter.vpc_id | string |  `aws ec2 vpc id`  |   vpc-0606b5757a86faaaa 
action_result.data.\*.ResponseMetadata.HTTPHeaders.cache-control | string |  |   no-cache, no-store 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-length | string |  |   219 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-type | string |  |   text/xml;charset=UTF-8 
action_result.data.\*.ResponseMetadata.HTTPHeaders.date | string |  |   Thu, 11 Feb 2021 00:01:31 GMT 
action_result.data.\*.ResponseMetadata.HTTPHeaders.server | string |  |   AmazonEC2 
action_result.data.\*.ResponseMetadata.HTTPHeaders.strict-transport-security | string |  |   max-age=31536000; includeSubDomains 
action_result.data.\*.ResponseMetadata.HTTPHeaders.x-amzn-requestid | string |  |   b220b8a8-9763-4a2a-9811-be6393fede56 
action_result.data.\*.ResponseMetadata.HTTPStatusCode | numeric |  |   200 
action_result.data.\*.ResponseMetadata.RequestId | string |  |   b220b8a8-9763-4a2a-9811-be6393fede56 
action_result.data.\*.ResponseMetadata.RetryAttempts | numeric |  |   0 
action_result.summary.status | string |  |   Successfully deleted VPC 
action_result.message | string |  |   Status: Successfully deleted VPC 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'register instance'
Register an instance to a Classic AWS Elastic Load Balancer

Type: **contain**  
Read only: **False**

The load balancer provided in the 'load_balancer_name' parameter, has to be in the active state and of type classic.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**load_balancer_name** |  required  | Name of the classic load balancer | string | 
**instance_ids** |  required  | One or more instance IDs, separated by commas | string |  `aws ec2 instance id` 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.credentials | string |  `aws credentials`  |   {'AccessKeyId': 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration': '2020-12-09 22:28:04', 'SecretAccessKey': 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken': 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ+yY5Qk2QpWctS2BGn4n+G8cD6zEweCCMj+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='} 
action_result.parameter.instance_ids | string |  `aws ec2 instance id`  |   i-00617ee31402c4b46 
action_result.parameter.load_balancer_name | string |  |   testloadbalancer1 
action_result.data.\*.Instances.\*.InstanceId | string |  |   i-00617ee31402c4b46 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-length | string |  |   468 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-type | string |  |   text/xml 
action_result.data.\*.ResponseMetadata.HTTPHeaders.date | string |  |   Thu, 11 Feb 2021 00:17:18 GMT 
action_result.data.\*.ResponseMetadata.HTTPHeaders.x-amzn-requestid | string |  |   bdecdff6-ccfb-4c12-81a7-1d6c4dc99ead 
action_result.data.\*.ResponseMetadata.HTTPStatusCode | numeric |  |   200 
action_result.data.\*.ResponseMetadata.RequestId | string |  |   bdecdff6-ccfb-4c12-81a7-1d6c4dc99ead 
action_result.data.\*.ResponseMetadata.RetryAttempts | numeric |  |   0 
action_result.summary.status | string |  |   Successfully registered instance 
action_result.message | string |  |   Status: Successfully registered instance 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'deregister instance'
Deregister an instance from a Classic AWS Elastic Load Balancer

Type: **contain**  
Read only: **False**

The load balancer provided in the 'load_balancer_name' parameter, has to be in the active state and type classic.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**load_balancer_name** |  required  | Name of the classic load balancer | string | 
**instance_ids** |  required  | One or more instance IDs, separated by commas | string |  `aws ec2 instance id` 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.credentials | string |  `aws credentials`  |   {'AccessKeyId': 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration': '2020-12-09 22:28:04', 'SecretAccessKey': 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken': 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ+yY5Qk2QpWctS2BGn4n+G8cD6zEweCCMj+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='} 
action_result.parameter.instance_ids | string |  `aws ec2 instance id`  |   i-0d872de1de2ea7640 
action_result.parameter.load_balancer_name | string |  |   test-2 
action_result.data.\*.Instances.\*.InstanceId | string |  `aws ec2 instance id`  |   376 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-length | string |  |   376 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-type | string |  |   text/xml 
action_result.data.\*.ResponseMetadata.HTTPHeaders.date | string |  |   Mon, 15 Apr 2019 14:20:48 GMT 
action_result.data.\*.ResponseMetadata.HTTPHeaders.x-amzn-requestid | string |  |   aa6ed835-5f89-11e9-98f6-57e14b621ca5 
action_result.data.\*.ResponseMetadata.HTTPStatusCode | numeric |  |   200 
action_result.data.\*.ResponseMetadata.RequestId | string |  |   aa6ed835-5f89-11e9-98f6-57e14b621ca5 
action_result.data.\*.ResponseMetadata.RetryAttempts | numeric |  |   0 
action_result.summary.status | string |  |   Successfully deregistered instance 
action_result.message | string |  |   Status: Successfully deregistered instance 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'delete snapshot'
Delete snapshot of given AWS instance

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**snapshot_id** |  required  | Snapshot ID | string |  `aws ec2 snapshot id` 
**dry_run** |  optional  | Check if asset has required permissions for the action | boolean | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.credentials | string |  `aws credentials`  |   {'AccessKeyId': 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration': '2020-12-09 22:28:04', 'SecretAccessKey': 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken': 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ+yY5Qk2QpWctS2BGn4n+G8cD6zEweCCMj+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='} 
action_result.parameter.dry_run | numeric |  |   False 
action_result.parameter.snapshot_id | string |  `aws ec2 snapshot id`  |   snap-0157e1eeeee3112be 
action_result.data.\*.ResponseMetadata.HTTPHeaders.cache-control | string |  |   no-cache, no-store 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-length | string |  |   229 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-type | string |  |   text/xml;charset=UTF-8 
action_result.data.\*.ResponseMetadata.HTTPHeaders.date | string |  |   Thu, 11 Feb 2021 00:18:26 GMT 
action_result.data.\*.ResponseMetadata.HTTPHeaders.server | string |  |   AmazonEC2 
action_result.data.\*.ResponseMetadata.HTTPHeaders.strict-transport-security | string |  |   max-age=31536000; includeSubDomains 
action_result.data.\*.ResponseMetadata.HTTPHeaders.x-amzn-requestid | string |  |   cbdea730-5f77-4607-a030-4b94587283d8 
action_result.data.\*.ResponseMetadata.HTTPStatusCode | numeric |  |   200 
action_result.data.\*.ResponseMetadata.RequestId | string |  |   cbdea730-5f77-4607-a030-4b94587283d8 
action_result.data.\*.ResponseMetadata.RetryAttempts | numeric |  |   0 
action_result.summary.status | string |  |   Successfully deleted snapshot 
action_result.message | string |  |   Status: Successfully deleted snapshot 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'snapshot instance'
Snapshot AWS instance that has the given IP address or instance ID

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**volume_id** |  required  | The ID of the Elastic Block Store (EBS) volume | string | 
**description** |  optional  | A description of the snapshot | string | 
**tag_specifications** |  optional  | The tags to apply to the snapshot during creation, separated by commas | string | 
**dry_run** |  optional  | Check if asset has required permissions for the action | boolean | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.credentials | string |  `aws credentials`  |   {'AccessKeyId': 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration': '2020-12-09 22:28:04', 'SecretAccessKey': 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken': 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ+yY5Qk2QpWctS2BGn4n+G8cD6zEweCCMj+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='} 
action_result.parameter.description | string |  |   test 
action_result.parameter.dry_run | boolean |  |   False  True 
action_result.parameter.tag_specifications | string |  |   [{"ResourceType": "security-group","Tags": [{"Key": "test-key", "Value": "test-value"}]}] 
action_result.parameter.volume_id | string |  |   vol-0606e18158aac7321 
action_result.data.\*.Description | string |  |   test 
action_result.data.\*.Encrypted | boolean |  |   True  False 
action_result.data.\*.OwnerId | string |  `aws ec2 owner id`  |   849257271967 
action_result.data.\*.Progress | string |  |   89 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-length | string |  |   560 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-type | string |  |   text/xml;charset=UTF-8 
action_result.data.\*.ResponseMetadata.HTTPHeaders.date | string |  |   Wed, 10 Apr 2019 10:04:42 GMT 
action_result.data.\*.ResponseMetadata.HTTPHeaders.server | string |  |   AmazonEC2 
action_result.data.\*.ResponseMetadata.HTTPStatusCode | numeric |  |   200 
action_result.data.\*.ResponseMetadata.RequestId | string |  |   735ef5a4-1f16-4a56-8914-4fd5831278cb 
action_result.data.\*.ResponseMetadata.RetryAttempts | numeric |  |   0 
action_result.data.\*.SnapshotId | string |  |   snap-0267a8dc4d41113ef 
action_result.data.\*.StartTime | string |  |   2019-04-10 10:04:43 
action_result.data.\*.State | string |  |   pending 
action_result.data.\*.VolumeId | string |  |   vol-0606e18158aac7321 
action_result.data.\*.VolumeSize | numeric |  |   50 
action_result.summary.snapshot_id | numeric |  |   22 
action_result.message | string |  |   Snapshot id: 22 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'get tag'
Get the value of a tag for the given instance ID

Type: **investigate**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**instance_id** |  required  | Instance ID | string |  `aws ec2 instance id` 
**tag_key** |  required  | Tag key | string |  `aws ec2 tag key` 
**dry_run** |  optional  | Check if asset has required permissions for the action | boolean | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.credentials | string |  `aws credentials`  |   {'AccessKeyId': 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration': '2020-12-09 22:28:04', 'SecretAccessKey': 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken': 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ+yY5Qk2QpWctS2BGn4n+G8cD6zEweCCMj+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='} 
action_result.parameter.dry_run | boolean |  |   True  False 
action_result.parameter.instance_id | string |  `aws ec2 instance id`  |   i-059d3667cb8b94f39 
action_result.parameter.tag_key | string |  `aws ec2 tag key`  |   test 
action_result.data.\*.Key | string |  `aws ec2 tag key`  |   test 
action_result.data.\*.ResourceId | string |  `aws ec2 instance id`  |   i-059d3667cb8b94f39 
action_result.data.\*.ResourceType | string |  |   instance 
action_result.data.\*.Value | string |  `aws ec2 tag value`  |   value 
action_result.summary | string |  |  
action_result.message | string |  |   Successfully fetched the tag 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'add tag'
Add a tag to an instance

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**instance_id** |  required  | The ID of the instance | string |  `aws ec2 instance id` 
**tag_key** |  required  | Tag key | string |  `aws ec2 tag key` 
**tag_value** |  optional  | Tag value. Defaults to an empty string if left blank | string |  `aws ec2 tag value` 
**dry_run** |  optional  | Check if asset has required permissions for the action | boolean | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.credentials | string |  `aws credentials`  |   {'AccessKeyId': 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration': '2020-12-09 22:28:04', 'SecretAccessKey': 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken': 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ+yY5Qk2QpWctS2BGn4n+G8cD6zEweCCMj+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='} 
action_result.parameter.dry_run | boolean |  |   True  False 
action_result.parameter.instance_id | string |  `aws ec2 instance id`  |   i-074f52e85356829a3 
action_result.parameter.tag_key | string |  `aws ec2 tag key`  |   test1 
action_result.parameter.tag_value | string |  `aws ec2 tag value`  |   test 
action_result.data.\*.resource_id | string |  `aws ec2 resource id`  |   i-074f52e85356829a3 
action_result.summary.status | string |  |   Successfully added tag 
action_result.message | string |  |   Status: Successfully added tag 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'remove tag'
Remove specified tag from an instance

Type: **generic**  
Read only: **False**

If the user specifies a tag key without a tag value, it deletes any tag with this key regardless of its value. If the user specifies a tag key with an empty string as the tag value, it deletes the tag only if its value is an empty string. If the user omits this parameter, it deletes all user-defined tags for the specified resources. It does not delete AWS-generated tags (tags that have the AWS: prefix).

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**instance_id** |  required  | The ID of the instance | string |  `aws ec2 instance id` 
**tag_key** |  optional  | Tag key | string |  `aws ec2 tag key` 
**tag_value** |  optional  | Tag value. If not specified, all tags with tag_key will be removed. If empty string "" is specified, then tag_key with value of empty string will be removed | string |  `aws ec2 tag value` 
**dry_run** |  optional  | Check if asset has required permissions for the action | boolean | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.credentials | string |  `aws credentials`  |   {'AccessKeyId': 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration': '2020-12-09 22:28:04', 'SecretAccessKey': 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken': 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ+yY5Qk2QpWctS2BGn4n+G8cD6zEweCCMj+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='} 
action_result.parameter.dry_run | boolean |  |   True  False 
action_result.parameter.instance_id | string |  `aws ec2 instance id`  |   i-074f52e85356829a3 
action_result.parameter.tag_key | string |  `aws ec2 tag key`  |   test1 
action_result.parameter.tag_value | string |  `aws ec2 tag value`  |   test 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-length | string |  |   221 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-type | string |  |   text/xml;charset=UTF-8 
action_result.data.\*.ResponseMetadata.HTTPHeaders.date | string |  |   Tue, 26 Feb 2019 01:28:49 GMT 
action_result.data.\*.ResponseMetadata.HTTPHeaders.server | string |  |   AmazonEC2 
action_result.data.\*.ResponseMetadata.HTTPStatusCode | numeric |  |   200 
action_result.data.\*.ResponseMetadata.RequestId | string |  |   8d814715-abff-4816-829c-888344f8ccf5 
action_result.data.\*.ResponseMetadata.RetryAttempts | numeric |  |   0 
action_result.summary.status | string |  |   Successfully removed tag 
action_result.message | string |  |   Status: Successfully removed tag 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'get acls'
Get one or more network ACLs

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**filters** |  optional  | One or more filters in dictionary format, separated by commas | string | 
**dry_run** |  optional  | Check if asset has required permissions for the action | boolean | 
**network_acl_ids** |  optional  | One or more network ACL IDs, separated by commas | string | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.credentials | string |  `aws credentials`  |   {'AccessKeyId': 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration': '2020-12-09 22:28:04', 'SecretAccessKey': 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken': 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ+yY5Qk2QpWctS2BGn4n+G8cD6zEweCCMj+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='} 
action_result.parameter.dry_run | boolean |  |   True  False 
action_result.parameter.filters | string |  |   { 'Name': 'name_1', 'Values': [ 'val_1' ]} 
action_result.parameter.network_acl_ids | string |  |   acl-0729ksdnv768dda206 
action_result.data.\*.NetworkAcls.\*.Associations.\*.NetworkAclAssociationId | string |  |   aclassoc-dd6a3495 
action_result.data.\*.NetworkAcls.\*.Associations.\*.NetworkAclId | string |  |   acl-018ed07a 
action_result.data.\*.NetworkAcls.\*.Associations.\*.SubnetId | string |  `aws ec2 subnet id`  |   subnet-e3dcc0a8 
action_result.data.\*.NetworkAcls.\*.Entries.\*.CidrBlock | string |  |   0.0.0.0/0 
action_result.data.\*.NetworkAcls.\*.Entries.\*.Egress | boolean |  |   True  False 
action_result.data.\*.NetworkAcls.\*.Entries.\*.Ipv6CidrBlock | string |  |   ::/0 
action_result.data.\*.NetworkAcls.\*.Entries.\*.Protocol | string |  |   -1 
action_result.data.\*.NetworkAcls.\*.Entries.\*.RuleAction | string |  |   allow 
action_result.data.\*.NetworkAcls.\*.Entries.\*.RuleNumber | numeric |  |   100 
action_result.data.\*.NetworkAcls.\*.IsDefault | boolean |  |   True  False 
action_result.data.\*.NetworkAcls.\*.NetworkAclId | string |  `aws ec2 acl id`  |   acl-021d6e09826ed337c 
action_result.data.\*.NetworkAcls.\*.OwnerId | string |  `aws ec2 owner id`  |   849257271967 
action_result.data.\*.NetworkAcls.\*.Tags.\*.Key | string |  |   Name 
action_result.data.\*.NetworkAcls.\*.Tags.\*.Value | string |  |   Value 
action_result.data.\*.NetworkAcls.\*.VpcId | string |  `aws ec2 vpc id`  |   vpc-0ebb6161e92f4b472 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-length | string |  |   5632 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-type | string |  |   text/xml;charset=UTF-8 
action_result.data.\*.ResponseMetadata.HTTPHeaders.date | string |  |   Mon, 25 Feb 2019 20:55:14 GMT 
action_result.data.\*.ResponseMetadata.HTTPHeaders.server | string |  |   AmazonEC2 
action_result.data.\*.ResponseMetadata.HTTPHeaders.transfer-encoding | string |  |   chunked 
action_result.data.\*.ResponseMetadata.HTTPHeaders.vary | string |  |   Accept-Encoding 
action_result.data.\*.ResponseMetadata.HTTPStatusCode | numeric |  |   200 
action_result.data.\*.ResponseMetadata.RequestId | string |  |   f7e6f8a7-4968-4aff-9cb5-687b18d01335 
action_result.data.\*.ResponseMetadata.RetryAttempts | numeric |  |   0 
action_result.summary.num_acls | numeric |  |   3 
action_result.message | string |  |   Num acls: 3 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'add acl'
Add ACL to an instance

Type: **correct**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**vpc_id** |  required  | The ID of the virtual private cloud (VPC) | string |  `aws ec2 vpc id` 
**dry_run** |  optional  | Check if asset has required permissions for the action | boolean | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.credentials | string |  `aws credentials`  |   {'AccessKeyId': 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration': '2020-12-09 22:28:04', 'SecretAccessKey': 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken': 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ+yY5Qk2QpWctS2BGn4n+G8cD6zEweCCMj+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='} 
action_result.parameter.dry_run | boolean |  |   True  False 
action_result.parameter.vpc_id | string |  `aws ec2 vpc id`  |   vpc-0ebb6161e92f4b472 
action_result.data.\*.NetworkAcl.Entries.\*.CidrBlock | string |  |   0.0.0.0/0 
action_result.data.\*.NetworkAcl.Entries.\*.Egress | boolean |  |   True  False 
action_result.data.\*.NetworkAcl.Entries.\*.Ipv6CidrBlock | string |  |   ::/0 
action_result.data.\*.NetworkAcl.Entries.\*.Protocol | string |  |   -1 
action_result.data.\*.NetworkAcl.Entries.\*.RuleAction | string |  |   deny 
action_result.data.\*.NetworkAcl.Entries.\*.RuleNumber | numeric |  |   32767 
action_result.data.\*.NetworkAcl.IsDefault | boolean |  |   True  False 
action_result.data.\*.NetworkAcl.NetworkAclId | string |  `aws ec2 acl id`  |   acl-0e12cacd61c686be7 
action_result.data.\*.NetworkAcl.OwnerId | string |  `aws ec2 owner id`  |   849257271967 
action_result.data.\*.NetworkAcl.VpcId | string |  `aws ec2 vpc id`  |   vpc-0ebb6161e92f4b472 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-length | string |  |   1143 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-type | string |  |   text/xml;charset=UTF-8 
action_result.data.\*.ResponseMetadata.HTTPHeaders.date | string |  |   Mon, 25 Feb 2019 21:06:44 GMT 
action_result.data.\*.ResponseMetadata.HTTPHeaders.server | string |  |   AmazonEC2 
action_result.data.\*.ResponseMetadata.HTTPStatusCode | numeric |  |   200 
action_result.data.\*.ResponseMetadata.RequestId | string |  |   5fa65a92-5e47-4e08-873e-b4224e051da6 
action_result.data.\*.ResponseMetadata.RetryAttempts | numeric |  |   0 
action_result.summary.network_acl_id | string |  `aws ec2 acl id`  |   acl-0e12cacd61c686be7 
action_result.message | string |  |   Network acl id: acl-0e12cacd61c686be7 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'remove acl'
Remove ACL from an instance. The default network ACL and ACLs associated with any subnets cannot be deleted

Type: **contain**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**network_acl_id** |  required  | The ID of the network ACL | string |  `aws ec2 acl id` 
**dry_run** |  optional  | Check if asset has required permissions for the action | boolean | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.credentials | string |  `aws credentials`  |   {'AccessKeyId': 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration': '2020-12-09 22:28:04', 'SecretAccessKey': 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken': 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ+yY5Qk2QpWctS2BGn4n+G8cD6zEweCCMj+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='} 
action_result.parameter.dry_run | boolean |  |   True  False 
action_result.parameter.network_acl_id | string |  `aws ec2 acl id`  |   acl-0e12cacd61c686be7 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-length | string |  |   233 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-type | string |  |   text/xml;charset=UTF-8 
action_result.data.\*.ResponseMetadata.HTTPHeaders.date | string |  |   Tue, 26 Feb 2019 01:35:33 GMT 
action_result.data.\*.ResponseMetadata.HTTPHeaders.server | string |  |   AmazonEC2 
action_result.data.\*.ResponseMetadata.HTTPStatusCode | numeric |  |   200 
action_result.data.\*.ResponseMetadata.RequestId | string |  |   7c359e18-1df3-4e06-a812-c582da323550 
action_result.data.\*.ResponseMetadata.RetryAttempts | numeric |  |   0 
action_result.summary.status | string |  |   Successfully removed acl 
action_result.message | string |  |   Status: Successfully removed acl 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'list security groups'
Describe one or more security groups

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**filters** |  optional  | One or more filters in dictionary format, separated by commas | string | 
**dry_run** |  optional  | Check if asset has required permissions for the action | boolean | 
**group_ids** |  optional  | One or more security group IDs, separated by commas. Required for security groups in a non-default VPC | string |  `aws ec2 group id` 
**group_names** |  optional  | One or more security group names, separated by commas | string |  `aws ec2 group name` 
**next_token** |  optional  | The token to request the next page of results | string |  `aws ec2 next token` 
**max_results** |  optional  | Maximum number of results to return in a single call | numeric | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.credentials | string |  `aws credentials`  |   {'AccessKeyId': 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration': '2020-12-09 22:28:04', 'SecretAccessKey': 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken': 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ+yY5Qk2QpWctS2BGn4n+G8cD6zEweCCMj+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='} 
action_result.parameter.dry_run | boolean |  |   True  False 
action_result.parameter.filters | string |  |   { 'Name': 'name_1', 'Values': [ 'val_1' ]} 
action_result.parameter.group_ids | string |  `aws ec2 group id`  |   sg-005000000ea7b73e0 
action_result.parameter.group_names | string |  `aws ec2 group name`  |   Test Security Group 
action_result.parameter.max_results | numeric |  |   10 
action_result.parameter.next_token | string |  `aws ec2 next token`  |   eyJ2IjoiMiIsImMiOiJxTVBvSm9GZASDFGHJKLERTYU34GFG78SDFGHJR6SnN6VWNHcStSWGRwWTJ2cWtxZlBUWjY1QjJ3VzZRNlFqRkZaUzVrRDQ2V1lzTVpsY2dPSS9mVWNqVlVIbCtpaHV6b1dybnJWbXoxclp0T25YR3NvWVJRQkFuamhqaDlEN2o2dEtvcjB6bDBoeVo3clB2eGZOUlZxQUYzdWo5WnJKbTRRSmZqbHQzS0h1REhkWFI1Q1VmZnRLU2k2RkxhTkhaaUVkbXNPUlMwYnNYbkhVSHEwT0x1SmhEb2thTkc3R0tORkhaeWtIZCIsInMiOiIxIn0= 
action_result.data.\*.NextToken | string |  `aws ec2 next token`  |   eyJ2IjoiMiIsImMiOiJxTVBvSm9GZmpOVFhrc2RYL0RDK3htaytZR0luRDhuTWR6SnN6VWNHcStSWGRwWTJ2cWtxZlBUWjY1QjJ3VzZRNlFqRkZaUzVrRDQ2V1lzTVpsY2dPSS9mVWNqVlVIbCtpaHV6b1dybnJWbXoxclp0T25YR3NvWVJRQkFuamhqaDlEN2o2dEtvcjB6bDBoeVo3clB2eGZOUlZxQUYzdWo5WnJKbTRRSmZqbHQzS0h1REhkWFI1Q1VmZnRLU2k2RkxhTkhaaUVkbXNPUlMwYnNYbkhVSHEwT0x1SmhEb2thTkc3R0tORkhaeWtIZCIsInMiOiIxIn0= 
action_result.data.\*.ResponseMetadata.HTTPHeaders.cache-control | string |  |   no-cache, no-store 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-length | string |  |   '2719' 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-type | string |  |   text/xml;charset=UTF-8 
action_result.data.\*.ResponseMetadata.HTTPHeaders.date | string |  |   Tue, 09 Apr 2019 05:51:50 GMT 
action_result.data.\*.ResponseMetadata.HTTPHeaders.server | string |  |   AmazonEC2 
action_result.data.\*.ResponseMetadata.HTTPHeaders.strict-transport-security | string |  |   max-age=31536000; includeSubDomains 
action_result.data.\*.ResponseMetadata.HTTPHeaders.transfer-encoding | string |  |   chunked 
action_result.data.\*.ResponseMetadata.HTTPHeaders.vary | string |  |   accept-encoding 
action_result.data.\*.ResponseMetadata.HTTPHeaders.x-amzn-requestid | string |  |   deb7046d-4d6d-411b-89a7-dfeccf0713f3 
action_result.data.\*.ResponseMetadata.HTTPStatusCode | numeric |  |   200 
action_result.data.\*.ResponseMetadata.RequestId | string |  |   151cefc2-6f16-4949-b345-2ae3e2d6a02e 
action_result.data.\*.ResponseMetadata.RetryAttempts | numeric |  |   0 
action_result.data.\*.SecurityGroups.\*.Description | string |  |   SG for minemeld 
action_result.data.\*.SecurityGroups.\*.GroupId | string |  `aws ec2 group id`  |   sg-0050f8ec5ea7b73e0 
action_result.data.\*.SecurityGroups.\*.GroupName | string |  `aws ec2 group name`  |   minemeld-SGMinemeld-1PU2N2REVCWEB 
action_result.data.\*.SecurityGroups.\*.IpPermissions.\*.FromPort | numeric |  |   22 
action_result.data.\*.SecurityGroups.\*.IpPermissions.\*.IpProtocol | string |  |   tcp 
action_result.data.\*.SecurityGroups.\*.IpPermissions.\*.IpRanges.\*.CidrIp | string |  |   0.0.0.0/0 
action_result.data.\*.SecurityGroups.\*.IpPermissions.\*.IpRanges.\*.Description | string |  |   Test description 
action_result.data.\*.SecurityGroups.\*.IpPermissions.\*.Ipv6Ranges.\*.CidrIpv6 | string |  |   ::/0 
action_result.data.\*.SecurityGroups.\*.IpPermissions.\*.Ipv6Ranges.\*.Description | string |  |   Test description 
action_result.data.\*.SecurityGroups.\*.IpPermissions.\*.ToPort | numeric |  |   22 
action_result.data.\*.SecurityGroups.\*.IpPermissions.\*.UserIdGroupPairs.\*.Description | string |  |  
action_result.data.\*.SecurityGroups.\*.IpPermissions.\*.UserIdGroupPairs.\*.GroupId | string |  `aws ec2 group id`  |   sg-04c191ec3ad281c4d 
action_result.data.\*.SecurityGroups.\*.IpPermissions.\*.UserIdGroupPairs.\*.UserId | string |  |   849257271967 
action_result.data.\*.SecurityGroups.\*.IpPermissionsEgress.\*.IpProtocol | string |  |   -1 
action_result.data.\*.SecurityGroups.\*.IpPermissionsEgress.\*.IpRanges.\*.CidrIp | string |  |   0.0.0.0/0 
action_result.data.\*.SecurityGroups.\*.IpPermissionsEgress.\*.IpRanges.\*.Description | string |  |  
action_result.data.\*.SecurityGroups.\*.IpPermissionsEgress.\*.Ipv6Ranges.\*.CidrIpv6 | string |  |   ::/0 
action_result.data.\*.SecurityGroups.\*.IpPermissionsEgress.\*.UserIdGroupPairs.\*.GroupId | string |  `aws ec2 group id`  |   sg-0c95f4c3e04a5ed2f 
action_result.data.\*.SecurityGroups.\*.IpPermissionsEgress.\*.UserIdGroupPairs.\*.UserId | string |  |   849257271967 
action_result.data.\*.SecurityGroups.\*.OwnerId | string |  `aws ec2 owner id`  |   849257271967 
action_result.data.\*.SecurityGroups.\*.Tags.\*.Key | string |  |   aws:cloudformation:stack-id 
action_result.data.\*.SecurityGroups.\*.Tags.\*.Value | string |  |   arn:aws:cloudformation:us-east-1:849257271967:stack/minemeld/766407e0-3b8f-11e9-92b4-128fc503e968 
action_result.data.\*.SecurityGroups.\*.VpcId | string |  `aws ec2 vpc id`  |   vpc-5113dc2a 
action_result.summary.num_security_groups | numeric |  |   37 
action_result.message | string |  |   Num security groups: 37 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'assign instance'
Assign an instance to a security group

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**instance_id** |  required  | The ID of the instance | string |  `aws ec2 instance id` 
**group_id** |  required  | The security group ID to add | string |  `aws ec2 group id` 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.credentials | string |  `aws credentials`  |   {'AccessKeyId': 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration': '2020-12-09 22:28:04', 'SecretAccessKey': 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken': 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ+yY5Qk2QpWctS2BGn4n+G8cD6zEweCCMj+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='} 
action_result.parameter.group_id | string |  `aws ec2 group id`  |   sg-00c60fd41aea33c09 
action_result.parameter.instance_id | string |  `aws ec2 instance id`  |   i-074f52e85356829a3 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-length | string |  |   263 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-type | string |  |   text/xml;charset=UTF-8 
action_result.data.\*.ResponseMetadata.HTTPHeaders.date | string |  |   Tue, 26 Feb 2019 01:05:03 GMT 
action_result.data.\*.ResponseMetadata.HTTPHeaders.server | string |  |   AmazonEC2 
action_result.data.\*.ResponseMetadata.HTTPStatusCode | numeric |  |   200 
action_result.data.\*.ResponseMetadata.RequestId | string |  |   5b8d85e9-81c0-4e72-bd9e-90f598508ed1 
action_result.data.\*.ResponseMetadata.RetryAttempts | numeric |  |   0 
action_result.summary.status | string |  |   Successfully added instance to security group 
action_result.message | string |  |   Status: Successfully added instance to security group 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'remove instance'
Removes an instance from a security group

Type: **contain**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**instance_id** |  required  | The ID of the instance | string |  `aws ec2 instance id` 
**group_id** |  required  | The security group ID to remove | string |  `aws ec2 group id` 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.credentials | string |  `aws credentials`  |   {'AccessKeyId': 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration': '2020-12-09 22:28:04', 'SecretAccessKey': 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken': 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ+yY5Qk2QpWctS2BGn4n+G8cD6zEweCCMj+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='} 
action_result.parameter.group_id | string |  `aws ec2 group id`  |   sg-00c60fd41aea33c09 
action_result.parameter.instance_id | string |  `aws ec2 instance id`  |   i-074f52e85356829a3 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-length | string |  |   263 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-type | string |  |   text/xml;charset=UTF-8 
action_result.data.\*.ResponseMetadata.HTTPHeaders.date | string |  |   Tue, 26 Feb 2019 00:58:55 GMT 
action_result.data.\*.ResponseMetadata.HTTPHeaders.server | string |  |   AmazonEC2 
action_result.data.\*.ResponseMetadata.HTTPStatusCode | numeric |  |   200 
action_result.data.\*.ResponseMetadata.RequestId | string |  |   cd58da56-a011-4921-98aa-cc8dc333f284 
action_result.data.\*.ResponseMetadata.RetryAttempts | numeric |  |   0 
action_result.summary.status | string |  |   Successfully removed instance from security group 
action_result.message | string |  |   Status: Successfully removed instance from security group 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'create vpc'
Create a VPC with the specified IPv4 CIDR block

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**cidr_block** |  required  | The IPv4 network range for the VPC, in CIDR notation. For example: 10.0.0.0/16 | string |  `aws cidr block` 
**amazon_provided_ipv6_cidr_block** |  optional  | The Amazon provided IPv6 CIDR block with a /56 prefix length | boolean |  `aws cidr ipv6 block` 
**dry_run** |  optional  | Check if asset has required permissions for the action | boolean | 
**instance_tenancy** |  optional  | The tenancy options for instances launched into the VPC | string | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.amazon_provided_ipv6_cidr_block | boolean |  `aws cidr ipv6 block`  |   True  False 
action_result.parameter.cidr_block | string |  `aws cidr block`  |   172.31.0.0/16 
action_result.parameter.credentials | string |  `aws credentials`  |   {'AccessKeyId': 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration': '2020-12-09 22:28:04', 'SecretAccessKey': 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken': 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ+yY5Qk2QpWctS2BGn4n+G8cD6zEweCCMj+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='} 
action_result.parameter.dry_run | boolean |  |   True  False 
action_result.parameter.instance_tenancy | string |  |   Dedicated 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-length | string |  |   927 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-type | string |  |   text/xml;charset=UTF-8 
action_result.data.\*.ResponseMetadata.HTTPHeaders.date | string |  |   Tue, 26 Feb 2019 01:01:15 GMT 
action_result.data.\*.ResponseMetadata.HTTPHeaders.server | string |  |   AmazonEC2 
action_result.data.\*.ResponseMetadata.HTTPStatusCode | numeric |  |   200 
action_result.data.\*.ResponseMetadata.RequestId | string |  |   ddebfb7f-882d-4a04-bcbc-8c51d1e8b75d 
action_result.data.\*.ResponseMetadata.RetryAttempts | numeric |  |   0 
action_result.data.\*.Vpc.CidrBlock | string |  `aws cidr block`  |   172.31.0.0/16 
action_result.data.\*.Vpc.CidrBlockAssociationSet.\*.AssociationId | string |  |   vpc-cidr-assoc-0ebaa63a21400f523 
action_result.data.\*.Vpc.CidrBlockAssociationSet.\*.CidrBlock | string |  |   172.31.0.0/16 
action_result.data.\*.Vpc.CidrBlockAssociationSet.\*.CidrBlockState.State | string |  |   associated 
action_result.data.\*.Vpc.DhcpOptionsId | string |  |   dopt-d0d246a8 
action_result.data.\*.Vpc.InstanceTenancy | string |  |   default 
action_result.data.\*.Vpc.Ipv6CidrBlockAssociationSet.\*.AssociationId | string |  |   vpc-cidr-assoc-0c15e77e5475d004e 
action_result.data.\*.Vpc.Ipv6CidrBlockAssociationSet.\*.Ipv6CidrBlock | string |  |   2000:1000:2000:4000::/56 
action_result.data.\*.Vpc.Ipv6CidrBlockAssociationSet.\*.Ipv6CidrBlockState.State | string |  |   associating 
action_result.data.\*.Vpc.IsDefault | boolean |  |   True  False 
action_result.data.\*.Vpc.OwnerId | string |  `aws ec2 owner id`  |   849257271967 
action_result.data.\*.Vpc.State | string |  |   pending 
action_result.data.\*.Vpc.VpcId | string |  `aws ec2 vpc id`  |   vpc-0840e9850b3f02915 
action_result.summary.instance_tenancy | string |  |   default 
action_result.summary.vpc_id | string |  `aws ec2 vpc id`  |   vpc-0840e9850b3f02915 
action_result.message | string |  |   Instance tenancy: default, Vpc id: vpc-0840e9850b3f02915 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'list network interfaces'
Display network interfaces

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**filters** |  optional  | One or more filters in dictionary format, separated by commas | string | 
**dry_run** |  optional  | Check if asset has required permissions for the action | boolean | 
**network_interface_ids** |  optional  | One or more network interface IDs, separated by commas | string |  `aws ec2 network interface id` 
**next_token** |  optional  | The token to request the next page of results | string |  `aws ec2 next token` 
**max_results** |  optional  | Maximum number of results to return in a single call | numeric | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.credentials | string |  `aws credentials`  |   {'AccessKeyId': 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration': '2020-12-09 22:28:04', 'SecretAccessKey': 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken': 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ+yY5Qk2QpWctS2BGn4n+G8cD6zEweCCMj+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='} 
action_result.parameter.dry_run | boolean |  |   True  False 
action_result.parameter.filters | string |  |   { 'Name': 'name_1', 'Values': [ 'val_1' ]} 
action_result.parameter.max_results | numeric |  |   10 
action_result.parameter.network_interface_ids | string |  `aws ec2 network interface id`  |   eni-07fb411234dd33d65a 
action_result.parameter.next_token | string |  `aws ec2 next token`  |   eyJ2IjoiMiIsImMiOiJaaaaasdfghjkwertyuieeeeehjgvhjaytZR0luRDhuTWR6SnN6VWNHcStSWGRwWTJ2cWtxZlBUWjY1QjJ3VzZRNlFqRkZaUzVrRDQ2V1lzTVpsY2dPSS9mVWNqVlVIbCtpaHV6b1dybnJWbXoxclp0T25YR3NvWVJRQkFuamhqaDlEN2o2dEtvcjB6bDBoeVo3clB2eGZOUlZxQUYzdWo5WnJKbTRRSmZqbHQzS0h1REhkWFI1Q1VmZnRLU2k2RkxhTkhaaUVkbXNPUlMwYnNYbkhVSHEwT0x1SmhEb2thTkc3R0tORkhaeWtIZCIsInMiOiIxIn0= 
action_result.data.\*.NetworkInterfaces.\*.Association.AllocationId | string |  |   eipalloc-0e89c95ade8e8538f 
action_result.data.\*.NetworkInterfaces.\*.Association.AssociationId | string |  |   eipassoc-0b9359ed2e35464ff 
action_result.data.\*.NetworkInterfaces.\*.Association.IpOwnerId | string |  |   amazon 
action_result.data.\*.NetworkInterfaces.\*.Association.PublicDnsName | string |  |   ec2-122-122-122-122.compute-1.amazonaws.com 
action_result.data.\*.NetworkInterfaces.\*.Association.PublicIp | string |  `ip`  |   122.122.122.122 
action_result.data.\*.NetworkInterfaces.\*.Attachment.AttachTime | string |  |   2019-01-29 21:16:37 
action_result.data.\*.NetworkInterfaces.\*.Attachment.AttachmentId | string |  |   eni-attach-01e68402d9b5a989a 
action_result.data.\*.NetworkInterfaces.\*.Attachment.DeleteOnTermination | boolean |  |   True  False 
action_result.data.\*.NetworkInterfaces.\*.Attachment.DeviceIndex | numeric |  |   0 
action_result.data.\*.NetworkInterfaces.\*.Attachment.InstanceId | string |  |   i-09ddee967979f61dc 
action_result.data.\*.NetworkInterfaces.\*.Attachment.InstanceOwnerId | string |  |   849257271967 
action_result.data.\*.NetworkInterfaces.\*.Attachment.NetworkCardIndex | numeric |  |  
action_result.data.\*.NetworkInterfaces.\*.Attachment.Status | string |  |   attached 
action_result.data.\*.NetworkInterfaces.\*.AvailabilityZone | string |  |   us-east-1e 
action_result.data.\*.NetworkInterfaces.\*.Description | string |  |   ElastiCache test-clstr2-0003-001 
action_result.data.\*.NetworkInterfaces.\*.Groups.\*.GroupId | string |  `aws ec2 group id`  |   sg-00c60hquaea33c09 
action_result.data.\*.NetworkInterfaces.\*.Groups.\*.GroupName | string |  |   nginx-default-sg 
action_result.data.\*.NetworkInterfaces.\*.InterfaceType | string |  |   interface 
action_result.data.\*.NetworkInterfaces.\*.MacAddress | string |  |   06:2d:58:59:16:10 
action_result.data.\*.NetworkInterfaces.\*.NetworkInterfaceId | string |  `aws ec2 network interface id`  |   eni-024c6effa845834bb 
action_result.data.\*.NetworkInterfaces.\*.OwnerId | string |  `aws ec2 owner id`  |   849257271967 
action_result.data.\*.NetworkInterfaces.\*.PrivateDnsName | string |  |   ip-122-122-122-122.ec2.internal 
action_result.data.\*.NetworkInterfaces.\*.PrivateIpAddress | string |  `ip`  |   122.122.122.122 
action_result.data.\*.NetworkInterfaces.\*.PrivateIpAddresses.\*.Association.AllocationId | string |  |   eipalloc-0e89c95ade8e8538f 
action_result.data.\*.NetworkInterfaces.\*.PrivateIpAddresses.\*.Association.AssociationId | string |  |   eipassoc-0b9359ed2e35464ff 
action_result.data.\*.NetworkInterfaces.\*.PrivateIpAddresses.\*.Association.IpOwnerId | string |  |   amazon 
action_result.data.\*.NetworkInterfaces.\*.PrivateIpAddresses.\*.Association.PublicDnsName | string |  |   ec2-122-122-122-122.compute-1.amazonaws.com 
action_result.data.\*.NetworkInterfaces.\*.PrivateIpAddresses.\*.Association.PublicIp | string |  `ip`  |   122.122.122.122 
action_result.data.\*.NetworkInterfaces.\*.PrivateIpAddresses.\*.Primary | boolean |  |   True  False 
action_result.data.\*.NetworkInterfaces.\*.PrivateIpAddresses.\*.PrivateDnsName | string |  |   ip-122-122-122-122.ec2.internal 
action_result.data.\*.NetworkInterfaces.\*.PrivateIpAddresses.\*.PrivateIpAddress | string |  `ip`  |   122.122.122.122 
action_result.data.\*.NetworkInterfaces.\*.RequesterId | string |  |   803884302965 
action_result.data.\*.NetworkInterfaces.\*.RequesterManaged | boolean |  |   True  False 
action_result.data.\*.NetworkInterfaces.\*.SourceDestCheck | boolean |  |   True  False 
action_result.data.\*.NetworkInterfaces.\*.Status | string |  |   in-use 
action_result.data.\*.NetworkInterfaces.\*.SubnetId | string |  `aws ec2 subnet id`  |   subnet-160c5929 
action_result.data.\*.NetworkInterfaces.\*.TagSet.\*.Key | string |  |   TagName 
action_result.data.\*.NetworkInterfaces.\*.TagSet.\*.Value | string |  |   TagValue 
action_result.data.\*.NetworkInterfaces.\*.VpcId | string |  `aws ec2 vpc id`  |   vpc-5113dc2a 
action_result.data.\*.NextToken | string |  `aws ec2 next token`  |   eyJ2IjoiMiIsImMiOiJxTVBvSm9GZmpOVFhrc2RYL0RDasdfghjklasdfghjklVWNHcStSWGRwWTJ2cWtxZlBUWjY1QjJ3VzZRNlFqRkZaUzVrRDQ2V1lzTVpsY2dPSS9mVWNqVlVIbCtpaHV6b1dybnJWbXoxclp0T25YR3NvWVJRQkFuamhqaDlEN2o2dEtvcjB6bDBoeVo3clB2eGZOUlZxQUYzdWo5WnJKbTRRSmZqbHQzS0h1REhkWFI1Q1VmZnRLU2k2RkxhTkhaaUVkbXNPUlMwYnNYbkhVSHEwT0x1SmhEb2thTkc3R0tORkhaeWtIZCIsInMiOiIxIn0= 
action_result.data.\*.ResponseMetadata.HTTPHeaders.cache-control | string |  |   no-cache, no-store 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-length | string |  |   4508 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-type | string |  |   text/xml;charset=UTF-8 
action_result.data.\*.ResponseMetadata.HTTPHeaders.date | string |  |   Mon, 25 Feb 2019 22:45:38 GMT 
action_result.data.\*.ResponseMetadata.HTTPHeaders.server | string |  |   AmazonEC2 
action_result.data.\*.ResponseMetadata.HTTPHeaders.strict-transport-security | string |  |   max-age=31536000; includeSubDomains 
action_result.data.\*.ResponseMetadata.HTTPHeaders.transfer-encoding | string |  |   chunked 
action_result.data.\*.ResponseMetadata.HTTPHeaders.vary | string |  |   Accept-Encoding 
action_result.data.\*.ResponseMetadata.HTTPHeaders.x-amzn-requestid | string |  |   19523f47-f0be-4f9e-a05b-8917e7430937 
action_result.data.\*.ResponseMetadata.HTTPStatusCode | numeric |  |   200 
action_result.data.\*.ResponseMetadata.RequestId | string |  |   e24f0b23-e541-4d4a-8319-3418227f27d8 
action_result.data.\*.ResponseMetadata.RetryAttempts | numeric |  |   0 
action_result.summary.num_network_interfaces | numeric |  |   4 
action_result.message | string |  |   Num network interfaces: 4 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'list autoscaling groups'
Display autoscaling groups

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**autoscaling_group_names** |  optional  | The names of the Auto Scaling groups, separated by commas | string |  `aws ec2 autoscaling group name` 
**next_token** |  optional  | The token for the next set of items to return | string |  `aws ec2 next token` 
**max_results** |  optional  | Maximum number of results to return in a single call | numeric | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.autoscaling_group_names | string |  `aws ec2 autoscaling group name`  |   test ec2 group 
action_result.parameter.credentials | string |  `aws credentials`  |   {'AccessKeyId': 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration': '2020-12-09 22:28:04', 'SecretAccessKey': 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken': 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ+yY5Qk2QpWctS2BGn4n+G8cD6zEweCCMj+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='} 
action_result.parameter.max_results | numeric |  |   5 
action_result.parameter.next_token | string |  `aws ec2 next token`  |   eyJ2IjoiMiIsImMiOiJaaaaasdfghjkwertyuieeeeehjgvhjaytZR0luRDhuTWR6SnN6VWNHcStSWGRwWTJ2cWtxZlBUWjY1QjJ3VzZRNlFqRkZaUzVrRDQ2V1lzTVpsY2dPSS9mVWNqVlVIbCtpaHV6b1dybnJWbXoxclp0T25YR3NvWVJRQkFuamhqaDlEN2o2dEtvcjB6bDBoeVo3clB2eGZOUlZxQUYzdWo5WnJKbTRRSmZqbHQzS0h1REhkWFI1Q1VmZnRLU2k2RkxhTkhaaUVkbXNPUlMwYnNYbkhVSHEwT0x1SmhEb2thTkc3R0tORkhaeWtIZCIsInMiOiIxIn0= 
action_result.data.\*.AutoScalingGroups.\*.AutoScalingGroupARN | string |  |   arn:aws:autoscaling:us-east-1:849257271967:autoScalingGroup:19c78b3e-ed8a-40a5-a25e-03d628b45e8b:autoScalingGroupName/test ec2 group 
action_result.data.\*.AutoScalingGroups.\*.AutoScalingGroupName | string |  `aws ec2 autoscaling group name`  |   test ec2 group 
action_result.data.\*.AutoScalingGroups.\*.AvailabilityZones | string |  |   us-east-1f 
action_result.data.\*.AutoScalingGroups.\*.CapacityRebalance | boolean |  |   True  False 
action_result.data.\*.AutoScalingGroups.\*.CreatedTime | string |  |   2019-04-05 07:12:06 
action_result.data.\*.AutoScalingGroups.\*.DefaultCooldown | numeric |  |   300 
action_result.data.\*.AutoScalingGroups.\*.DesiredCapacity | numeric |  |   1 
action_result.data.\*.AutoScalingGroups.\*.HealthCheckGracePeriod | numeric |  |   300 
action_result.data.\*.AutoScalingGroups.\*.HealthCheckType | string |  |   EC2 
action_result.data.\*.AutoScalingGroups.\*.Instances.\*.AvailabilityZone | string |  |   us-east-1f 
action_result.data.\*.AutoScalingGroups.\*.Instances.\*.HealthStatus | string |  |   Healthy 
action_result.data.\*.AutoScalingGroups.\*.Instances.\*.InstanceId | string |  |   i-0533733e3fcb9b2b2 
action_result.data.\*.AutoScalingGroups.\*.Instances.\*.LaunchConfigurationName | string |  |   test ec2 
action_result.data.\*.AutoScalingGroups.\*.Instances.\*.LifecycleState | string |  |   InService 
action_result.data.\*.AutoScalingGroups.\*.Instances.\*.ProtectedFromScaleIn | boolean |  |   True  False 
action_result.data.\*.AutoScalingGroups.\*.LaunchConfigurationName | string |  |   test ec2 
action_result.data.\*.AutoScalingGroups.\*.MaxSize | numeric |  |   1 
action_result.data.\*.AutoScalingGroups.\*.MinSize | numeric |  |   1 
action_result.data.\*.AutoScalingGroups.\*.MixedInstancesPolicy.InstancesDistribution.OnDemandAllocationStrategy | string |  |   prioritized 
action_result.data.\*.AutoScalingGroups.\*.MixedInstancesPolicy.InstancesDistribution.OnDemandBaseCapacity | numeric |  |   0 
action_result.data.\*.AutoScalingGroups.\*.MixedInstancesPolicy.InstancesDistribution.OnDemandPercentageAboveBaseCapacity | numeric |  |   70 
action_result.data.\*.AutoScalingGroups.\*.MixedInstancesPolicy.InstancesDistribution.SpotAllocationStrategy | string |  |   capacity-optimized 
action_result.data.\*.AutoScalingGroups.\*.MixedInstancesPolicy.LaunchTemplate.LaunchTemplateSpecification.LaunchTemplateId | string |  |   lt-064a0gg751234654h 
action_result.data.\*.AutoScalingGroups.\*.MixedInstancesPolicy.LaunchTemplate.LaunchTemplateSpecification.LaunchTemplateName | string |  |   SOAR_Linux 
action_result.data.\*.AutoScalingGroups.\*.MixedInstancesPolicy.LaunchTemplate.LaunchTemplateSpecification.Version | string |  |   $Default 
action_result.data.\*.AutoScalingGroups.\*.MixedInstancesPolicy.LaunchTemplate.Overrides.\*.InstanceType | string |  |   a1.medium 
action_result.data.\*.AutoScalingGroups.\*.NewInstancesProtectedFromScaleIn | boolean |  |   True  False 
action_result.data.\*.AutoScalingGroups.\*.ServiceLinkedRoleARN | string |  |   arn:aws:iam::849257270067:role/aws-service-role/autoscaling.amazonaws.com/AWSServiceRoleForAutoScaling 
action_result.data.\*.AutoScalingGroups.\*.SuspendedProcesses.\*.ProcessName | string |  |   AlarmNotification 
action_result.data.\*.AutoScalingGroups.\*.SuspendedProcesses.\*.SuspensionReason | string |  |   User suspended at 2021-03-05T20:00:06Z 
action_result.data.\*.AutoScalingGroups.\*.Tags.\*.Key | string |  |   Environment 
action_result.data.\*.AutoScalingGroups.\*.Tags.\*.PropagateAtLaunch | boolean |  |   True  False 
action_result.data.\*.AutoScalingGroups.\*.Tags.\*.ResourceId | string |  |   test ec2 group 
action_result.data.\*.AutoScalingGroups.\*.Tags.\*.ResourceType | string |  |   auto-scaling-group 
action_result.data.\*.AutoScalingGroups.\*.Tags.\*.Value | string |  |   Production 
action_result.data.\*.AutoScalingGroups.\*.TerminationPolicies | string |  |   Default 
action_result.data.\*.AutoScalingGroups.\*.VPCZoneIdentifier | string |  |   subnet-3ee92331 
action_result.data.\*.NextToken | string |  `aws ec2 next token`  |   eyJ2IjoiMiIsImMiOiJxTVBvSm9GZmpOVFhrc2RYL0RDK3htaaaaaaaaaaaDhuTWR6SnN6VWNHcStSWGRwWTJ2cWtxZlBUWjY1QjJ3VzZRNlFqRkZaUzVrRDQ2V1lzTVpsY2dPSS9mVWNqVlVIbCtpaHV6b1dybnJWbXoxclp0T25YR3NvWVJRQkFuamhqaDlEN2o2dEtvcjB6bDBoeVo3clB2eGZOUlZxQUYzdWo5WnJKbTRRSmZqbHQzS0h1REhkWFI1Q1VmZnRLU2k2RkxhTkhaaUVkbXNPUlMwYnNYbkhVSHEwT0x1SmhEb2thTkc3R0tORkhaeWtIZCIsInMiOiIxIn0= 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-length | string |  |   2380 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-type | string |  |   text/xml 
action_result.data.\*.ResponseMetadata.HTTPHeaders.date | string |  |   Fri, 05 Apr 2019 07:18:01 GMT 
action_result.data.\*.ResponseMetadata.HTTPHeaders.vary | string |  |   Accept-Encoding 
action_result.data.\*.ResponseMetadata.HTTPHeaders.x-amzn-requestid | string |  |   f2cbc7b7-5772-11e9-9a12-85eb8661eb93 
action_result.data.\*.ResponseMetadata.HTTPStatusCode | numeric |  |   200 
action_result.data.\*.ResponseMetadata.RequestId | string |  |   f2cbc7b7-5772-11e9-9a12-85eb8661eb93 
action_result.data.\*.ResponseMetadata.RetryAttempts | numeric |  |   0 
action_result.summary.num_autoscaling_groups | numeric |  |   1 
action_result.message | string |  |   Num autoscaling groups: 1 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1 