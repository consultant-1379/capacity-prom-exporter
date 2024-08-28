import utils



sess = utils.create_session()
nova_conn = utils.connect_nova(sess)
ks_conn   = utils.connect_ks(sess)
cinder_conn = utils.connect_cinder(sess)

def get_hypervisor_stats(nova_conn):
    hy_stat = nova_conn.hypervisor_stats.statistics()
    return vars(hy_stat)


def get_total_memory():
    return utils.conv_mb_to_gb(hyp_stat['memory_mb'])


def get_total_tenant_alloc_memory():
    ram = 0
    for quota in compute_quotas:
        ram =  ram + quota['compute_quota']['ram']
    return utils.conv_mb_to_gb(ram)


def get_total_cpu():
    return hyp_stat['vcpus']

def get_total_tenant_alloc_vcpu():
    vcpu = 0
    for quota in compute_quotas:
         vcpu =  vcpu +  quota['compute_quota']['cores']
    return vcpu


def get_tenant_alloc_memory():
    _data = {}
    for i in compute_quotas:
        _data[i['name']] = utils.conv_mb_to_gb(i['compute_quota']['ram'])
    return _data

def get_tenant_alloc_cores():
    _data = {}
    for i in compute_quotas:
        _data[i['name']] =i['compute_quota']['cores']
    return _data

def get_tenant_memory_use():
    compute_limits = utils.get_compute_limits(nova_conn)
    _data = {}
    for i in compute_limits:
        _data[i['name']] = utils.conv_mb_to_gb(i['compute_limit']['totalRAMUsed'])
    return _data



def get_tenant_core_use():
    compute_limits = utils.get_compute_limits(nova_conn)
    _data = {}
    for i in compute_limits:
        _data[i['name']] = i['compute_limit']['totalCoresUsed']
    return _data

hyp_stat = get_hypervisor_stats(nova_conn)
compute_quotas = utils.get_nova_quota(nova_conn)




#print(get_tenant_alloc_memory())
#utils.list_project(ks_conn)

#format_dict(utils.list_project(ks_conn),compute_quotas)

#print(compute_quotas)

