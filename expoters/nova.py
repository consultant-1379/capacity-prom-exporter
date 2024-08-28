#!/usr/bin/python2.7


import utils


def _get_total_memory():
    token, nova, cinder = utils.get_clients()
    hy_stat = nova.hypervisor_stats.statistics()
    total_memory = vars(hy_stat)['memory_mb']
    return utils.conv_mb_to_gb(total_memory)

def get_nova_limits(nova):
    projects = utils.list_projects()
    _list = []
    for project in projects:
        compute_limits = nova.limits.get(tenant_id = project['id']).absolute
        limits =  utils.convert_gen_to_dict(compute_limits)
        project['compute_limit'] = limits
        _list.append(project)
    return _list


def get_nova_quota(nova):
    project_list = utils.list_projects()
    _dict = {}
    _list = []
    for project in project_list:
        _dict = nova.quotas.get(project['id']).to_dict()
        project['compute_quota'] = _dict
        _list.append(project)
    return _list



def _get_total_cores():
    token, nova, cinder = utils.get_clients()
    hy_stat = nova.hypervisor_stats.statistics()
    return vars(hy_stat)['vcpus']


def _get_total_allocated_memory():
    token, nova, cinder = utils.get_clients()
    ram_size = 0
    for i in get_nova_quota(nova):
        ram_size = ram_size + i['compute_quota']['ram']
    return utils.conv_mb_to_gb(ram_size)


def _get_total_allocated_cores():
    token, nova, cinder = utils.get_clients()
    cores = 0
    for i in get_nova_quota(nova):
        cores = cores + i['compute_quota']['cores']
    return cores


def _get_allocated_memory_per_tenant():
    token, nova, cinder = utils.get_clients()
    _data = {}
    for i in get_nova_quota(nova):
        _data[i['name']] = utils.conv_mb_to_gb(i['compute_quota']['ram'])
    return _data
    
def _get_allocated_cores_per_tenant():
    token, nova, cinder = utils.get_clients()
    _data = {}
    for i in get_nova_quota(nova):
        _data[i['name']] = i['compute_quota']['cores']
    return _data

def _get_memory_used_per_tenant():
    token, nova, cinder = utils.get_clients()
    _data = {}
    for i in get_nova_limits(nova):
        _data[i['name']] = utils.conv_mb_to_gb(i['compute_limit']['totalRAMUsed'])
    return _data

def _get_cores_used_per_tenant():
    token, nova, cinder = utils.get_clients()
    _data = {}
    for i in get_nova_limits(nova):
        _data[i['name']] = i['compute_limit']['totalCoresUsed']
    return _data


def _get_hypervisor_stats():
    token, nova, cinder = utils.get_clients()
    hypervisors = nova.hypervisors.list()
    _list = []
    for hypervisor in hypervisors:
        hyp = hypervisor.to_dict()
        _dict = {}
        _dict['name']            =  hyp['hypervisor_hostname']
        _dict['memory']          =  utils.conv_mb_to_gb(hyp['memory_mb'])
        _dict['memory_used']     =  utils.conv_mb_to_gb(hyp['memory_mb_used'])
        _dict['vcpus']           =  hyp['vcpus']
        _dict['vcpus_used']      =  hyp['vcpus_used']
       # _dict['status']          = hyp['status']  // Prom doesn't support string as value
        _dict['running_vms']     =  hyp['running_vms']
        _list.append(_dict)
    return _list
