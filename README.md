[comment]: # "Auto-generated SOAR connector documentation"
# AWS EC2

Publisher: Splunk  
Connector Version: 2\.3\.8  
Product Vendor: AWS  
Product Name: EC2  
Product Version Supported (regex): "\.\*"  
Minimum Product Version: 5\.0\.0  

This app integrates with AWS Elastic Compute Cloud \(EC2\) to perform virtualization actions

[comment]: # " File: readme.md"
[comment]: # "  Copyright (c) 2019-2021 Splunk Inc."
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
**access\_key** |  optional  | password | Access Key
**secret\_key** |  optional  | password | Secret Key
**region** |  required  | string | Default Region
**use\_role** |  optional  | boolean | Use attached role when running Phantom in EC2

### Supported Actions  
[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity using supplied configuration  
[start instance](#action-start-instance) - Start one or more instances  
[stop instance](#action-stop-instance) - Stop one or more instances  
[describe instance](#action-describe-instance) - Describe one or more instances  
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
[remove acl](#action-remove-acl) - Remove ACL from an instance\. The default network ACL and ACLs associated with any subnets cannot be deleted  
[list security groups](#action-list-security-groups) - Display security groups  
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
**instance\_ids** |  required  | One or more instance IDs, separated by commas | string |  `aws ec2 instance id` 
**dry\_run** |  optional  | Check if asset has required permissions for the action | boolean | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.dry\_run | boolean | 
action\_result\.parameter\.instance\_ids | string |  `aws ec2 instance id` 
action\_result\.parameter\.credentials | string |  `aws credentials` 
action\_result\.data\.\*\.CurrentState\.Code | numeric | 
action\_result\.data\.\*\.CurrentState\.Name | string | 
action\_result\.data\.\*\.InstanceId | string |  `aws ec2 instance id` 
action\_result\.data\.\*\.PreviousState\.Code | numeric | 
action\_result\.data\.\*\.PreviousState\.Name | string | 
action\_result\.summary | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'stop instance'
Stop one or more instances

Type: **generic**  
Read only: **False**

If the force parameter is enabled, the instances do not have an opportunity to flush file system caches or file system metadata\. If this option is enabled, you must perform file system check and repair procedures\. This option is not recommended for Windows instances\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**instance\_ids** |  required  | One or more instance IDs, separated by commas | string |  `aws ec2 instance id` 
**force** |  optional  | Forces the instances to stop | boolean | 
**dry\_run** |  optional  | Check if asset has required permissions for the action | boolean | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.dry\_run | boolean | 
action\_result\.parameter\.force | boolean | 
action\_result\.parameter\.instance\_ids | string |  `aws ec2 instance id` 
action\_result\.parameter\.credentials | string |  `aws credentials` 
action\_result\.data\.\*\.CurrentState\.Code | numeric | 
action\_result\.data\.\*\.CurrentState\.Name | string | 
action\_result\.data\.\*\.InstanceId | string |  `aws ec2 instance id` 
action\_result\.data\.\*\.PreviousState\.Code | numeric | 
action\_result\.data\.\*\.PreviousState\.Name | string | 
action\_result\.summary | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'describe instance'
Describe one or more instances

Type: **investigate**  
Read only: **True**

It is not suggested to use the limit parameter when instanceIDs parameter is used or instance\-id is used as filter criteria in the filters parameter\. But, if the limit parameter is used along with the above\-mentioned parameters, the number of instances fetched will be driven by the limit parameter value\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**filters** |  optional  | One or more filters, separated by commas\. Example\: \{ 'Name'\: 'name1', 'Values'\: \[ 'value1' \] \}, \{ 'Name'\: 'name2', 'Values'\: \[ 'value2' \] \} | string | 
**instance\_ids** |  optional  | One or more instance IDs, separated by commas | string |  `aws ec2 instance id` 
**limit** |  optional  | The maximum number of results to be fetched | numeric | 
**dry\_run** |  optional  | Check if asset has required permissions for the action | boolean | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.dry\_run | boolean | 
action\_result\.parameter\.filters | string | 
action\_result\.parameter\.instance\_ids | string |  `aws ec2 instance id` 
action\_result\.parameter\.limit | numeric | 
action\_result\.parameter\.credentials | string |  `aws credentials` 
action\_result\.data\.\*\.NextToken | string |  `aws ec2 next token` 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.AmiLaunchIndex | numeric | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.Architecture | string | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.BlockDeviceMappings\.\*\.DeviceName | string | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.BlockDeviceMappings\.\*\.Ebs\.AttachTime | string | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.BlockDeviceMappings\.\*\.Ebs\.DeleteOnTermination | boolean | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.BlockDeviceMappings\.\*\.Ebs\.Status | string | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.BlockDeviceMappings\.\*\.Ebs\.VolumeId | string | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.CapacityReservationSpecification\.CapacityReservationPreference | string | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.ClientToken | string | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.CpuOptions\.CoreCount | numeric | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.CpuOptions\.ThreadsPerCore | numeric | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.EbsOptimized | boolean | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.EnaSupport | boolean | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.HibernationOptions\.Configured | boolean | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.Hypervisor | string | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.IamInstanceProfile\.Arn | string | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.IamInstanceProfile\.Id | string | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.ImageId | string | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.InstanceId | string |  `aws ec2 instance id` 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.InstanceType | string | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.KeyName | string | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.LaunchTime | string | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.Monitoring\.State | string | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.NetworkInterfaces\.\*\.Association\.IpOwnerId | string | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.NetworkInterfaces\.\*\.Association\.PublicDnsName | string | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.NetworkInterfaces\.\*\.Association\.PublicIp | string |  `ip` 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.NetworkInterfaces\.\*\.Attachment\.AttachTime | string | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.NetworkInterfaces\.\*\.Attachment\.AttachmentId | string | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.NetworkInterfaces\.\*\.Attachment\.DeleteOnTermination | boolean | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.NetworkInterfaces\.\*\.Attachment\.DeviceIndex | numeric | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.NetworkInterfaces\.\*\.Attachment\.Status | string | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.NetworkInterfaces\.\*\.Description | string | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.NetworkInterfaces\.\*\.Groups\.\*\.GroupId | string | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.NetworkInterfaces\.\*\.Groups\.\*\.GroupName | string |  `url` 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.NetworkInterfaces\.\*\.MacAddress | string | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.NetworkInterfaces\.\*\.NetworkInterfaceId | string | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.NetworkInterfaces\.\*\.OwnerId | string | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.NetworkInterfaces\.\*\.PrivateDnsName | string | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.NetworkInterfaces\.\*\.PrivateIpAddress | string |  `ip` 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.NetworkInterfaces\.\*\.PrivateIpAddresses\.\*\.Association\.IpOwnerId | string | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.NetworkInterfaces\.\*\.PrivateIpAddresses\.\*\.Association\.PublicDnsName | string | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.NetworkInterfaces\.\*\.PrivateIpAddresses\.\*\.Association\.PublicIp | string |  `ip` 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.NetworkInterfaces\.\*\.PrivateIpAddresses\.\*\.Primary | boolean | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.NetworkInterfaces\.\*\.PrivateIpAddresses\.\*\.PrivateDnsName | string | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.NetworkInterfaces\.\*\.PrivateIpAddresses\.\*\.PrivateIpAddress | string |  `ip` 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.NetworkInterfaces\.\*\.SourceDestCheck | boolean | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.NetworkInterfaces\.\*\.Status | string | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.NetworkInterfaces\.\*\.SubnetId | string | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.NetworkInterfaces\.\*\.VpcId | string |  `aws ec2 vpc id` 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.Placement\.AvailabilityZone | string | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.Placement\.GroupName | string | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.Placement\.Tenancy | string | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.Platform | string | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.PrivateDnsName | string | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.PrivateIpAddress | string |  `ip` 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.ProductCodes\.\*\.ProductCodeId | string | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.ProductCodes\.\*\.ProductCodeType | string | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.PublicDnsName | string | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.PublicIpAddress | string |  `ip` 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.RootDeviceName | string | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.RootDeviceType | string | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.SecurityGroups\.\*\.GroupId | string | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.SecurityGroups\.\*\.GroupName | string |  `url` 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.SourceDestCheck | boolean | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.State\.Code | numeric | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.State\.Name | string | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.StateReason\.Code | string | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.StateReason\.Message | string | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.StateTransitionReason | string | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.SubnetId | string | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.VirtualizationType | string | 
action\_result\.data\.\*\.Reservations\.\*\.Instances\.\*\.VpcId | string |  `aws ec2 vpc id` 
action\_result\.data\.\*\.Reservations\.\*\.OwnerId | string | 
action\_result\.data\.\*\.Reservations\.\*\.RequesterId | string | 
action\_result\.data\.\*\.Reservations\.\*\.ReservationId | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-length | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-type | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.server | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.transfer\-encoding | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.vary | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.data\.\*\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.summary\.num\_instances | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'detach instance'
Detach an instance from an autoscaling group

Type: **contain**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**instance\_ids** |  required  | Up to 20 IDs of the instances, separated by commas | string |  `aws ec2 instance id` 
**autoscaling\_group\_name** |  required  | The name of the autoscaling group | string |  `aws ec2 autoscaling group name` 
**should\_decrement\_desired\_capacity** |  optional  | Decrement the desired capacity value by the number of instances being detached | boolean | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.autoscaling\_group\_name | string |  `aws ec2 autoscaling group name` 
action\_result\.parameter\.instance\_ids | string |  `aws ec2 instance id` 
action\_result\.parameter\.should\_decrement\_desired\_capacity | boolean | 
action\_result\.parameter\.credentials | string |  `aws credentials` 
action\_result\.data\.\*\.Activities\.\*\.ActivityId | string | 
action\_result\.data\.\*\.Activities\.\*\.AutoScalingGroupName | string | 
action\_result\.data\.\*\.Activities\.\*\.Cause | string | 
action\_result\.data\.\*\.Activities\.\*\.Description | string | 
action\_result\.data\.\*\.Activities\.\*\.Details | string | 
action\_result\.data\.\*\.Activities\.\*\.Progress | numeric | 
action\_result\.data\.\*\.Activities\.\*\.StartTime | string | 
action\_result\.data\.\*\.Activities\.\*\.StatusCode | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-length | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-type | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amzn\-requestid | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.data\.\*\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.summary\.status | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'attach instance'
Attach an instance to an autoscaling group

Type: **correct**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**instance\_ids** |  required  | Up to 20 IDs of the instances, separated by commas | string |  `aws ec2 instance id` 
**autoscaling\_group\_name** |  required  | The name of the autoscaling group | string |  `aws ec2 autoscaling group name` 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.autoscaling\_group\_name | string |  `aws ec2 autoscaling group name` 
action\_result\.parameter\.instance\_ids | string |  `aws ec2 instance id` 
action\_result\.parameter\.credentials | string |  `aws credentials` 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-length | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-type | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amzn\-requestid | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.data\.\*\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.summary\.status | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'delete vpc'
Delete a VPC

Type: **contain**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**vpc\_id** |  required  | VPC id | string |  `aws ec2 vpc id` 
**dry\_run** |  optional  | Check if asset has required permissions for the action | boolean | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.data\.\*\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.server | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-type | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.cache\-control | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-length | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amzn\-requestid | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.strict\-transport\-security | string | 
action\_result\.data\.\*\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.parameter\.vpc\_id | string |  `aws ec2 vpc id` 
action\_result\.parameter\.dry\_run | numeric | 
action\_result\.parameter\.credentials | string |  `aws credentials` 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 
action\_result\.summary\.status | string |   

## action: 'register instance'
Register an instance to a Classic AWS Elastic Load Balancer

Type: **contain**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**load\_balancer\_name** |  required  | Name of the classic load balancer | string | 
**instance\_ids** |  required  | One or more instance IDs, separated by commas | string |  `aws ec2 instance id` 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.data\.\*\.Instances\.\*\.InstanceId | string | 
action\_result\.data\.\*\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-type | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-length | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amzn\-requestid | string | 
action\_result\.data\.\*\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary\.status | string | 
action\_result\.parameter\.instance\_ids | string |  `aws ec2 instance id` 
action\_result\.parameter\.load\_balancer\_name | string | 
action\_result\.parameter\.credentials | string |  `aws credentials` 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'deregister instance'
Deregister an instance from a Classic AWS Elastic Load Balancer

Type: **contain**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**load\_balancer\_name** |  required  | Name of the classic load balancer | string | 
**instance\_ids** |  required  | One or more instance IDs, separated by commas | string |  `aws ec2 instance id` 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.instance\_ids | string |  `aws ec2 instance id` 
action\_result\.parameter\.load\_balancer\_name | string | 
action\_result\.parameter\.credentials | string |  `aws credentials` 
action\_result\.data\.\*\.Instances\.\*\.InstanceId | string |  `aws ec2 instance id` 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-length | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-type | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amzn\-requestid | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.data\.\*\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.summary\.status | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'delete snapshot'
Delete snapshot of given AWS instance

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**snapshot\_id** |  required  | Snapshot ID | string |  `aws ec2 snapshot id` 
**dry\_run** |  optional  | Check if asset has required permissions for the action | boolean | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.data\.\*\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.server | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-type | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.cache\-control | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-length | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amzn\-requestid | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.strict\-transport\-security | string | 
action\_result\.data\.\*\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.parameter\.snapshot\_id | string |  `aws ec2 snapshot id` 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.parameter\.dry\_run | numeric | 
action\_result\.parameter\.credentials | string |  `aws credentials` 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 
action\_result\.summary\.status | string |   

## action: 'snapshot instance'
Snapshot AWS instance that has the given IP address or instance ID

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**volume\_id** |  required  | The ID of the Elastic Block Store \(EBS\) volume | string | 
**description** |  optional  | A description of the snapshot | string | 
**tag\_specifications** |  required  | The tags to apply to the snapshot during creation, separated by commas\. Example\: \{ 'Name'\: 'name1', 'Values'\: \[ 'value1' \] \}, \{ 'Name'\: 'name2', 'Values'\: \[ 'value2' \] \} | string | 
**dry\_run** |  optional  | Check if asset has required permissions for the action | boolean | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.description | string | 
action\_result\.parameter\.dry\_run | boolean | 
action\_result\.parameter\.tag\_specifications | string | 
action\_result\.parameter\.volume\_id | string | 
action\_result\.parameter\.credentials | string |  `aws credentials` 
action\_result\.data\.\*\.Description | string | 
action\_result\.data\.\*\.Encrypted | boolean | 
action\_result\.data\.\*\.OwnerId | string | 
action\_result\.data\.\*\.Progress | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-length | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-type | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.server | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.data\.\*\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.data\.\*\.SnapshotId | string | 
action\_result\.data\.\*\.StartTime | string | 
action\_result\.data\.\*\.State | string | 
action\_result\.data\.\*\.VolumeId | string | 
action\_result\.data\.\*\.VolumeSize | numeric | 
action\_result\.summary\.snapshot\_id | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'get tag'
Get the value of a tag for the given instance ID

Type: **investigate**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**instance\_id** |  required  | Instance ID | string |  `aws ec2 instance id` 
**tag\_key** |  required  | Tag key | string |  `aws ec2 tag key` 
**dry\_run** |  optional  | Check if asset has required permissions for the action | boolean | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.dry\_run | boolean | 
action\_result\.parameter\.instance\_id | string |  `aws ec2 instance id` 
action\_result\.parameter\.tag\_key | string |  `aws ec2 tag key` 
action\_result\.parameter\.credentials | string |  `aws credentials` 
action\_result\.data\.\*\.Key | string |  `aws ec2 tag key` 
action\_result\.data\.\*\.ResourceId | string |  `aws ec2 instance id` 
action\_result\.data\.\*\.ResourceType | string | 
action\_result\.data\.\*\.Value | string |  `aws ec2 tag value` 
action\_result\.summary | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'add tag'
Add a tag to an instance

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**instance\_id** |  required  | The ID of the instance | string |  `aws ec2 instance id` 
**tag\_key** |  required  | Tag key | string |  `aws ec2 tag key` 
**tag\_value** |  optional  | Tag value\. Defaults to an empty string if left blank | string |  `aws ec2 tag value` 
**dry\_run** |  optional  | Check if asset has required permissions for the action | boolean | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.dry\_run | boolean | 
action\_result\.parameter\.instance\_id | string |  `aws ec2 instance id` 
action\_result\.parameter\.tag\_key | string |  `aws ec2 tag key` 
action\_result\.parameter\.tag\_value | string |  `aws ec2 tag value` 
action\_result\.parameter\.credentials | string |  `aws credentials` 
action\_result\.data\.\*\.resource\_id | string |  `aws ec2 resource id` 
action\_result\.summary\.status | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'remove tag'
Remove specified tag from an instance

Type: **generic**  
Read only: **False**

If the user specifies a tag key without a tag value, it deletes any tag with this key regardless of its value\. If the user specifies a tag key with an empty string as the tag value, it deletes the tag only if its value is an empty string\. If the user omits this parameter, it deletes all user\-defined tags for the specified resources\. It does not delete AWS\-generated tags \(tags that have the AWS\: prefix\)\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**instance\_id** |  required  | The ID of the instance | string |  `aws ec2 instance id` 
**tag\_key** |  optional  | Tag key | string |  `aws ec2 tag key` 
**tag\_value** |  optional  | Tag value\. If not specified, all tags with tag\_key will be removed\. If empty string "" is specified, then tag\_key with value of empty string will be removed | string |  `aws ec2 tag value` 
**dry\_run** |  optional  | Check if asset has required permissions for the action | boolean | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.dry\_run | boolean | 
action\_result\.parameter\.instance\_id | string |  `aws ec2 instance id` 
action\_result\.parameter\.tag\_key | string |  `aws ec2 tag key` 
action\_result\.parameter\.tag\_value | string |  `aws ec2 tag value` 
action\_result\.parameter\.credentials | string |  `aws credentials` 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-length | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-type | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.server | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.data\.\*\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.summary\.status | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'get acls'
Get one or more network ACLs

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**filters** |  optional  | One or more filters in dictionary format, separated by commas\. Example\: \{ 'Name'\: 'string', 'Values'\: \[ 'string' \]\} | string | 
**dry\_run** |  optional  | Check if asset has required permissions for the action | boolean | 
**network\_acl\_ids** |  optional  | One or more network ACL IDs, separated by commas | string | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.dry\_run | boolean | 
action\_result\.parameter\.filters | string | 
action\_result\.parameter\.network\_acl\_ids | string | 
action\_result\.parameter\.credentials | string |  `aws credentials` 
action\_result\.data\.\*\.NetworkAcls\.\*\.Associations\.\*\.NetworkAclAssociationId | string | 
action\_result\.data\.\*\.NetworkAcls\.\*\.Associations\.\*\.NetworkAclId | string | 
action\_result\.data\.\*\.NetworkAcls\.\*\.Associations\.\*\.SubnetId | string | 
action\_result\.data\.\*\.NetworkAcls\.\*\.Entries\.\*\.CidrBlock | string | 
action\_result\.data\.\*\.NetworkAcls\.\*\.Entries\.\*\.Egress | boolean | 
action\_result\.data\.\*\.NetworkAcls\.\*\.Entries\.\*\.Ipv6CidrBlock | string | 
action\_result\.data\.\*\.NetworkAcls\.\*\.Entries\.\*\.Protocol | string | 
action\_result\.data\.\*\.NetworkAcls\.\*\.Entries\.\*\.RuleAction | string | 
action\_result\.data\.\*\.NetworkAcls\.\*\.Entries\.\*\.RuleNumber | numeric | 
action\_result\.data\.\*\.NetworkAcls\.\*\.IsDefault | boolean | 
action\_result\.data\.\*\.NetworkAcls\.\*\.NetworkAclId | string |  `aws ec2 acl id` 
action\_result\.data\.\*\.NetworkAcls\.\*\.OwnerId | string | 
action\_result\.data\.\*\.NetworkAcls\.\*\.Tags\.\*\.Key | string | 
action\_result\.data\.\*\.NetworkAcls\.\*\.Tags\.\*\.Value | string | 
action\_result\.data\.\*\.NetworkAcls\.\*\.VpcId | string |  `aws ec2 vpc id` 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-length | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-type | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.server | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.transfer\-encoding | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.vary | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.data\.\*\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.summary\.num\_acls | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'add acl'
Add ACL to an instance

Type: **correct**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**vpc\_id** |  required  | The ID of the virtual private cloud \(VPC\) | string |  `aws ec2 vpc id` 
**dry\_run** |  optional  | Check if asset has required permissions for the action | boolean | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.dry\_run | boolean | 
action\_result\.parameter\.vpc\_id | string |  `aws ec2 vpc id` 
action\_result\.parameter\.credentials | string |  `aws credentials` 
action\_result\.data\.\*\.NetworkAcl\.Entries\.\*\.CidrBlock | string | 
action\_result\.data\.\*\.NetworkAcl\.Entries\.\*\.Egress | boolean | 
action\_result\.data\.\*\.NetworkAcl\.Entries\.\*\.Ipv6CidrBlock | string | 
action\_result\.data\.\*\.NetworkAcl\.Entries\.\*\.Protocol | string | 
action\_result\.data\.\*\.NetworkAcl\.Entries\.\*\.RuleAction | string | 
action\_result\.data\.\*\.NetworkAcl\.Entries\.\*\.RuleNumber | numeric | 
action\_result\.data\.\*\.NetworkAcl\.IsDefault | boolean | 
action\_result\.data\.\*\.NetworkAcl\.NetworkAclId | string |  `aws ec2 acl id` 
action\_result\.data\.\*\.NetworkAcl\.OwnerId | string | 
action\_result\.data\.\*\.NetworkAcl\.VpcId | string |  `aws ec2 vpc id` 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-length | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-type | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.server | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.data\.\*\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.summary\.network\_acl\_id | string |  `aws ec2 acl id` 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'remove acl'
Remove ACL from an instance\. The default network ACL and ACLs associated with any subnets cannot be deleted

Type: **contain**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**network\_acl\_id** |  required  | The ID of the network ACL | string |  `aws ec2 acl id` 
**dry\_run** |  optional  | Check if asset has required permissions for the action | boolean | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.dry\_run | boolean | 
action\_result\.parameter\.network\_acl\_id | string |  `aws ec2 acl id` 
action\_result\.parameter\.credentials | string |  `aws credentials` 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-length | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-type | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.server | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.data\.\*\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.summary\.status | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'list security groups'
Display security groups

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**filters** |  optional  | One or more filters in dictionary format, separated by commas\. Example\: \{ 'Name'\: 'string', 'Values'\: \[ 'string' \]\} | string | 
**dry\_run** |  optional  | Check if asset has required permissions for the action | boolean | 
**group\_ids** |  optional  | One or more security group IDs, separated by commas\. Required for security groups in a non\-default VPC | string |  `aws ec2 group id` 
**group\_names** |  optional  | One or more security group names, separated by commas | string |  `aws ec2 group name` 
**next\_token** |  optional  | The token to request the next page of results | string |  `aws ec2 next token` 
**max\_results** |  optional  | Maximum number of results to return in a single call | numeric | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.dry\_run | boolean | 
action\_result\.parameter\.filters | string | 
action\_result\.parameter\.group\_ids | string |  `aws ec2 group id` 
action\_result\.parameter\.group\_names | string |  `aws ec2 group name` 
action\_result\.parameter\.max\_results | numeric | 
action\_result\.parameter\.next\_token | string |  `aws ec2 next token` 
action\_result\.parameter\.credentials | string |  `aws credentials` 
action\_result\.data\.\*\.NextToken | string |  `aws ec2 next token` 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-length | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-type | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.server | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.transfer\-encoding | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.vary | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.data\.\*\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.data\.\*\.SecurityGroups\.\*\.Description | string | 
action\_result\.data\.\*\.SecurityGroups\.\*\.GroupId | string |  `aws ec2 group id` 
action\_result\.data\.\*\.SecurityGroups\.\*\.GroupName | string |  `url` 
action\_result\.data\.\*\.SecurityGroups\.\*\.IpPermissions\.\*\.FromPort | numeric | 
action\_result\.data\.\*\.SecurityGroups\.\*\.IpPermissions\.\*\.IpProtocol | string | 
action\_result\.data\.\*\.SecurityGroups\.\*\.IpPermissions\.\*\.IpRanges\.\*\.CidrIp | string | 
action\_result\.data\.\*\.SecurityGroups\.\*\.IpPermissions\.\*\.IpRanges\.\*\.Description | string | 
action\_result\.data\.\*\.SecurityGroups\.\*\.IpPermissions\.\*\.Ipv6Ranges\.\*\.CidrIpv6 | string | 
action\_result\.data\.\*\.SecurityGroups\.\*\.IpPermissions\.\*\.Ipv6Ranges\.\*\.Description | string | 
action\_result\.data\.\*\.SecurityGroups\.\*\.IpPermissions\.\*\.ToPort | numeric | 
action\_result\.data\.\*\.SecurityGroups\.\*\.IpPermissions\.\*\.UserIdGroupPairs\.\*\.Description | string | 
action\_result\.data\.\*\.SecurityGroups\.\*\.IpPermissions\.\*\.UserIdGroupPairs\.\*\.GroupId | string | 
action\_result\.data\.\*\.SecurityGroups\.\*\.IpPermissions\.\*\.UserIdGroupPairs\.\*\.UserId | string | 
action\_result\.data\.\*\.SecurityGroups\.\*\.IpPermissionsEgress\.\*\.IpProtocol | string | 
action\_result\.data\.\*\.SecurityGroups\.\*\.IpPermissionsEgress\.\*\.IpRanges\.\*\.CidrIp | string | 
action\_result\.data\.\*\.SecurityGroups\.\*\.IpPermissionsEgress\.\*\.IpRanges\.\*\.Description | string | 
action\_result\.data\.\*\.SecurityGroups\.\*\.IpPermissionsEgress\.\*\.Ipv6Ranges\.\*\.CidrIpv6 | string | 
action\_result\.data\.\*\.SecurityGroups\.\*\.IpPermissionsEgress\.\*\.UserIdGroupPairs\.\*\.GroupId | string | 
action\_result\.data\.\*\.SecurityGroups\.\*\.IpPermissionsEgress\.\*\.UserIdGroupPairs\.\*\.UserId | string | 
action\_result\.data\.\*\.SecurityGroups\.\*\.OwnerId | string | 
action\_result\.data\.\*\.SecurityGroups\.\*\.Tags\.\*\.Key | string | 
action\_result\.data\.\*\.SecurityGroups\.\*\.Tags\.\*\.Value | string | 
action\_result\.data\.\*\.SecurityGroups\.\*\.VpcId | string |  `aws ec2 vpc id` 
action\_result\.summary\.num\_security\_groups | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'assign instance'
Assign an instance to a security group

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**instance\_id** |  required  | The ID of the instance | string |  `aws ec2 instance id` 
**group\_id** |  required  | The security group ID to add | string |  `aws ec2 group id` 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.group\_id | string |  `aws ec2 group id` 
action\_result\.parameter\.instance\_id | string |  `aws ec2 instance id` 
action\_result\.parameter\.credentials | string |  `aws credentials` 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-length | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-type | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.server | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.data\.\*\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.summary\.status | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'remove instance'
Removes an instance from a security group

Type: **contain**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**instance\_id** |  required  | The ID of the instance | string |  `aws ec2 instance id` 
**group\_id** |  required  | The security group ID to remove | string |  `aws ec2 group id` 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.group\_id | string |  `aws ec2 group id` 
action\_result\.parameter\.instance\_id | string |  `aws ec2 instance id` 
action\_result\.parameter\.credentials | string |  `aws credentials` 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-length | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-type | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.server | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.data\.\*\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.summary\.status | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'create vpc'
Create a VPC with the specified IPv4 CIDR block

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**cidr\_block** |  required  | The IPv4 network range for the VPC, in CIDR notation\. For example\: 10\.0\.0\.0/16 | string | 
**amazon\_provided\_ipv6\_cidr\_block** |  optional  | The Amazon provided IPv6 CIDR block with a /56 prefix length | boolean | 
**dry\_run** |  optional  | Check if asset has required permissions for the action | boolean | 
**instance\_tenancy** |  optional  | The tenancy options for instances launched into the VPC | string | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.amazon\_provided\_ipv6\_cidr\_block | boolean | 
action\_result\.parameter\.cidr\_block | string | 
action\_result\.parameter\.dry\_run | boolean | 
action\_result\.parameter\.instance\_tenancy | string | 
action\_result\.parameter\.credentials | string |  `aws credentials` 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-length | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-type | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.server | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.data\.\*\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.data\.\*\.Vpc\.CidrBlock | string | 
action\_result\.data\.\*\.Vpc\.CidrBlockAssociationSet\.\*\.AssociationId | string | 
action\_result\.data\.\*\.Vpc\.CidrBlockAssociationSet\.\*\.CidrBlock | string | 
action\_result\.data\.\*\.Vpc\.CidrBlockAssociationSet\.\*\.CidrBlockState\.State | string | 
action\_result\.data\.\*\.Vpc\.DhcpOptionsId | string | 
action\_result\.data\.\*\.Vpc\.InstanceTenancy | string | 
action\_result\.data\.\*\.Vpc\.Ipv6CidrBlockAssociationSet\.\*\.AssociationId | string | 
action\_result\.data\.\*\.Vpc\.Ipv6CidrBlockAssociationSet\.\*\.Ipv6CidrBlock | string | 
action\_result\.data\.\*\.Vpc\.Ipv6CidrBlockAssociationSet\.\*\.Ipv6CidrBlockState\.State | string | 
action\_result\.data\.\*\.Vpc\.IsDefault | boolean | 
action\_result\.data\.\*\.Vpc\.OwnerId | string | 
action\_result\.data\.\*\.Vpc\.State | string | 
action\_result\.data\.\*\.Vpc\.VpcId | string |  `aws ec2 vpc id` 
action\_result\.summary\.instance\_tenancy | string | 
action\_result\.summary\.vpc\_id | string |  `aws ec2 vpc id` 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'list network interfaces'
Display network interfaces

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**filters** |  optional  | One or more filters in dictionary format, separated by commas\. Example\: \{ 'Name'\: 'string', 'Values'\: \[ 'string' \]\} | string | 
**dry\_run** |  optional  | Check if asset has required permissions for the action | boolean | 
**network\_interface\_ids** |  optional  | One or more network interface IDs, separated by commas | string |  `aws ec2 network interface id` 
**next\_token** |  optional  | The token to request the next page of results | string |  `aws ec2 next token` 
**max\_results** |  optional  | Maximum number of results to return in a single call | numeric | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.dry\_run | boolean | 
action\_result\.parameter\.filters | string | 
action\_result\.parameter\.max\_results | numeric | 
action\_result\.parameter\.network\_interface\_ids | string |  `aws ec2 network interface id` 
action\_result\.parameter\.next\_token | string |  `aws ec2 next token` 
action\_result\.parameter\.credentials | string |  `aws credentials` 
action\_result\.data\.\*\.NetworkInterfaces\.\*\.Association\.AllocationId | string | 
action\_result\.data\.\*\.NetworkInterfaces\.\*\.Association\.AssociationId | string | 
action\_result\.data\.\*\.NetworkInterfaces\.\*\.Association\.IpOwnerId | string | 
action\_result\.data\.\*\.NetworkInterfaces\.\*\.Association\.PublicDnsName | string | 
action\_result\.data\.\*\.NetworkInterfaces\.\*\.Association\.PublicIp | string |  `ip` 
action\_result\.data\.\*\.NetworkInterfaces\.\*\.Attachment\.AttachTime | string | 
action\_result\.data\.\*\.NetworkInterfaces\.\*\.Attachment\.AttachmentId | string | 
action\_result\.data\.\*\.NetworkInterfaces\.\*\.Attachment\.DeleteOnTermination | boolean | 
action\_result\.data\.\*\.NetworkInterfaces\.\*\.Attachment\.DeviceIndex | numeric | 
action\_result\.data\.\*\.NetworkInterfaces\.\*\.Attachment\.InstanceId | string | 
action\_result\.data\.\*\.NetworkInterfaces\.\*\.Attachment\.InstanceOwnerId | string | 
action\_result\.data\.\*\.NetworkInterfaces\.\*\.Attachment\.Status | string | 
action\_result\.data\.\*\.NetworkInterfaces\.\*\.AvailabilityZone | string | 
action\_result\.data\.\*\.NetworkInterfaces\.\*\.Description | string | 
action\_result\.data\.\*\.NetworkInterfaces\.\*\.Groups\.\*\.GroupId | string | 
action\_result\.data\.\*\.NetworkInterfaces\.\*\.Groups\.\*\.GroupName | string | 
action\_result\.data\.\*\.NetworkInterfaces\.\*\.InterfaceType | string | 
action\_result\.data\.\*\.NetworkInterfaces\.\*\.MacAddress | string | 
action\_result\.data\.\*\.NetworkInterfaces\.\*\.NetworkInterfaceId | string | 
action\_result\.data\.\*\.NetworkInterfaces\.\*\.OwnerId | string | 
action\_result\.data\.\*\.NetworkInterfaces\.\*\.PrivateDnsName | string | 
action\_result\.data\.\*\.NetworkInterfaces\.\*\.PrivateIpAddress | string |  `ip` 
action\_result\.data\.\*\.NetworkInterfaces\.\*\.PrivateIpAddresses\.\*\.Association\.AllocationId | string | 
action\_result\.data\.\*\.NetworkInterfaces\.\*\.PrivateIpAddresses\.\*\.Association\.AssociationId | string | 
action\_result\.data\.\*\.NetworkInterfaces\.\*\.PrivateIpAddresses\.\*\.Association\.IpOwnerId | string | 
action\_result\.data\.\*\.NetworkInterfaces\.\*\.PrivateIpAddresses\.\*\.Association\.PublicDnsName | string | 
action\_result\.data\.\*\.NetworkInterfaces\.\*\.PrivateIpAddresses\.\*\.Association\.PublicIp | string |  `ip` 
action\_result\.data\.\*\.NetworkInterfaces\.\*\.PrivateIpAddresses\.\*\.Primary | boolean | 
action\_result\.data\.\*\.NetworkInterfaces\.\*\.PrivateIpAddresses\.\*\.PrivateDnsName | string | 
action\_result\.data\.\*\.NetworkInterfaces\.\*\.PrivateIpAddresses\.\*\.PrivateIpAddress | string |  `ip` 
action\_result\.data\.\*\.NetworkInterfaces\.\*\.RequesterId | string | 
action\_result\.data\.\*\.NetworkInterfaces\.\*\.RequesterManaged | boolean | 
action\_result\.data\.\*\.NetworkInterfaces\.\*\.SourceDestCheck | boolean | 
action\_result\.data\.\*\.NetworkInterfaces\.\*\.Status | string | 
action\_result\.data\.\*\.NetworkInterfaces\.\*\.SubnetId | string | 
action\_result\.data\.\*\.NetworkInterfaces\.\*\.TagSet\.\*\.Key | string | 
action\_result\.data\.\*\.NetworkInterfaces\.\*\.TagSet\.\*\.Value | string | 
action\_result\.data\.\*\.NetworkInterfaces\.\*\.VpcId | string |  `aws ec2 vpc id` 
action\_result\.data\.\*\.NextToken | string |  `aws ec2 next token` 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-length | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-type | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.server | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.transfer\-encoding | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.vary | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.data\.\*\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.summary\.num\_network\_interfaces | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'list autoscaling groups'
Display autoscaling groups

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**autoscaling\_group\_names** |  optional  | The names of the Auto Scaling groups, separated by commas | string |  `aws ec2 autoscaling group name` 
**next\_token** |  optional  | The token for the next set of items to return | string |  `aws ec2 next token` 
**max\_results** |  optional  | Maximum number of results to return in a single call | numeric | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.autoscaling\_group\_names | string |  `aws ec2 autoscaling group name` 
action\_result\.parameter\.max\_results | numeric | 
action\_result\.parameter\.next\_token | string |  `aws ec2 next token` 
action\_result\.parameter\.credentials | string |  `aws credentials` 
action\_result\.data\.\*\.AutoScalingGroups\.\*\.AutoScalingGroupARN | string | 
action\_result\.data\.\*\.AutoScalingGroups\.\*\.AutoScalingGroupName | string |  `aws ec2 autoscaling group name` 
action\_result\.data\.\*\.AutoScalingGroups\.\*\.AvailabilityZones | string | 
action\_result\.data\.\*\.AutoScalingGroups\.\*\.CreatedTime | string | 
action\_result\.data\.\*\.AutoScalingGroups\.\*\.DefaultCooldown | numeric | 
action\_result\.data\.\*\.AutoScalingGroups\.\*\.DesiredCapacity | numeric | 
action\_result\.data\.\*\.AutoScalingGroups\.\*\.HealthCheckGracePeriod | numeric | 
action\_result\.data\.\*\.AutoScalingGroups\.\*\.HealthCheckType | string | 
action\_result\.data\.\*\.AutoScalingGroups\.\*\.Instances\.\*\.AvailabilityZone | string | 
action\_result\.data\.\*\.AutoScalingGroups\.\*\.Instances\.\*\.HealthStatus | string | 
action\_result\.data\.\*\.AutoScalingGroups\.\*\.Instances\.\*\.InstanceId | string | 
action\_result\.data\.\*\.AutoScalingGroups\.\*\.Instances\.\*\.LaunchConfigurationName | string | 
action\_result\.data\.\*\.AutoScalingGroups\.\*\.Instances\.\*\.LifecycleState | string | 
action\_result\.data\.\*\.AutoScalingGroups\.\*\.Instances\.\*\.ProtectedFromScaleIn | boolean | 
action\_result\.data\.\*\.AutoScalingGroups\.\*\.LaunchConfigurationName | string | 
action\_result\.data\.\*\.AutoScalingGroups\.\*\.MaxSize | numeric | 
action\_result\.data\.\*\.AutoScalingGroups\.\*\.MinSize | numeric | 
action\_result\.data\.\*\.AutoScalingGroups\.\*\.MixedInstancesPolicy\.InstancesDistribution\.OnDemandAllocationStrategy | string | 
action\_result\.data\.\*\.AutoScalingGroups\.\*\.MixedInstancesPolicy\.InstancesDistribution\.OnDemandBaseCapacity | numeric | 
action\_result\.data\.\*\.AutoScalingGroups\.\*\.MixedInstancesPolicy\.InstancesDistribution\.OnDemandPercentageAboveBaseCapacity | numeric | 
action\_result\.data\.\*\.AutoScalingGroups\.\*\.MixedInstancesPolicy\.InstancesDistribution\.SpotAllocationStrategy | string | 
action\_result\.data\.\*\.AutoScalingGroups\.\*\.MixedInstancesPolicy\.LaunchTemplate\.LaunchTemplateSpecification\.LaunchTemplateId | string | 
action\_result\.data\.\*\.AutoScalingGroups\.\*\.MixedInstancesPolicy\.LaunchTemplate\.LaunchTemplateSpecification\.LaunchTemplateName | string | 
action\_result\.data\.\*\.AutoScalingGroups\.\*\.MixedInstancesPolicy\.LaunchTemplate\.LaunchTemplateSpecification\.Version | string | 
action\_result\.data\.\*\.AutoScalingGroups\.\*\.MixedInstancesPolicy\.LaunchTemplate\.Overrides\.\*\.InstanceType | string | 
action\_result\.data\.\*\.AutoScalingGroups\.\*\.NewInstancesProtectedFromScaleIn | boolean | 
action\_result\.data\.\*\.AutoScalingGroups\.\*\.ServiceLinkedRoleARN | string | 
action\_result\.data\.\*\.AutoScalingGroups\.\*\.Tags\.\*\.Key | string | 
action\_result\.data\.\*\.AutoScalingGroups\.\*\.Tags\.\*\.PropagateAtLaunch | boolean | 
action\_result\.data\.\*\.AutoScalingGroups\.\*\.Tags\.\*\.ResourceId | string | 
action\_result\.data\.\*\.AutoScalingGroups\.\*\.Tags\.\*\.ResourceType | string | 
action\_result\.data\.\*\.AutoScalingGroups\.\*\.Tags\.\*\.Value | string | 
action\_result\.data\.\*\.AutoScalingGroups\.\*\.TerminationPolicies | string | 
action\_result\.data\.\*\.AutoScalingGroups\.\*\.VPCZoneIdentifier | string | 
action\_result\.data\.\*\.NextToken | string |  `aws ec2 next token` 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-length | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-type | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.vary | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amzn\-requestid | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.data\.\*\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.summary\.num\_autoscaling\_groups | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 