#!/usr/bin/python

"""

Openstack expoter to monitor Openstack capacity using garafana prometheus

"""
import yaml
import logging
import logging.handlers
import requests
import json
import sys

from novaclient import client as nova_client
from cinderclient import client as cinder_client
from os import environ as env

from urllib3 import disable_warnings
disable_warnings()


# Initiating STDOUT log handler
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s:%(levelname)s:  %(message)s")
logger = logging.getLogger(__name__)


config = None
ENM_Tenants = env['ENM_Tenants'].strip('\"').split( )
OTHER_Tenants   = env['OTHER_Tenants'].strip('\"').split( )



def get_creds_dict(*names):
    return  {name: env['OS_%s' % name.upper()]
        for name in names if 'OS_%s' % name.upper() in env}


def get_clients():
    from keystoneauth1.identity import v3
    from keystoneauth1 import session

#    log_header("Authenticating Openstack")
    ks_creds_admin = get_creds_dict(
        "username", "password", "user_domain_name", "auth_url",
        "project_domain_name", "project_name", "project_domain_id", "project_id")
    
    auth_admin = v3.Password(**ks_creds_admin)
    sess       = session.Session(auth=auth_admin, verify=False)

    token      = sess.get_token()
    nova       = nova_client.Client(2, session=sess)
    cinder     = cinder_client.Client(3, session=sess)


    return (token, nova, cinder)


def get_url(url,headers):
    r = requests.get(url, headers=headers,verify=False)
    return r



def conv_mb_to_gb(input_mb):
    gb = 1.0/1024
    convert_gb = gb * input_mb
    return round(convert_gb)


def _cinder_limits(token,url):
    headers = {
        'X-Auth-Token' : token,
        'Content-type' : 'application/json'
    }
    response = get_url(url,headers).json()
    return response

def _ks_project_list(token, url):
    endpoint_url = url + '/projects'
    headers = {
        'X-Auth-Token' : token,
        'Content-type' : 'application/json'
    }
    response = get_url(endpoint_url,headers)
    return response


def list_projects():
    token, nova, cinder = get_clients()
    # This should auto fetch from openstack
    allowed_projects = ENM_Tenants + OTHER_Tenants
    _dict = {}
    _list = []
    tenants = _ks_project_list(token, get_creds_dict('auth_url')['auth_url'] ).json()
    for tenant in tenants['projects']:
        if tenant['name'] in allowed_projects:
            _dict = {
                'id' : str(tenant['id']),
                'name': str(tenant['name'])
            }
            _list.append(_dict)
    return _list

def convert_gen_to_dict(object):
    l = list(object)
    _dict = dict(map(lambda x: (x.name, x.value), l))
    return _dict



def _get_enm_tenants_count():
    return len(ENM_Tenants)
