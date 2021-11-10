#!/usr/bin/python3
import json
import yaml
import cfg
import requests
import re
import time
from datetime import datetime
import logging
from requestToken import refresh_token

   
def get_domain_uuid(domain_name):
    for domain in cfg.all_domains_json:
        if domain['name'] == domain_name:
            return {'name': domain['name'], 'uuid': domain['uuid']}


def get_domain_name_by_uuid(uuid):
    for domain_data in cfg.all_domains_json:
        if domain_data.get('uuid') == uuid:
            return domain_data.get('name')


def check_token_status():
    time_now = time.time()
    auth_token_start = cfg.auth_token_start
    auth_token_lifetime = (time_now - auth_token_start)
    if auth_token_lifetime > 1750:
        fmc_ip = cfg.fmc_ip
        path = "/api/fmc_platform/v1/auth/refreshtoken"
        header = cfg.headers_json
        refresh_token(fmc_ip, path, header)
        pass
        cfg.headers_json = header
        cfg.auth_token_start = time.time()
        pass


def api_call_counter():
    """
    api_call_counter 
    FMC has limitations:
    429 Too Many Requests
    – Too many requests were sent to the API. This error will occur if you send more than 120 requests per minute.
    – Too many concurrent requests. The system cannot accept more than 10 parallel requests from all clients.
    – Too many write operations per server. The API will only allow one PUT, POST, or DELETE request per user on a server at a time.
    From <https://www.cisco.com/c/en/us/td/docs/security/firepower/623/api/REST/Firepower_Management_Center_REST_API_Quick_Start_Guide_623/Objects_in_the_REST_API.html> 
    
    api_call_counter throttle script in order to not exceed 120 api calls per minute
    global variable api_counter created in cfg.py (global init module)
    each module and function that create API call update api_counter within cfg module
    If amount of 120 API calls - the time.sleep timer occurs
    """
    current_time = time.time()
    cfg.api_counter += 1
    # logging.info(f'api call counter = {cfg.api_counter}')
    if cfg.api_counter < 119 and ((current_time - cfg.start_time) < 59):
        pass
    elif cfg.api_counter < 119 and ((current_time - cfg.start_time) > 60):
        # logging.info(f' {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Amount of API calls is {cfg.api_counter} but communication time is {current_time - cfg.start_time}. Clearing api_counter')
        cfg.api_counter = 1
        cfg.start_time = time.time()
    elif cfg.api_counter == 119 and ((current_time - cfg.start_time) < 60):
        logging.info(f' {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Amount of API calls is {cfg.api_counter} per minute is close to max per minute. Please wait for 60 seconds')
        time.sleep(60)
        cfg.api_counter = 1
        cfg.start_time = time.time()
    
        
        
def get_all_domains_data():
    """
    get all domains name and uuid and store them into json

    :return: json list of all domans and uuids
    :rtype: list()
    """
    domain_path = f"/api/fmc_platform/v1/info/domain"
    domains_names_uuid_raw = ''
    
    fmc_ip = cfg.fmc_ip
    headers_json = cfg.headers_json
           
    try:
        check_token_status()
        api_call_counter()
        resp = requests.get(
            f"https://{fmc_ip}{domain_path}", headers=headers_json, verify=False)
        logging.info(
            f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} all domains uuid request status Code: {str(resp.status_code)}\n')
        # time.sleep(0.7)
        if str(resp.status_code).startswith('2'):
            domains_names_uuid_raw = resp.text
        elif not str(resp.status_code).startswith('2'):
            errors_filename = 'outputs/errors.txt'
            with open(errors_filename, "a") as f:
                f.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Status code: {resp.status_code}\n Request.body: {resp.request.body}\n Request text: {resp.text}\n')
    except requests.exceptions.HTTPError as errh:
        logging.info(f'{errh}')
    except requests.exceptions.RequestException as err:
        logging.info(f'{err}')

    domains_names_uuid_json = json.loads(domains_names_uuid_raw).get('items')
    return domains_names_uuid_json


