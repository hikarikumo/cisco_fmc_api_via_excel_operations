#!/usr/bin/python3
import cfg
import json
import requests
from datetime import datetime
import logging
from get_func import get_domain_uuid, get_domain_name_by_uuid, api_call_counter, check_token_status


def post_network_objects(domain_data, domains_uuid):
    fmc_ip = cfg.fmc_ip
    headers_json = cfg.headers_json
          
    logging.info(f'\n {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Starting to add network objects in domain {get_domain_name_by_uuid(domains_uuid)}\n')
    try:
        check_token_status()
        api_call_counter()
        resp = requests.post(
            f"https://{fmc_ip}/api/fmc_config/v1/domain/{domains_uuid}/object/networks?bulk=true",
            headers=headers_json, data=json.dumps(domain_data), verify=False)
        # time.sleep(0.7)
        # logging.info(f'request_body:\n{resp.request.body}')
        # logging.info(f'Headers: {str(resp.headers)}\n')
        # logging.info(f'Text: {str(resp.text)}\n')
        logging.info(
            f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Network objects add operation in domain {get_domain_name_by_uuid(domains_uuid)} status Code: {str(resp.status_code)}\n')
        if not str(resp.status_code).startswith('2'):
            errors_filename = 'outputs/errors.txt'
            with open(errors_filename, "a") as f:
                f.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  Status code: {resp.status_code}\n Request.body: {resp.request.body}\n Request text: {resp.text}\n')
    except requests.exceptions.HTTPError as errh:
        logging.info(f'{errh}')
        raise SystemExit(errh)
    except requests.exceptions.RequestException as err:
        logging.info(f'{err}')
        raise SystemExit(err)
    logging.info(f'\n{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Finished adding network objects in domain {get_domain_name_by_uuid(domains_uuid)}\n')


def post_range_objects(domain_data, domains_uuid):
    fmc_ip = cfg.fmc_ip
    headers_json = cfg.headers_json

    logging.info(f'\n {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Starting to add range objects in domain {get_domain_name_by_uuid(domains_uuid)}\n')
    try:
        check_token_status()
        api_call_counter()
        resp = requests.post(
            f"https://{fmc_ip}/api/fmc_config/v1/domain/{domains_uuid}/object/ranges?bulk=true",
            headers=headers_json, data=json.dumps(domain_data), verify=False)
        # time.sleep(0.7)
        # logging.info(f'request_body:\n{resp.request.body}')
        # logging.info(f'Headers: {str(resp.headers)}\n')
        # logging.info(f'Text: {str(resp.text)}\n')
        logging.info(
            f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} range objects add operation in domain {get_domain_name_by_uuid(domains_uuid)} status Code: {str(resp.status_code)}\n')
        if not str(resp.status_code).startswith('2'):
            errors_filename = 'outputs/errors.txt'
            with open(errors_filename, "a") as f:
                f.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  Status code: {resp.status_code}\n Request.body: {resp.request.body}\n Request text: {resp.text}\n')
    except requests.exceptions.HTTPError as errh:
        logging.info(f'{errh}')
        raise SystemExit(errh)
    except requests.exceptions.RequestException as err:
        logging.info(f'{err}')
        raise SystemExit(err)
    logging.info(f'\n{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Finished adding range objects in domain {get_domain_name_by_uuid(domains_uuid)}\n')


def post_host_objects(domain_data, domains_uuid):
    fmc_ip = cfg.fmc_ip
    headers_json = cfg.headers_json

    logging.info(f'\n {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Starting to add host objects in domain {get_domain_name_by_uuid(domains_uuid)}\n')
    try:
        check_token_status()
        api_call_counter()
        resp = requests.post(
            f"https://{fmc_ip}/api/fmc_config/v1/domain/{domains_uuid}/object/hosts?bulk=true",
            headers=headers_json, data=json.dumps(domain_data), verify=False)
        # time.sleep(0.7)
        # logging.info(f'request_body:\n{resp.request.body}')
        # logging.info(f'Headers: {str(resp.headers)}\n')
        # logging.info(f'Text: {str(resp.text)}\n')
        logging.info(f' {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Host objects add operation in domain {get_domain_name_by_uuid(domains_uuid)} status Code: {str(resp.status_code)}\n')
        if not str(resp.status_code).startswith('2'):
            errors_filename = 'outputs/errors.txt'
            with open(errors_filename, "a") as f:
                f.write(
                    f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Status code: {resp.status_code}\n Request.body: {resp.request.body}\n Request text: {resp.text}\n')
    except requests.exceptions.HTTPError as errh:
        logging.info(f'{errh}')
        raise SystemExit(errh)
    except requests.exceptions.RequestException as err:
        logging.info(f'{err}')
        raise SystemExit(err)
    logging.info(f'\n{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Finished adding host objests in domain {get_domain_name_by_uuid(domains_uuid)}\n')


def post_url_objects(domain_data, domains_uuid):
    fmc_ip = cfg.fmc_ip
    headers_json = cfg.headers_json
          
    logging.info(f'\n {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Starting to add url objects in domain {get_domain_name_by_uuid(domains_uuid)}\n')
    try:
        check_token_status()
        api_call_counter()
        resp = requests.post(
            f"https://{fmc_ip}/api/fmc_config/v1/domain/{domains_uuid}/object/urls?bulk=true",
            headers=headers_json, data=json.dumps(domain_data), verify=False)
        # time.sleep(0.7)
        # logging.info(f'request_body:\n{resp.request.body}')
        # logging.info(f'Headers: {str(resp.headers)}\n')
        # logging.info(f'Text: {str(resp.text)}\n')
        logging.info(
            f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Url objects add operation in domain {get_domain_name_by_uuid(domains_uuid)} status Code: {str(resp.status_code)}\n')
        if not str(resp.status_code).startswith('2'):
            errors_filename = 'outputs/errors.txt'
            with open(errors_filename, "a") as f:
                f.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  Status code: {resp.status_code}\n Request.body: {resp.request.body}\n Request text: {resp.text}\n')
    except requests.exceptions.HTTPError as errh:
        logging.info(f'{errh}')
        raise SystemExit(errh)
    except requests.exceptions.RequestException as err:
        logging.info(f'{err}')
        raise SystemExit(err)
    logging.info(f'\n{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Finished adding url objects in domain {get_domain_name_by_uuid(domains_uuid)}\n')


def post_groups_objects(domain_data, domain_uuid):
    fmc_ip = cfg.fmc_ip
    headers_json = cfg.headers_json

    logging.info(f'\n {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Starting to add POST group in domain {get_domain_name_by_uuid(domain_uuid)}\n')
    try:
        check_token_status()
        api_call_counter()
        resp = requests.post(
            f"https://{fmc_ip}/api/fmc_config/v1/domain/{domain_uuid}/object/networkgroups?bulk=true",
            headers=headers_json, data=json.dumps(domain_data), verify=False)
        # time.sleep(0.7)
        logging.info(
            f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} POST group ADD status Code: {str(resp.status_code)}\n')
        if not str(resp.status_code).startswith('2'):
            errors_filename = 'outputs/errors.txt'
            with open(errors_filename, "a") as f:
                f.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Status code: {resp.status_code}\n Request.body: {resp.request.body}\n Request text: {resp.text}\n')
    except requests.exceptions.HTTPError as errh:
        logging.info(f'{errh}')
        raise SystemExit(errh)
    except requests.exceptions.RequestException as err:
        logging.info(f'{err}')
        raise SystemExit(err)
    logging.info(f'\n{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Finished adding POST group in domain {get_domain_name_by_uuid(domain_uuid)}"\n')


def post_urlgroups_objects(domain_data, domain_uuid):
    fmc_ip = cfg.fmc_ip
    headers_json = cfg.headers_json

    logging.info(
        f'\n {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Starting to add POST group in domain {get_domain_name_by_uuid(domain_uuid)}\n')
    try:
        check_token_status()
        api_call_counter()
        resp = requests.post(
            f"https://{fmc_ip}/api/fmc_config/v1/domain/{domain_uuid}/object/urlgroups?bulk=true",
            headers=headers_json, data=json.dumps(domain_data), verify=False)
        # time.sleep(0.7)
        logging.info(
            f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} POST urlgroup ADD status Code: {str(resp.status_code)}\n')
        if not str(resp.status_code).startswith('2'):
            errors_filename = 'outputs/errors.txt'
            with open(errors_filename, "a") as f:
                f.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Status code: {resp.status_code}\n Request.body: {resp.request.body}\n Request text: {resp.text}\n')
    except requests.exceptions.HTTPError as errh:
        logging.info(f'{errh}')
        raise SystemExit(errh)
    except requests.exceptions.RequestException as err:
        logging.info(f'{err}')
        raise SystemExit(err)
    logging.info(
        f'\n{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Finished adding POST urlgroup in domain {get_domain_name_by_uuid(domain_uuid)}\n')


def del_groups(group_data, domain_name):
    fmc_ip = cfg.fmc_ip
    headers_json = cfg.headers_json
        
    logging.info(f'\n {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Starting to DEL  groups in domain {domain_name}\n')
    object_type = group_data['type']
    group_id = group_data['id']
    domain_uuid = get_domain_uuid(domain_name)['uuid']
    try:
        check_token_status()
        api_call_counter()
        resp = requests.delete(
            f"https://{fmc_ip}/api/fmc_config/v1/domain/{domain_uuid}/object/networkgroups/{group_id}",
            headers=headers_json, verify=False)
        # time.sleep(0.7)
        # logging.info(f'Text: {str(resp.text)}\n')
        logging.info(
            f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} DEL group {group_data["name"]} status Code: {str(resp.status_code)}\n')
        if not str(resp.status_code).startswith('2'):
            errors_filename = 'outputs/errors.txt'
            with open(errors_filename, "a") as f:
                f.write(
                    f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Status code: {resp.status_code}\n Request.body: {resp.request.body}\n Request text: {resp.text}\n')
        elif str(resp.status_code).startswith('2'):
            del cfg.all_obj_domain[domain_name][object_type][group_data['name']]
            del cfg.all_detailed_networkgroups[domain_name][group_data['name']]
    except requests.exceptions.HTTPError as errh:
        logging.info(f'{errh}')
        raise SystemExit(errh)
    except requests.exceptions.RequestException as err:
        logging.info(f'{err}')
        raise SystemExit(err)
    logging.info(f'\n {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Finished to DEL groups in domain {domain_name}\n')


def del_urlgroups(group_data, domain_name):
    fmc_ip = cfg.fmc_ip
    headers_json = cfg.headers_json

    logging.info(
        f'\n {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Starting to DEL urlgroups in domain {domain_name}\n')
    object_type = group_data['type']
    group_id = group_data['id']
    domain_uuid = get_domain_uuid(domain_name)['uuid']
    try:
        check_token_status()
        api_call_counter()
        resp = requests.delete(
            f"https://{fmc_ip}/api/fmc_config/v1/domain/{domain_uuid}/object/{object_type.lower()}s/{group_id}",
            headers=headers_json, verify=False)
        # time.sleep(0.7)
        # logging.info(f'Text: {str(resp.text)}\n')
        logging.info(
            f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} DEL urlgroup {group_data["name"]} status Code: {str(resp.status_code)}\n')
        if not str(resp.status_code).startswith('2'):
            errors_filename = 'outputs/errors.txt'
            with open(errors_filename, "a") as f:
                f.write(
                    f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Status code: {resp.status_code}\n Request.body: {resp.request.body}\n Request text: {resp.text}\n')
        elif str(resp.status_code).startswith('2'):
            del cfg.all_obj_domain[domain_name][f'{object_type.lower()}s'][group_data['name']]
    except requests.exceptions.HTTPError as errh:
        logging.info(f'{errh}')
        raise SystemExit(errh)
    except requests.exceptions.RequestException as err:
        logging.info(f'{err}')
        raise SystemExit(err)
    logging.info(
        f'\n {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Finished to DEL urlgroups in domain {domain_name}\n')


def put_networkgroups(group_data, domain_name):
    fmc_ip = cfg.fmc_ip
    headers_json = cfg.headers_json

    logging.info(f'\n {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Starting to modify PUT group in domain {domain_name}\n')
    group_id = group_data['id']
    domain_uuid = get_domain_uuid(domain_name)['uuid']
    try:
        check_token_status()
        api_call_counter()
        resp = requests.put(
            f"https://{fmc_ip}/api/fmc_config/v1/domain/{domain_uuid}/object/networkgroups/{group_id}",
            headers=headers_json, data=json.dumps(group_data), verify=False)
        # time.sleep(0.7)
        # logging.info(f'Text: {str(resp.text)}\n')
        logging.info(
            f' {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} PUT group {group_data["name"]} modify operation status Code: {str(resp.status_code)}\n')
        if not str(resp.status_code).startswith('2'):
            errors_filename = 'outputs/errors.txt'
            with open(errors_filename, "a") as f:
                f.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Status code: {resp.status_code}\n Request.body: {resp.request.body}\n Request text: {resp.text}\n')
    except requests.exceptions.HTTPError as errh:
        logging.info(f'{errh}')
        raise SystemExit(errh)
    except requests.exceptions.RequestException as err:
        logging.info(f'{err}')
        raise SystemExit(err)
    logging.info(f'\n {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Finished to modify PUT group in domain {domain_name}\n')


def put_urlgroups(group_data, domain_name):
    fmc_ip = cfg.fmc_ip
    headers_json = cfg.headers_json

    logging.info(
        f'\n {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Starting to modify PUT urlgroup in domain {domain_name}\n')
    group_id = group_data['id']
    domain_uuid = get_domain_uuid(domain_name)['uuid']
    try:
        check_token_status()
        api_call_counter()
        resp = requests.put(
            f"https://{fmc_ip}/api/fmc_config/v1/domain/{domain_uuid}/object/urlgroups/{group_id}",
            headers=headers_json, data=json.dumps(group_data), verify=False)
        # time.sleep(0.7)
        # logging.info(f'Text: {str(resp.text)}\n')
        logging.info(
            f' {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} PUT urlgroup {group_data["name"]} modify operation status Code: {str(resp.status_code)}\n')
        if not str(resp.status_code).startswith('2'):
            errors_filename = 'outputs/errors.txt'
            with open(errors_filename, "a") as f:
                f.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Status code: {resp.status_code}\n Request.body: {resp.request.body}\n Request text: {resp.text}\n')
        
    except requests.exceptions.HTTPError as errh:
        logging.info(f'{errh}')
        raise SystemExit(errh)
    except requests.exceptions.RequestException as err:
        logging.info(f'{err}')
        raise SystemExit(err)
    logging.info(
        f'\n {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Finished to modify PUT urlgroup in domain {domain_name}\n')


def put_object(object_data, domain_uuid):
    fmc_ip = cfg.fmc_ip
    headers_json = cfg.headers_json
    all_obj_domain = cfg.all_obj_domain
  
    logging.info(f'\n {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Starting to modify PUT object in domain {get_domain_name_by_uuid(domain_uuid)}\n')
    object_id = object_data['id']
    
    # object_type = check_object_type(object_data.get('name'))
    object_type = object_data.get('type')
    # domain_uuid = get_domain_uuid(domain_name)['uuid']
    try:
        check_token_status()
        api_call_counter()
        resp = requests.put(
            f"https://{fmc_ip}/api/fmc_config/v1/domain/{domain_uuid}/object/{object_type}s/{object_id}",
            headers=headers_json, data=json.dumps(object_data), verify=False)
        # time.sleep(0.7)
        # logging.info(f'Text: {str(resp.text)}\n')
        logging.info(
            f' {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} PUT object {object_data["name"]} modify operation status Code: {str(resp.status_code)}\n')
        if not str(resp.status_code).startswith('2'):
            errors_filename = 'outputs/errors.txt'
            with open(errors_filename, "a") as f:
                f.write(
                    f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Status code: {resp.status_code}\n Request.body: {resp.request.body}\n Request text: {resp.text}\n')
        elif str(resp.status_code).startswith('2'):
            tmp_object_data = all_obj_domain[get_domain_name_by_uuid(domain_uuid)][f'{object_type}s'][object_data.get('name')]
            if object_data.get('value'):
                tmp_object_data.update({'value': object_data.get('value')})
            elif object_data.get('url'):
                tmp_object_data.update({'url': object_data.get('url')})
            cfg.all_obj_domain[get_domain_name_by_uuid(domain_uuid)][f'{object_type}s'][object_data.get('name')].update({object_data.get('name'): tmp_object_data})
    except requests.exceptions.HTTPError as errh:
        logging.info(f'{errh}')
        raise SystemExit(errh)
    except requests.exceptions.RequestException as err:
        logging.info(f'{err}')
        raise SystemExit(err)
    logging.info(f'\n {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Finished to modify PUT object in domain {get_domain_name_by_uuid(domain_uuid)}\n')


def del_objects(object_data, domain_name):
    fmc_ip = cfg.fmc_ip
    headers_json = cfg.headers_json
    
    logging.info(f'\n {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Starting to DEL objects in domain {domain_name}\n')
    # obj_id = all_devices[object_data['name']]['id']
    obj_id = object_data['id']
    api_obj_type = f"{object_data['type'].lower()}s"
    try:
        uuid = get_domain_uuid(domain_name)['uuid']
    except TypeError as error:
        logging.info(
            f'Domain {domain_name} do not exist either on FMC, either in Excel sheet')
        errors_filename = 'outputs/errors.txt'
        with open(errors_filename, "a") as f:
            f.write(
                f'Domain {domain_name} do not exist either on FMC, either in Excel sheet\n Error: {error}\n')

    try:
        check_token_status()
        api_call_counter()
        resp = requests.delete(
            f"https://{fmc_ip}/api/fmc_config/v1/domain/{uuid}/object/{api_obj_type}/{obj_id}",
            headers=headers_json,
            # data=json.dumps(domain_data),
            verify=False)
        # time.sleep(0.7)
        # logging.info(f'resp.request.body')
        # logging.info(f'Headers: {str(resp.headers)}')
        # logging.info(f'Text: {str(resp.text)}')
        logging.info(
            f' {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} DEL object {object_data["name"]} in domain {domain_name} status code: {str(resp.status_code)}')
        if not str(resp.status_code).startswith('2'):
            errors_filename = 'outputs/errors.txt'
            with open(errors_filename, "a") as f:
                f.write(
                    f'Status code: {resp.status_code}\n Request.body: {resp.request.body}\n Request text: {resp.text}\n')
        elif str(resp.status_code).startswith('2'):
            del cfg.all_obj_domain[domain_name][api_obj_type][object_data['name']]
        # elif str(resp.status_code).startswith('4'):
        #     del cfg.all_obj_domain[domain_name][api_obj_type][object_data['name']]
    except requests.exceptions.HTTPError as errh:
        logging.info(f'{errh}')
        raise SystemExit(errh)
    except requests.exceptions.RequestException as err:
        logging.info(f'{err}')
        raise SystemExit(err)
    logging.info(f'\n {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Finished to DEL objects in domain {domain_name}\n')
