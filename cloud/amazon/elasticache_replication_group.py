#!/usr/bin/python
#
DOCUMENTATION = """
---
module: elasticache_tag
short_description: create and remove tag(s) to ec2 resources.
description:
    - Creates, removes and modifies any ElastiCache Replication Group resource.  The resource is referenced by its resource name. This module has a dependency on boto3.
version_added: "1"
options:
  state:
    description:
      - Whether the tags should be present or absent on the resource. Use list to interrogate the tags of an instance.
    required: false
    default: present
    choices: ['present', 'absent']
    aliases: []
  automatic_failover_enabled:
    description:
      - Specifies whether a read-only replica will be automatically promoted to read/write primary if the existing primary fails. If yes, Multi-AZ is enabled for this replication group. If no, Multi-AZ is disabled for this replication group.
    required: false
    default: no
    choices: [ "yes", "no" ]
    aliases: []
  apply_immediately:
    description:
      - If yes, this parameter causes the modifications in this request and any pending modifications to be applied, asynchronously and as soon as possible, regardless of the PreferredMaintenanceWindow setting for the replication group. If no, then changes to the nodes in the replication group are applied on the next maintenance reboot, or the next failure reboot, whichever occurs first.
    required: false
    default: no
    choices: [ "yes", "no" ]
    aliases: []
  name:
    description:
      - The identifier of the replication group to create/modify. Must be less than 14 characters with no spaces. Dashes are permitted.
    required: true
    aliases: []
  cache_node_type:
    description:
      - A valid cache node type that you want to scale this replication group to. When modifying, the value of this parameter must be one of the ScaleUpModifications values returned by the ListAllowedCacheNodeTypeModification action.
    required: false
    default: cache.m3.medium
    aliases: []
  cache_subnet_group_name:
    description:
      - The name of the cache subnet group associated with the cache cluster. If not supplied, default will be chosen.
    required: false
    aliases: []
  region:
    description:
      - The AWS region to use. If not specified then the value of the AWS_REGION or EC2_REGION environment variable, if any, is used. See http://docs.aws.amazon.com/general/latest/gr/rande.html#ec2_region
    required: false
    aliases: ['aws_region', 'ec2_region']
  primary_cluster_id:
    description:
      - The identifier of the cache cluster that will serve as the primary for this replication group. This cache cluster must already exist and have a status of available. This parameter is not required if NumCacheClusters is specified.
    required: false
    aliases: []
  num_cache_clusters:
    description:
      - The number of cache clusters this replication group should have, new clusters will be created and extra clusters will be deleted. If Multi-AZ is enabled, the value of this parameter must be at least 2. The maximum permitted value for NumCacheClusters is 6 (primary plus 5 replicas). If you need to exceed this limit, please fill out the ElastiCache Limit Increase Request form at http://aws.amazon.com/contact-us/elasticache-node-limit-request.
    required: false
    aliases: []
  engine:
    description:
      - The name of the cache engine to be used for the cache clusters in this replication group.
    required: false
    default: redis
    aliases: []
  engine_version:
    description:
      - The version number of the cache engine to be used for the cache clusters in this replication group. To view the supported cache engine versions, use the DescribeCacheEngineVersions action.
    required: false
    aliases: []
  replication_group_description:
    description:
      - A user-created description for the replication group.
    required: true
    aliases: []
  security_group_ids:
    description:
      - One or more Amazon VPC security groups associated with this replication group. Use this parameter only when you are creating a replication group in an Amazon Virtual Private Cloud (VPC).
    required: false
    aliases: []
  preferred_cache_cluster_azs:
    description:
      - A list of EC2 availability zones in which the replication group's cache clusters will be created. The order of the availability zones in the list is not important. The number of availability zones listed must equal the value of NumCacheClusters. Default: system chosen availability zones.
    required: false
    aliases: []
  cache_security_group_names:
    description:
      - A list of cache security group names to associate with this replication group.
    required: false
    aliases: []
  cache_parameter_group_name:
    description:
      - The name of the parameter group to associate with this replication group. If this argument is omitted, the default cache parameter group for the specified engine is used.
    required: false
    aliases: []
  auto_minor_version_upgrade:
    description:
      - This parameter is currently disabled.
    default: yes
    choices: [ "yes", "no" ]
    aliases: []
  port:
    description:
      - The port number on which each member of the replication group will accept connections.
    required: false
    default: 6379
    aliases: []
  notification_topic_arn:
    description: 
      - The ARN for the SNS topic to be notified.
    required: false
    aliases: []
  notification_topic_status:
    description: 
      - The status of the Amazon SNS notification topic for the replication group. Notifications are sent only if the status is active .
    default: active
    choices: [ "active", "inactive" ]
    required: false
    aliases: []
  snapshot_retention_limit:
    description:
      - The number of days for which ElastiCache will retain automatic cache cluster snapshots before deleting them. For example, if you set SnapshotRetentionLimit to 5, then a snapshot that was taken today will be retained for 5 days before being deleted.
    required: false
    aliases: []
  snapshot_window:
    description: 
      - The daily time range (in UTC) during which ElastiCache will begin taking a daily snapshot of your cache cluster. Example: 05:00-09:00
    required: false
    aliases: []
  snapshot_arns:
    description: 
      - A single-element string list containing an Amazon Resource Name (ARN) that uniquely identifies a Redis RDB snapshot file stored in Amazon S3. The snapshot file will be used to populate the node group. The Amazon S3 object name in the ARN cannot contain any commas.
      - Note: This parameter is only valid if the Engine parameter is redis.
      - Example of an Amazon S3 ARN: arn:aws:s3:::my_bucket/snapshot1.rdb
    required: false
    aliases: []
  snapshot_name:
    description: 
      - The name of a snapshot from which to restore data into the new node group. The snapshot status changes to restoring while the new node group is being created.
      - Note: This parameter is only valid if the Engine parameter is redis.
    required: false
    aliases: []
  preferred_maintenance_window:
    description:
      - Specifies the weekly time range during which maintenance on the cache cluster is performed. It is specified as a range in the format ddd:hh24:mi-ddd:hh24:mi (24H Clock UTC). The minimum maintenance window is a 60 minute period. Valid values for ddd are:
      - sun
      - mon
      - tue
      - wed
      - thu
      - fri
      - sat
      - Example: sun:05:00-sun:09:00
    required: false
    aliases: []
  snapshotting_cluster_id:
    description:
      - The cache cluster ID that is used as the daily snapshot source for the replication group.
    required: false
    aliases: []
  retain_primary_cluster:
    description:
      - "When state is 'absent', if set to yes, all of the read replicas will be deleted, but the primary node will be retained."
    required: false
    default: no
    choices: [ "yes", "no" ]
    aliases: []
  final_snapshot_identifier:
    description:
      - "When state is 'absent', this is the name of a final node group snapshot. ElastiCache creates the snapshot from the primary node in the cluster, rather than one of the replicas; this is to ensure that it captures the freshest data. After the final snapshot is taken, the cluster is immediately deleted."
    required: false
    aliases: []
  snapshot_on_num_cache_clusters:
    description:
      - Whether to create a snapshot of nodes that are destroyed during negative changes to the num_cache_clusters option. 
    required: false
    default: no
    choices: [ "yes", "no" ]
    aliases: []
  wait:
    description:
      - Wait for cache cluster result before returning
    required: false
    default: yes
    choices: [ "yes", "no" ]
    aliases: []
extends_documentation_fragment:
    - aws
    - ec2
"""