def get_all_objects_with_domains():
    """
    get_all_objects_with_domains 
    return all objects in dictionary:
        - all objects dict where key is object name, value is object data
    dictionary format: object_name: 
    """
    logging.info(f'\n {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Starting to work to get info of all hosts, all networks, all networkgroups\n')

    fmc_ip = cfg.fmc_ip
    headers_json = cfg.headers_json
    all_domains_json = cfg.all_domains_json
    all_obj_domain = cfg.all_obj_domain
    all_ids_domain = cfg.all_ids_domain
    
    system_objects = cfg.system_objects
    system_hosts = cfg.system_hosts
    system_networks = cfg.system_networks
    system_networkgroups = cfg.system_networkgroups

    all_obj_domain = {}
    all_ids_domain = {}

    obj_types = cfg.object_types
    
    offset_value = 0
    limit_value = 1000
    for domain_data in all_domains_json:
        tmp_hosts = {}
        tmp_ranges = {}
        tmp_networks = {}
        tmp_urls = {}
        tmp_networkgroups = {}
        tmp_urlgrps = {}
        tmp_ids = {}
        for obj_type in obj_types:
            objects_data = []
            check_token_status()
            api_call_counter()
            resp = requests.get(
                f"https://{fmc_ip}/api/fmc_config/v1/domain/{get_domain_uuid(domain_data.get('name'))['uuid']}/object/{obj_type}?expanded=true&offset={offset_value}&limit={limit_value}",
                headers=headers_json,
                verify=False)
            ''' below lines (raise_for_status()) are required for troubleshooting of REST API requests '''
            # time.sleep(0.7)
            logging.info(
                f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} get {obj_type} for {domain_data.get("name")} status code: {str(resp.status_code)}\n')
            if str(resp.status_code).startswith('2'):
                objects_data = json.loads(resp.text).get('items')
                try:
                    # offset_value += 1000
                    next_url = resp.json()['paging']['next'][0]
                except KeyError as error:
                    logging.info(
                        f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Reached end of pages for {obj_type} in {domain_data.get("name")}')
                    next_url = ''
                while next_url:
                    check_token_status()
                    api_call_counter()
                    resp = requests.get(next_url,
                                        headers=headers_json,
                                        verify=False)
                    # time.sleep(0.7)
                    if str(resp.status_code).startswith('2'):
                        # logging.info(f'{json.loads(resp.text)}')
                        objects_data += json.loads(resp.text).get('items')
                    try:
                        next_url = resp.json()['paging']['next'][0]
                    except KeyError as error:
                        logging.info(
                            f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Reached end of pages for {obj_type} in {domain_data.get("name")}')
                        next_url = ''
                if objects_data:
                    for obj in objects_data:
                        if obj.get('name') in system_objects:
                            continue
                        if check_if_object_already_exist(obj.get('name'), domain_data.get('name')):
                            continue
                        else:
                            all_ids = list()
                            if all_ids_domain:
                                for domain_key, ids_data in all_ids_domain.items():
                                    all_ids += list(ids_data)
                            if obj.get('id') in all_ids:
                                continue
                            else:
                                tmp_ids.update(
                                    {obj.get('id'): obj.get('name')})
                                if obj_type == 'hosts':
                                    if obj['name'] in system_hosts:
                                        continue
                                    tmp_hosts.update({obj['name']: obj})
                                elif obj_type == 'networks':
                                    if obj['name'] in system_networks:
                                        continue
                                    tmp_networks.update({obj['name']: obj})
                                elif obj_type == 'ranges':
                                    tmp_ranges.update({obj['name']: obj})
                                elif obj_type == 'urls':
                                    tmp_urls.update({obj['name']: obj})
                                elif obj_type == 'networkgroups':
                                    if obj['name'] in system_networkgroups:
                                        continue
                                    tmp_networkgroups.update(
                                        {obj['name']: obj})
                                elif obj_type == 'urlgroups':
                                    tmp_urlgrps.update({obj['name']: obj})
            else:
                logging.info(f' {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Object request has returned incorrect status code {resp.status_code}')
                continue
        all_obj_domain.update({domain_data.get('name'):  {
                              'hosts': tmp_hosts, 'ranges': tmp_ranges, 'networks': tmp_networks, 'urls': tmp_urls, 'networkgroups': tmp_networkgroups, 'urlgroups': tmp_urlgrps}})
        all_ids_domain.update({domain_data.get('name'): tmp_ids})
    # with open('outputs/all_obj_domain.yaml', 'w') as dest:
    #     yaml.SafeDumper.ignore_aliases = lambda *args: True
    #     yaml.safe_dump(all_obj_domain, dest, default_flow_style=False)
    logging.info(f'\n {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Finished collection from FMC of already present {", ".join(cfg.object_types)}\n')
    return all_obj_domain, all_ids_domain


def get_all_objects_for_domain(domain):
    """
    get_all_objects_with_domains [function to retrieve all objects]
    return all objects in dictionary:
        - all objects dict where key is object name, value is object data
    dictionary format: object_name: 
    """
    logging.info(f'\n {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Starting to work to get info of hosts, networks, networkgroups of domain {domain}\n')
        
    fmc_ip = cfg.fmc_ip
    headers_json = cfg.headers_json
    all_domains_json = cfg.all_domains_json
    all_ids_domain = cfg.all_ids_domain
    
    system_hosts = cfg.system_hosts
    system_networks = cfg.system_networks
    system_networkgroups = cfg.system_networkgroups

    offset_value = 0
    limit_value = 1000
    
    all_obj_per_domain = {}
    all_ids_per_domain = {}
    obj_types = cfg.object_types

    # domain_all_objects = {}
    tmp_hosts = {}
    tmp_ranges = {}
    tmp_networks = {}
    tmp_networkgroups = {}
    tmp_ids = {}
    tmp_urls = {}
    tmp_urlgrps = {}
    for obj_type in obj_types:
        objects_data = []
        check_token_status()
        api_call_counter()
        resp = requests.get(
            f"https://{fmc_ip}/api/fmc_config/v1/domain/{get_domain_uuid(domain)['uuid']}/object/{obj_type}?expanded=true&offset={offset_value}&limit={limit_value}",
            headers=headers_json,
            verify=False)
        logging.info(
            f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} get {obj_type} for {domain} status code: {str(resp.status_code)}\n')
        if str(resp.status_code).startswith('2'):
            objects_data = json.loads(resp.text).get('items')
            try:
                next_url = resp.json()['paging']['next'][0]
            except KeyError as error:
                logging.info(
                    f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Reached end of pages for {obj_type} in {domain}')
                next_url = ''
            while next_url:
                check_token_status()
                api_call_counter()
                resp = requests.get(next_url,
                                    headers=headers_json,
                                    verify=False)
                # time.sleep(0.7)
                if str(resp.status_code).startswith('2'):
                    # logging.info(f'{json.loads(resp.text)}')
                    objects_data += json.loads(resp.text).get('items')
                try:
                    next_url = resp.json()['paging']['next'][0]
                except KeyError as error:
                    logging.info(
                        f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Reached end of pages for {obj_type} in {domain}')
                    next_url = ''
            if objects_data:
                for obj in objects_data:
                    # if obj['name'] in list(all_objects):
                    if check_if_object_already_exist(obj.get('name'), domain):
                        continue
                    # if all_ids_per_domain:
                        # if obj.get('id') in list(all_ids_per_domain):
                        #     continue
                    all_ids_not_current_domain = list()
                    for domains_data_items in all_domains_json:
                        if domains_data_items.get('name') != domain:
                            if all_ids_domain.get(domains_data_items.get('name')):
                                all_ids_not_current_domain += list(all_ids_domain.get(domains_data_items.get('name')))
                    if obj.get('id') in all_ids_not_current_domain:
                        continue
                    else:
                        tmp_ids.update({obj.get('id'): obj.get('name')})
                        if obj_type == 'hosts':
                            if obj['name'] in system_hosts:
                                continue
                            tmp_hosts.update({obj['name']: obj})

                        if obj_type == 'ranges':
                            tmp_ranges.update({obj['name']: obj})

                        if obj_type == 'networks':
                            if obj['name'] in system_networks:
                                continue
                            tmp_networks.update({obj['name']: obj})
                        
                        if obj_type == 'urls':
                            tmp_urls.update({obj['name']: obj})
                            
                        if obj_type == 'networkgroups':
                            if obj['name'] in system_networkgroups:
                                continue
                            tmp_networkgroups.update({obj['name']: obj})
                        if obj_type == 'urlgroups':
                            tmp_urlgrps.update({obj['name']: obj})
        else:
            logging.info(
                f' {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Object request has returned incorrect status code {resp.status_code}')
            continue
        all_obj_per_domain.update({domain:  {'hosts': tmp_hosts, 'ranges': tmp_ranges,'networks': tmp_networks, 'urls': tmp_urls, 'networkgroups': tmp_networkgroups, 'urlgroups': tmp_urlgrps}})
        all_ids_per_domain.update({domain: tmp_ids})
    # with open('outputs/all_obj_domain.yaml', 'w') as dest, open('outputs/all_objects.yaml', 'w') as dest2:
    #     yaml.SafeDumper.ignore_aliases = lambda *args: True
    #     yaml.safe_dump(all_objects, dest2, default_flow_style=False)
    #     yaml.safe_dump(all_obj_domain, dest, default_flow_style=False)
    logging.info(f'\n {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Finished collection of info of all {", ".join(obj_types)}\n')
    return all_obj_per_domain, all_ids_per_domain


def get_all_objects_for_domain_no_check_ids(domain):
    """
    get_all_objects_with_domains [function to retrieve all objects]
    return all objects in dictionary:
        - all objects dict where key is object name, value is object data
    dictionary format: object_name: 
    """
    logging.info(
        f'\n {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Starting to work to get info of hosts, networks, networkgroups of domain {domain}\n')

    fmc_ip = cfg.fmc_ip
    headers_json = cfg.headers_json
    all_domains_json = cfg.all_domains_json
    all_ids_domain = cfg.all_ids_domain

    system_hosts = cfg.system_hosts
    system_networks = cfg.system_networks
    system_networkgroups = cfg.system_networkgroups

    offset_value = 0
    limit_value = 1000

    all_obj_per_domain = {}
    all_ids_per_domain = {}
    obj_types = cfg.object_types

    # domain_all_objects = {}
    tmp_hosts = {}
    tmp_ranges = {}
    tmp_networks = {}
    tmp_networkgroups = {}
    tmp_ids = {}
    tmp_urls = {}
    tmp_urlgrps = {}
    for obj_type in obj_types:
        objects_data = []
        check_token_status()
        api_call_counter()
        resp = requests.get(
            f"https://{fmc_ip}/api/fmc_config/v1/domain/{get_domain_uuid(domain)['uuid']}/object/{obj_type}?expanded=true&offset={offset_value}&limit={limit_value}",
            headers=headers_json,
            verify=False)
        logging.info(
            f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} get {obj_type} for {domain} status code: {str(resp.status_code)}\n')
        if str(resp.status_code).startswith('2'):
            objects_data = json.loads(resp.text).get('items')
            try:
                next_url = resp.json()['paging']['next'][0]
            except KeyError as error:
                logging.info(
                    f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Reached end of pages for {obj_type} in {domain}')
                next_url = ''
            while next_url:
                check_token_status()
                api_call_counter()
                resp = requests.get(next_url,
                                    headers=headers_json,
                                    verify=False)
                # time.sleep(0.7)
                if str(resp.status_code).startswith('2'):
                    # logging.info(f'{json.loads(resp.text)}')
                    objects_data += json.loads(resp.text).get('items')
                try:
                    next_url = resp.json()['paging']['next'][0]
                except KeyError as error:
                    logging.info(
                        f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Reached end of pages for {obj_type} in {domain}')
                    next_url = ''
            if objects_data:
                for obj in objects_data:
                    # if obj['name'] in list(all_objects):
                    # if check_if_object_already_exist(obj.get('name'), domain):
                    #     continue
                    # if all_ids_per_domain:
                        # if obj.get('id') in list(all_ids_per_domain):
                        #     continue
                    # all_ids_not_current_domain = list()
                    # for domains_data_items in all_domains_json:
                    #     if domains_data_items.get('name') != domain:
                    #         if all_ids_domain.get(domains_data_items.get('name')):
                    #             all_ids_not_current_domain += list(
                    #                 all_ids_domain.get(domains_data_items.get('name')))
                    # if obj.get('id') in all_ids_not_current_domain:
                    #     continue
                    # else:
                    tmp_ids.update({obj.get('id'): obj.get('name')})
                    if obj_type == 'hosts':
                        if obj['name'] in system_hosts:
                            continue
                        tmp_hosts.update({obj['name']: obj})

                    if obj_type == 'ranges':
                        tmp_ranges.update({obj['name']: obj})

                    if obj_type == 'networks':
                        if obj['name'] in system_networks:
                            continue
                        tmp_networks.update({obj['name']: obj})

                    if obj_type == 'urls':
                        tmp_urls.update({obj['name']: obj})

                    if obj_type == 'networkgroups':
                        if obj['name'] in system_networkgroups:
                            continue
                        tmp_networkgroups.update({obj['name']: obj})
                    if obj_type == 'urlgroups':
                        tmp_urlgrps.update({obj['name']: obj})
        else:
            logging.info(
                f' {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Object request has returned incorrect status code {resp.status_code}')
            continue
        all_obj_per_domain.update({domain:  {'hosts': tmp_hosts, 'ranges': tmp_ranges, 'networks': tmp_networks,
                                  'urls': tmp_urls, 'networkgroups': tmp_networkgroups, 'urlgroups': tmp_urlgrps}})
        all_ids_per_domain.update({domain: tmp_ids})
    # with open('outputs/all_obj_domain.yaml', 'w') as dest, open('outputs/all_objects.yaml', 'w') as dest2:
    #     yaml.SafeDumper.ignore_aliases = lambda *args: True
    #     yaml.safe_dump(all_objects, dest2, default_flow_style=False)
    #     yaml.safe_dump(all_obj_domain, dest, default_flow_style=False)
    logging.info(
        f'\n {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Finished collection of info of all {", ".join(obj_types)}\n')
    return all_obj_per_domain, all_ids_per_domain



def get_all_groups_info():
    """
    get_all_groups_info retrieve all networkgroups details
    return all groups information in dictionary:
        - all objects dict where key is object name, value is object data
    dictionary format: object_name: 
    """
    logging.info(f'\n {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Starting to work to get detailed information of all networkgroups\n')
    fmc_ip = cfg.fmc_ip
    headers_json = cfg.headers_json
   
    obj_type = 'networkgroups'
    groups_per_domain = {}
    for domain_name, object_types in cfg.all_obj_domain.items():
        temp_groups = {}
        for networkgroup, networkgroup_data in object_types.get(obj_type).items():
            if networkgroup in cfg.system_networkgroups:
                continue
            objects_data = []
            check_token_status()
            api_call_counter()
            resp = requests.get(f"https://{fmc_ip}/api/fmc_config/v1/domain/{get_domain_uuid(domain_name)['uuid']}/object/{obj_type}/{networkgroup_data['id']}",
                                headers=headers_json,
                                verify=False)
            logging.info(f' {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Grab info {obj_type} {networkgroup} for {domain_name} status code: {str(resp.status_code)}\n')
            # time.sleep(0.7)
            if str(resp.status_code).startswith('2'):
                objects_data = json.loads(resp.text)
            elif str(resp.status_code) == '404':
                # del all_obj_domain[domain_name][{obj_type}][networkgroup]
                del cfg.all_detailed_networkgroups[domain_name][networkgroup]
            if objects_data:
                if objects_data.get('name') in cfg.system_networkgroups:
                    continue
                elif objects_data.get('overridable') == True:
                    continue
                if cfg.all_ids_domain.get(domain_name):
                    if objects_data.get('id') in list(cfg.all_ids_domain.get(domain_name)):
                        temp_groups.update({objects_data.get('name'): objects_data})
        groups_per_domain.update({domain_name: temp_groups})

    logging.info(f'\n {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Finished collection of info details of all networkgroups\n')
    # with open('outputs/all_networkgroups_detailed.yaml', 'w') as dest:
    #     yaml.SafeDumper.ignore_aliases = lambda *args: True
    #     yaml.safe_dump(groups_per_domain, dest, default_flow_style=False)
    return groups_per_domain


def get_all_detailed_groups_for_domain(domain_name):
    """
    get_all_detailed_groups_for_domain [function to retrieve detailed info of networkgroups in domain]
    return all objects in dictionary:
        - all objects dict where key is object name, value is object data
    dictionary format: object_name: 
    """
    logging.info(f'\n {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Starting to work to get detailed info of networkgroups for domain {domain_name}\n')
    fmc_ip = cfg.fmc_ip
    headers_json = cfg.headers_json
    obj_type = 'networkgroups'
    detailed_groups_per_domain = {}
    temp_networkgroups = dict()
        
    for networkgroup, networkgroup_data in cfg.all_obj_domain.get(domain_name).get(obj_type).items():
        
        if networkgroup in cfg.system_networkgroups:
            continue
        objects_data = []
        check_token_status()
        api_call_counter()
        resp = requests.get(f"https://{fmc_ip}/api/fmc_config/v1/domain/{get_domain_uuid(domain_name)['uuid']}/object/{obj_type}/{networkgroup_data['id']}",
                            headers=headers_json,
                            verify=False)
        logging.info(f' {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Grab info {obj_type} {networkgroup} for {domain_name} status code: {str(resp.status_code)}\n')
        # time.sleep(0.7)
        if str(resp.status_code).startswith('2'):
            objects_data = json.loads(resp.text)
        
        if objects_data:
            if objects_data.get('name') in cfg.system_networkgroups:
                continue
            elif objects_data.get('overridable') == True:
                continue
            all_ids_not_current_domain = list()
            for domains_data_items in cfg.all_domains_json:
                if domains_data_items.get('name') != domain_name:
                    if cfg.all_ids_domain.get(domains_data_items.get('name')):
                        all_ids_not_current_domain += list(cfg.all_ids_domain.get(domains_data_items.get('name')))
            if objects_data.get('id') in all_ids_not_current_domain:
                continue
            else:
                temp_networkgroups.update({objects_data.get('name'): objects_data})

    detailed_groups_per_domain.update({domain_name: temp_networkgroups})
    # with open('outputs/all_obj_domain.yaml', 'w') as dest, open('outputs/all_objects.yaml', 'w') as dest2:
    #     yaml.SafeDumper.ignore_aliases = lambda *args: True
    #     yaml.safe_dump(all_objects, dest2, default_flow_style=False)
    #     yaml.safe_dump(cfg.all_obj_domain, dest, default_flow_style=False)
    logging.info(f'\n {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Finished collection of networkgroups detailed info for {domain_name}\n')
    return detailed_groups_per_domain


def get_all_devices():
    """
    get_all_devices retrieve all devices present in FMC

    :return: dictionary with devices names as dictionary
    :rtype: dict
    """
    fmc_ip = cfg.fmc_ip
    headers_json = cfg.headers_json
    global_domain_uuid = cfg.global_domain_uuid
    offset_value = 0
    limit_value = 1000
    
    all_devices_dict = {}
    check_token_status()
    api_call_counter()
    resp = requests.get(
        f"https://{fmc_ip}/api/fmc_config/v1/domain/{global_domain_uuid}/devices/devicerecords?offset={offset_value}&limit={limit_value}",
        headers=headers_json,
        verify=False)
    logging.info(
        f' {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} get all devices list status code: {str(resp.status_code)}\n')
    if str(resp.status_code).startswith('2'):
        # objects_data = json.loads(resp.text).get('items')
        objects_data = json.loads(resp.text).get('items')
        try:
            next_url = resp.json()['paging']['next'][0]
        except KeyError as error:
            logging.info(
                f' {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Reached end of pages for devices')
            next_url = ''
        while next_url:
            check_token_status()
            api_call_counter()
            resp = requests.get(next_url,
                                headers=headers_json,
                                verify=False)
            if str(resp.status_code).startswith('2'):
                objects_data += json.loads(resp.text).get('items')
                try:
                    next_url = resp.json()['paging']['next'][0]
                except KeyError as error:
                    logging.info(f' {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Reached end of pages for devices in domain {global_domain_uuid}')
                    next_url = ''
        if objects_data:
            for obj in objects_data:
                all_devices_dict.update({obj['name']: obj})
    elif not str(resp.status_code).startswith('2'):
        errors_filename = 'outputs/errors.txt'
        with open(errors_filename, "a") as f:
            f.write(f' {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Status code: {resp.status_code}\n Request.body: {resp.request.body}\n Request text: {resp.text}\n')
    return all_devices_dict


# def check_object_type(object_name):
#     OBJECT_HOST_NAME_START = cfg.OBJECT_HOST_NAME_START
#     OBJECT_RANGE_NAME_START = cfg.OBJECT_RANGE_NAME_START
#     OBJECT_SUBNET_NAME_START = cfg.OBJECT_SUBNET_NAME_START
#     OBJECT_GROUP_NAME_START = cfg.OBJECT_GROUP_NAME_START

#     match = re.search(
#         r'(.+?(?=\.))',
#         object_name)
#     if match:
#         match = match.group().upper()
#         if match == OBJECT_HOST_NAME_START.replace('.',''):
#             return 'host'
#         elif match == OBJECT_SUBNET_NAME_START.replace('.', ''):
#             return 'network'
#         elif match == OBJECT_RANGE_NAME_START.replace('.', ''):
#             return 'range'
#         elif match == OBJECT_GROUP_NAME_START.replace('.', ''):
#             return 'networkgroup'
#     else:
#         logging.info(f' {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} object {object_name} is not named according to naming convention in constants.py. Please use naming rules.')
#         return False


def check_if_object_already_exist(obj_name, domain):
    if obj_name in cfg.system_objects:
        return True
    if cfg.all_obj_domain:
        for object_type in cfg.object_types:
            # object_type = check_object_type(obj_name)
            if cfg.all_obj_domain[domain][object_type].get(obj_name):
                return True


def convert_domain_name(raw_domain_name):
    match = re.sub(r'\s+\\\s+', r'/', raw_domain_name)
    if match:
        return match


def get_object_data(obj_name, domain):
    if obj_name in cfg.system_objects:
        return False
    # global all_obj_domain
    if cfg.all_obj_domain:
        for object_type in cfg.object_types:
            if cfg.all_obj_domain[domain][object_type].get(obj_name):
                return (obj_name, cfg.all_obj_domain[domain][object_type].get(obj_name))
