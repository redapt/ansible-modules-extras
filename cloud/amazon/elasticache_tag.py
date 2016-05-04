#!/usr/bin/python
#
DOCUMENTATION = """
---
module: elasticache_tag
short_description: create and remove tag(s) to ec2 resources.
description:
    - Creates, removes and lists tags from any ElastiCache resource.  The resource is referenced by its resource id (e.g. an instance being i-XXXXXXX). It is designed to be used with complex args (tags), see the examples.  This module has a dependency on boto3.
version_added: "1"
options:
  resource_name:
    description:
      - The ElastiCache resource name. 
    required: true
    default: null 
    aliases: []
  state:
    description:
      - Whether the tags should be present or absent on the resource. Use list to interrogate the tags of an instance.
    required: false
    default: present
    choices: ['present', 'absent', 'list']
    aliases: []
  account:
    description:
      - AWS Account number, used to lookup cluster.
    required: true
    default: null
    aliases: []
  region:
    description:
      - AWS Region, used to lookup cluster.
    required: true
    default: null
    aliases: []
  tags:
    description:
      - a hash/dictionary of tags to add to the resource; '{"key":"value"}' and '{"key":"value","key":"value"}'
    required: true
    default: null
    aliases: []
extends_documentation_fragment:
    - aws
    - ec2
"""

EXAMPLES = '''
# Basic example of adding tag(s)
tasks:
- name: tag a resource
  elasticache_tag: 
    account: 12903812032
    region: us-west-2
    resource: cache-cluster-name
    state: present
    tags:
      Name: My Cache Cluster
      env: prod

'''

import sys
import time

try:
    import boto
    import boto.ec2
    HAS_BOTO = True
except ImportError:
    HAS_BOTO = False

try:
    import boto3
    HAS_BOTO3 = True
except ImportError:
    HAS_BOTO3 = False

def ConvertTagsDictToTagsList (d) :
    if not d :
        return []
    #reserve as much *distinct* dicts as the longest sequence
    result = []
    for (key, value) in d.items() :
        oneDict = dict()
        oneDict['Key'] = key
        oneDict['Value'] = value
        result.append(oneDict)
    return result

def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(
            resource = dict(required=True),
            account = dict(required=True),
            region = dict(required=True),
            tags = dict(type='dict'),
            state = dict(default='present', choices=['present', 'absent', 'list']),
        )
    )
    module = AnsibleModule(argument_spec=argument_spec)

    if not HAS_BOTO or not HAS_BOTO3:
        module.fail_json(msg='boto3 required for this module')

    resource_name = module.params.get('resource')
    tags = module.params.get('tags')
    state = module.params.get('state')
    region = module.params.get('region')
    account = module.params.get('account')

    conn = boto3.client('elasticache', region_name=region)
  
    resource = "arn:aws:elasticache:"+region+":"+account+":cluster:"+resource_name
    
    gettags = conn.list_tags_for_resource(ResourceName=resource)
   
    dictadd = {}
    listremove = []
    baddict = {}
    tagdict = {}
    for tag in gettags['TagList']:
        tagdict[tag['Key']] = tag['Value']

    if state == 'present':
        if not tags:
            module.fail_json(msg="tags argument is required when state is present")
        if set(tags.items()).issubset(set(tagdict.items())):
            module.exit_json(msg="Tags already exists in %s." %resource, changed=False)
        else:
            for (key, value) in set(tags.items()): 
                if (key, value) not in set(tagdict.items()):
                    dictadd[key] = value

        tagger = conn.add_tags_to_resource(ResourceName=resource, Tags=ConvertTagsDictToTagsList(dictadd))
        gettags = conn.list_tags_for_resource(ResourceName=resource)
        module.exit_json(msg="Tags %s created for resource %s." % (dictadd,resource), changed=True)
 
    if state == 'absent':
        if not tags:
            module.fail_json(msg="tags argument is required when state is absent")
        for (key, value) in set(tags.items()):
            if (key, value) not in set(tagdict.items()):
                    baddict[key] = value
                    if set(baddict) == set(tags):
                        module.exit_json(msg="Nothing to remove here. Move along.", changed=False)
        for (key, value) in set(tags.items()):
            if (key, value) in set(tagdict.items()):
                    listremove.append(key)
        tagger = conn.remove_tags_from_resource(ResourceName=resource, TagKeys=listremove)
        gettags = conn.list_tags_for_resource(ResourceName=resource)
        module.exit_json(msg="Tags %s removed for resource %s." % (listremove,resource), changed=True)

    if state == 'list':
        module.exit_json(changed=False, tags=tagdict)

# import module snippets
from ansible.module_utils.basic import *
from ansible.module_utils.ec2 import *

if __name__ == '__main__':
    main()