EXAMPLES = """
# Note: None of these examples set aws_access_key, aws_secret_key, or region.
# It is assumed that their matching environment variables are set.

# Basic example
- elasticache_replication_group:
    state: present
    name: redis-g2
    replication_group_description: This is the replication group for redis elasticache.
    cache_subnet_group_name: elasticache-subnet-group
    security_group_ids:
      - sg-xxxxxxx
    apply_immediately: yes
    wait: yes
  register: replication_group

# Multiple nodes in same AZ
- elasticache_replication_group:
    state: present
    name: redis-gp
    replication_group_description: This is the replication group for redis elasticache.
    snapshot_retention_limit: 10
    automatic_failover_enabled: yes
    num_cache_clusters: 2
    snapshot_on_num_cache_clusters: no
    cache_node_type: cache.m3.medium
    engine: redis
    engine_version: 2.8.24
    region: "us-west-2"
    cache_parameter_group_name: default.redis2.8
    cache_subnet_group_name: elasticache-subnet-group
    port: 123
    security_group_ids:
      - "sg-xxxxxxx"
    preferred_cache_cluster_azs:
      - "us-west-2a"
      - "us-west-2a"
    apply_immediately: yes
    wait: yes
  register: replication_group

"""

import sys
import os
import time

try:
    import boto
    import boto.ec2
    HAS_BOTO = True
except ImportError:
    HAS_BOTO = False

try:
    import boto3
    import botocore
    HAS_BOTO3 = True
except ImportError:
    HAS_BOTO3 = False

class ElastiCacheReplicationGroupManager(object):

    def __init__(self):
        pass

