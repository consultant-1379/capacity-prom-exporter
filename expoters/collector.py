import utils
import nova
import cinder




def get_metric_dict():

    metric_dict = {}

    # ENM Related metrics
    metric_dict['enm_count']               =  utils._get_enm_tenants_count()
    ## Workaround to calculate ENM capacity metrics required
    metric_dict['enm_supported_count']               =  0



    metric_dict['total_memory']     =   nova._get_total_memory()
    metric_dict['total_cores']      =   nova._get_total_cores()
    metric_dict['total_allocated_memory']   =   nova._get_total_allocated_memory()
    metric_dict['total_allocated_cores']    =   nova._get_total_allocated_cores()

    # Mocking total_disk value, it should come from cheph api
    metric_dict['total_volume']            =   40000
    metric_dict['total_allocated_volume']  =  cinder._get_total_allocated_volume()
    metric_dict['total_used_volume']       =  cinder._get_total_used_volume()
    metric_dict['tenant_allocated_volume'] =  cinder._get_allocated_volume_per_tenant()
    metric_dict['tenant_allocated_memory'] =  nova._get_allocated_memory_per_tenant()
    metric_dict['tenant_allocated_cores']  =  nova._get_allocated_cores_per_tenant()
    metric_dict['tenant_used_memory']      =  nova._get_memory_used_per_tenant()
    metric_dict['tenant_used_cores']       =  nova._get_cores_used_per_tenant()
    metric_dict['tenant_used_volume']      =  cinder._get_total_volume_per_tenant()
    



    #metric_dict['tenant_ram'] = compute.get_tenant_alloc_memory()
    #metric_dict['tenant_vcpu'] = compute.get_tenant_alloc_cores()
    #metric_dict['tenant_memory_usage'] = compute.get_tenant_memory_use()
    #metric_dict['tenant_core_usage'] = compute.get_tenant_core_use()
    #metric_dict['tenant_volume_usage'] = volume.get_tenant_volume_use()
    
    return metric_dict


def get_hypervisor_dict():

    metric_dict = nova._get_hypervisor_stats()

    return metric_dict
