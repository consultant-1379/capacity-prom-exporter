from prometheus_client.core import  GaugeMetricFamily, REGISTRY, CounterMetricFamily, Metric
from prometheus_client import start_http_server

import json
import requests
import time
import collector
import parser
import urllib3


# Suppress InsecureWarning while contanting openstack endpoints
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Initiating STDOUT log handler
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s:%(levelname)s:  %(message)s")
logger = logging.getLogger(__name__)


class CapacityCollector(object):

    def __init__(self):
      #  self._metrics_dict = metrics_dict
        pass

    def collect(self):
        logger.info('Collecting Capacity Metrics')
        metric_dict = collector.get_metric_dict()
        hyp_metrics = collector.get_hypervisor_dict()

        metric = Metric('os_capacity', 'Metrics taken in every 10 seconds', 'summary')
        _exculde = ['tenant_allocated_memory','tenant_allocated_cores','tenant_used_memory','tenant_used_cores', 'tenant_used_volume', 'tenant_allocated_volume']
        for data in metric_dict:
            if not data in _exculde:
                metric.add_sample(data, value=metric_dict[data], labels={})
        yield metric

        metric = Metric('tenant_allocated_memory', "Metrics taken in every 10 sec", 'summary')
        for k, v in metric_dict['tenant_allocated_memory'].items():
            metric.add_sample('tenant_allocated_memory', value=v, labels={'name': k})
        yield metric
 
        metric = Metric('tenant_allocated_cores', "Metrics taken in every 10 sec", 'summary')
        for k, v in metric_dict['tenant_allocated_cores'].items():
            metric.add_sample('tenant_allocated_cores', value=v, labels={'name': k})
        yield metric
 
        metric = Metric('tenant_used_memory', "Metrics taken in every 10 sec", 'summary')
        for k, v in metric_dict['tenant_used_memory'].items():
            metric.add_sample('tenant_used_memory', value=v, labels={'name': k})
        yield metric
 
        metric = Metric('tenant_used_cores', "Metrics taken in every 10 sec", 'summary')
        for k, v in metric_dict['tenant_used_cores'].items():
            metric.add_sample('tenant_used_cores', value=v, labels={'name': k})
        yield metric
 
        metric = Metric('tenant_used_volume', "Metrics taken in every 10 sec", 'summary')
        for k, v in metric_dict['tenant_used_volume'].items():
           metric.add_sample('tenant_used_volume', value=v, labels={'name': k})
        yield metric

        metric = Metric('tenant_allocated_volume', "Metrics taken in every 10 sec", 'summary')
        for k, v in metric_dict['tenant_allocated_volume'].items():
           metric.add_sample('tenant_allocated_volume', value=v, labels={'name': k})
        yield metric
       
       
        metric = Metric('hypervisor_stats','Help','summary')
        for each_hypervisor in hyp_metrics:
        
            name = each_hypervisor['name']
            for k, v in each_hypervisor.items():
                if k is 'name':
                    continue
                metric.add_sample(k, value=v, labels={'name': name})
            yield metric

if __name__ == '__main__':
    logger.info('Initializing Expoter')
    start_http_server(8082)
    logger.info('Expoter listening on 8082')
    REGISTRY.register(CapacityCollector())
    
    while True: 	time.sleep(10)