def main():
    argument_spec = ec2_argument_spec()

    argument_spec.update(dict(
            state={'required': False, 'choices': ['present', 'absent'], 'default':'present'},
            automatic_failover_enabled={'required': False, 'type' : 'bool', 'default': False},
            apply_immediately={'required': False, 'type' : 'bool', 'default': False},
            name={'required': True},
            cache_node_type={'required': False, 'default':'cache.m3.medium'},
            cache_subnet_group_name={'required': False},
            region={'required': False},
            primary_cluster_id={'required': False},
            num_cache_clusters={'required': False, 'type' : 'int', 'default': 2},
            engine={'required': False},
            engine_version={'required': False},
            replication_group_description={'required': True},
            security_group_ids={'required': False, 'type': 'list'},
            preferred_cache_cluster_azs={'required': False, 'type': 'list'},
            cache_security_group_names={'required': False, 'type': 'list'},
            cache_parameter_group_name={'required': False},
            auto_minor_version_upgrade={'required': False, 'type' : 'bool', 'default': True},
            port={'required': False, 'type' : 'int', 'default': 6379},
            snapshot_retention_limit={'required': False, 'default': 0},
            snapshot_window={'required': False},
            snapshotting_cluster_id={'required': False},
            retain_primary_cluster={'required': False, 'type' : 'bool', 'default': False},
            final_snapshot_identifier={'required': False},
            snapshot_on_num_cache_clusters={'required': False, 'type' : 'bool', 'default': False},
            wait={'required': False, 'type' : 'bool', 'default': True},
            hard_modify={'required': False, 'type': 'bool', 'default': False},
            notification_topic_arn={'required':False},
            preferred_maintenance_window={'required': False},
            snapshot_name={'required': False},
            snapshot_arns={'required': False, 'type': 'list'},
            notification_topic_status={'required': False, 'default':'active'},
        )
    )
    
    module = AnsibleModule(
        argument_spec=argument_spec,
    )

    if not HAS_BOTO or not HAS_BOTO3:
        module.fail_json(msg='boto3 required for this module')

    state = module.params.get('state')
    automatic_failover_enabled = module.params.get('automatic_failover_enabled')
    auto_minor_version_upgrade = module.params.get('auto_minor_version_upgrade')
    preferred_cache_cluster_azs = module.params.get('preferred_cache_cluster_azs')
    num_cache_clusters = module.params.get('num_cache_clusters')
    apply_immediately = module.params.get('apply_immediately')
    name = module.params.get('name')
    primary_cluster_id = module.params.get('primary_cluster_id')
    replication_group_description = module.params.get('replication_group_description')
    security_group_ids = module.params.get('security_group_ids')
    engine_version = module.params.get('engine_version')
    cache_parameter_group_name = module.params.get('cache_parameter_group_name')
    cache_security_group_names = module.params.get('cache_security_group_names')
    cache_subnet_group_name = module.params.get('cache_subnet_group_name')
    engine = module.params.get('engine')
    cache_node_type = module.params.get('cache_node_type')
    port = module.params.get('port')
    snapshot_retention_limit = module.params.get('snapshot_retention_limit')
    snapshot_window = module.params.get('snapshot_window')
    snapshotting_cluster_id = module.params.get('snapshotting_cluster_id')
    retain_primary_cluster = module.params.get('retain_primary_cluster')
    final_snapshot_identifier = module.params.get('final_snapshot_identifier')
    snapshot_on_num_cache_clusters = module.params.get('snapshot_on_num_cache_clusters')
    preferred_maintenance_window = module.params.get('preferred_maintenance_window')
    notification_topic_arn = module.params.get('notification_topic_arn')
    snapshot_arns = module.params.get('snapshot_arns')
    snapshot_name = module.params.get('snapshot_name')
    notification_topic_status = module.params.get('notification_topic_status')
    wait = module.params.get('wait')
    hard_modify = module.params.get('hard_modify')
    
    region, ec2_url, aws_connect_kwargs = get_aws_connection_info(module)
    if module.params.get('region'):
        region = module.params.get('region')
    
    conn = boto3.client('elasticache', region_name=region)

    replication_group_data = {}
    changed = False

    if state == 'present':
        found = False
        try:
            replication_group_data = conn.describe_replication_groups(ReplicationGroupId=name)['ReplicationGroups'][0]
            found = True
        except botocore.exceptions.ClientError, ex:
            found = False
        if name and found:
            #Modify
            modify_dict = {
                "ReplicationGroupId":name,
                "ReplicationGroupDescription":replication_group_description,
                "AutomaticFailoverEnabled":automatic_failover_enabled,
                "ApplyImmediately":apply_immediately,
                "AutoMinorVersionUpgrade":auto_minor_version_upgrade,
                "SnapshotRetentionLimit":snapshot_retention_limit,
                "CacheNodeType":cache_node_type
            }

            if primary_cluster_id:
                modify_dict['PrimaryClusterId'] = primary_cluster_id
            if snapshotting_cluster_id:
                modify_dict['SnapshottingClusterId'] = snapshotting_cluster_id
            if engine_version:
                modify_dict['EngineVersion'] = engine_version
            if snapshot_window:
                modify_dict['SnapshotWindow'] = snapshot_window
            if preferred_maintenance_window:
                create_dict['PreferredMaintenanceWindow'] = preferred_maintenance_window
            if security_group_ids:
                modify_dict['SecurityGroupIds'] = security_group_ids
            if cache_security_group_names:
                modify_dict['CacheSecurityGroupNames'] = cache_security_group_names
            if notification_topic_arn:
                modify_dict['NotificationTopicArn'] = notification_topic_arn
            if notification_topic_status:
                modify_dict['NotificationTopicStatus'] = notification_topic_status
            if cache_parameter_group_name:
                modify_dict['CacheParameterGroupName'] = cache_parameter_group_name

            try:
                if replication_group_data['Status'] != 'available' and len(replication_group_data['MemberClusters']) == len(replication_group_data['NodeGroups'][0]['NodeGroupMembers']):
                    while True:
                        time.sleep(10)
                        try:
                            response = conn.describe_replication_groups(ReplicationGroupId=name)
                            replication_group_data = response['ReplicationGroups'][0]
                            if not wait:
                                break
                        except botocore.exceptions.ClientError, ex:
                            module.fail_json(msg='Modified replication group not found: ', error=ex)
                            break
                        if replication_group_data['Status'] == 'available' and len(replication_group_data['MemberClusters']) == len(replication_group_data['NodeGroups'][0]['NodeGroupMembers']):
                            break
                modified_group = conn.modify_replication_group(**modify_dict)
                changed = True
                while True:
                    time.sleep(10)
                    try:
                        response = conn.describe_replication_groups(ReplicationGroupId=name)
                        replication_group_data = response['ReplicationGroups'][0]
                        if not wait:
                            break
                    except botocore.exceptions.ClientError, ex:
                        module.fail_json(msg='Modified replication group not found: ', error=ex)
                        break
                    if replication_group_data['Status'] == 'available':
                        break
            except botocore.exceptions.ClientError, ex:
                module.fail_json(msg='Failed to modify replication group: ', error=ex)
            intial_length = len(replication_group_data['MemberClusters'])
            if num_cache_clusters and intial_length and intial_length != num_cache_clusters:
                if not preferred_cache_cluster_azs or len(preferred_cache_cluster_azs) == num_cache_clusters:
                    if intial_length < num_cache_clusters:
                        # Create Clusters for Replication Group
                        i = 1
                        while intial_length+i <= num_cache_clusters:
                            new_cache_cluster_id = str(intial_length+i)
                            new_cache_cluster_dict = {
                                "CacheClusterId":name+'-'+new_cache_cluster_id.rjust(3, '0'),
                                "ReplicationGroupId":name
                            }
                            new_az = (preferred_cache_cluster_azs and preferred_cache_cluster_azs[intial_length+i-1])
                            if new_az:
                                new_cache_cluster_dict['PreferredAvailabilityZone'] = preferred_cache_cluster_azs[intial_length+i-1]

                            try:
                                conn.create_cache_cluster(**new_cache_cluster_dict)
                            except botocore.exceptions.ClientError, ex:
                                module.fail_json(msg='There was a problem creating additional clusters for this replication group: ', error=ex)
                                break
                            i += 1
                    if intial_length > num_cache_clusters:
                        # Remove Clusters for Replication Group
                        i = 1
                        while intial_length-i >= num_cache_clusters:
                            removed_cache_cluster_id = replication_group_data['MemberClusters'][intial_length-i]
                            try:
                                delete_cache_cluster_dict = {
                                    "CacheClusterId":removed_cache_cluster_id
                                }
                                if snapshot_on_num_cache_clusters:
                                    delete_cache_cluster_dict['FinalSnapshotIdentifier'] = removed_cache_cluster_id+'-'+str(int(round(time.time() * 1000)))
                                conn.delete_cache_cluster(**delete_cache_cluster_dict)
                            except botocore.exceptions.ClientError, ex:
                                module.fail_json(msg='There was a problem removing clusters for this replication group: ', error=ex)
                                break
                            i += 1
                    response = conn.describe_replication_groups(ReplicationGroupId=name)
                    while True:
                        time.sleep(10)
                        try:
                            response = conn.describe_replication_groups(ReplicationGroupId=name)
                            replication_group_data = response['ReplicationGroups'][0]
                            if not wait:
                                break
                        except botocore.exceptions.ClientError, ex:
                            module.fail_json(msg='Modified replication group not found: ', error=ex)
                            break
                        if replication_group_data['Status'] == 'available' and len(replication_group_data['MemberClusters']) == num_cache_clusters and len(replication_group_data['MemberClusters']) == len(replication_group_data['NodeGroups'][0]['NodeGroupMembers']):
                            break
                else:
                    module.fail_json(msg='preferred_cache_cluster_azs must have a length equal to num_cache_clusters.')
        else:
            #Create
            create_dict = {
                "ReplicationGroupId": name,
                "ReplicationGroupDescription":replication_group_description,
                "AutomaticFailoverEnabled":automatic_failover_enabled,
                "CacheNodeType":cache_node_type,
                "AutoMinorVersionUpgrade":auto_minor_version_upgrade,
                "SnapshotRetentionLimit":snapshot_retention_limit,
            }
            if primary_cluster_id:
                create_dict['PrimaryClusterId'] = primary_cluster_id
                if num_cache_clusters:
                    module.fail_json(msg='cannot use num_cache_clusters with primary_cluster_id')
            elif num_cache_clusters:
                create_dict["NumCacheClusters"] = num_cache_clusters
            if preferred_cache_cluster_azs:
                create_dict["PreferredCacheClusterAZs"] = preferred_cache_cluster_azs
            if snapshot_window:
                create_dict['SnapshotWindow'] = snapshot_window
            if snapshot_arns:
                create_dict['SnapshotArns'] = snapshot_arns
            if snapshot_name:
                create_dict['SnapshotName'] = snapshot_name
            if preferred_maintenance_window:
                create_dict['PreferredMaintenanceWindow'] = preferred_maintenance_window
            if cache_subnet_group_name:
                create_dict['CacheSubnetGroupName'] = cache_subnet_group_name
            if security_group_ids:
                create_dict['SecurityGroupIds'] = security_group_ids
            if cache_security_group_names:
                create_dict['CacheSecurityGroupNames'] = cache_security_group_names
            if cache_parameter_group_name:
                create_dict['CacheParameterGroupName'] = cache_parameter_group_name
            if engine:
                create_dict['Engine'] = engine
            if engine_version:
                create_dict['EngineVersion'] = engine_version
            if port:
                create_dict['Port'] = port
            if notification_topic_arn and notification_topic_status == 'active':
                create_dict['NotificationTopicArn'] = notification_topic_arn

            try:
                new_group = conn.create_replication_group(**create_dict)
                while True:
                    time.sleep(10)
                    try:
                        response = conn.describe_replication_groups(ReplicationGroupId=name)
                        replication_group_data = response['ReplicationGroups'][0]
                        if not wait:
                            break
                    except botocore.exceptions.ClientError, ex:
                        module.fail_json(msg='Created replication group not found: ', error=ex)
                        break
                    if replication_group_data['Status'] == 'available':
                        break
            except botocore.exceptions.ClientError, ex:
                module.fail_json(msg='Failed to create replication group: ', error=ex)

        # module.exit_json(msg="Tags %s created for resource %s." % (dictadd,resource), changed=True)
    if state == 'absent':
        delete_dict = {
            "ReplicationGroupId":name,
            "RetainPrimaryCluster":retain_primary_cluster
        }
        if final_snapshot_identifier:
            delete_dict['FinalSnapshotIdentifier'] = final_snapshot_identifier
        while True:
            time.sleep(10)
            try:
                response = conn.describe_replication_groups(ReplicationGroupId=name)
                replication_group_data = response['ReplicationGroups'][0]
            except botocore.exceptions.ClientError, ex:
                module.fail_json(msg='Created replication group not found: ', error=ex)
                break
            if replication_group_data['Status'] == 'available':
                break
        response = conn.delete_replication_group(**delete_dict)
        while wait:
            time.sleep(10)
            try:
                response = conn.describe_replication_groups(ReplicationGroupId=name)
            except botocore.exceptions.ClientError, ex:
                print ex
                break
            if response['ReplicationGroups'][0]['Status'] == 'gone':
                break
        module.exit_json(msg="Replication Group %s removed." % (name), changed=True)

    facts_result = dict(changed=changed,elasticache_replication_group=replication_group_data)

    module.exit_json(**facts_result)

# import module snippets
from ansible.module_utils.basic import *
from ansible.module_utils.ec2 import *

main()