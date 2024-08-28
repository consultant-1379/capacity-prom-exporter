#!/usr/bin/python2.7


import utils
from os import environ as env

# Authenticate and create session

token, nova, cinder = utils.get_clients()


OS_PROJECT_ID = env['OS_PROJECT_ID']

def get_volume_stats(token, project_id):
    auth_url = utils.get_creds_dict('auth_url')['auth_url']
    cinder_endpoint =  auth_url.replace('13000','13776') + '/' + project_id + '/volumes/detail?all_tenants=True'
    _data = utils._cinder_limits(token, cinder_endpoint)
    return _data


vol_data =  get_volume_stats(token, OS_PROJECT_ID)['volumes']

def get_volume_quota(cinder):
    token, nova, cinder = utils.get_clients()
    projects = utils.list_projects()
    _dict = {}
    _list = []
    for project in projects:
        _dict = cinder.quotas.get(project['id']).to_dict()
        project['volume_quota'] = _dict
        _list.append(project)
    return _list


def _get_total_used_volume():
    size = 0
    for vol in vol_data:
        size = size + vol['size']
    return size

def _get_total_volume_per_tenant():
    token, nova, cinder = utils.get_clients()
    project_list = utils.list_projects()
    _dict = {}
    _list = []
    for project in project_list:
        _size = 0
        total_size = 0
        for vol in vol_data:
            if project['id'] != vol['os-vol-tenant-attr:tenant_id']:
                continue
            _size = _size + vol['size']
            total_size = _size
        _dict[project['name'] ] = total_size
    return _dict

def _get_allocated_volume_per_tenant():
    token, nova, cinder = utils.get_clients()
    _data = {}
    for i in get_volume_quota(cinder):
        _data[i['name']] = i['volume_quota']['gigabytes']
    return _data

        
def _get_total_allocated_volume():
    token, nova, cinder = utils.get_clients()
    _size = 0
    for i in get_volume_quota(cinder):
        _size = _size + i['volume_quota']['gigabytes']
    return _size


