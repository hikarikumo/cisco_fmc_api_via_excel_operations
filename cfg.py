#!/usr/bin/python3
from pathlib import Path
import yaml
import requestToken as token # requestToken is function from another file requestToken.py (should be in the same folder)
import getpass
# import constants  # constants import from the separate file constants.py
import time
# from datetime import datetime
import logging


logging.basicConfig(format='%(threadName)s %(name)s %(levelname)s: %(message)s',level=logging.INFO)


fmc_ip = str()
auth_header = dict()
headers_json = dict()
global_domain_uuid = dict()
all_domains_json = dict()
all_obj_domain = dict()
all_ids_domain = dict()
all_devices = dict()
all_detailed_networkgroups = dict()
system_hosts = list()
system_networks = list()
system_networkgroups = list()
system_objects = list()
system_ports = list()
object_types = list()
start_time = float()
api_counter = int()
auth_token_start = float()
input_xlsx = str()
output_xlsx = str()
output_acp_xlsx = str()
diff_before_filename = str()
diff_after_filename = str()
sorted_sheets = list()

# OBJECT_HOST_NAME_START = constants.object_host
# OBJECT_SUBNET_NAME_START = constants.object_subnet
# OBJECT_RANGE_NAME_START = constants.object_range
# OBJECT_GROUP_NAME_START = constants.object_group


def init():
    ''' Set global variables to access FMC and its credentials'''
    global fmc_ip
    global auth_header
    global headers_json
    global global_domain_uuid

    global system_hosts
    global system_networks
    global system_networkgroups
    global system_objects
    global system_ports
    global object_types
    
    global start_time
    global api_counter
    global auth_token_start
    
    global all_domains_json
    global all_obj_domain
    global all_ids_domain
    global all_devices
    global all_detailed_networkgroups
    
    global input_xlsx
    global output_xlsx
    global diff_before_filename
    global diff_after_filename
    global output_acp_xlsx
    
    global sorted_sheets
    
    fmc_ip = str()
    headers_json = dict()
    auth_header = dict()
    auth_token_path = "/api/fmc_platform/v1/auth/generatetoken"
    
    input_xlsx = 'FMC_objects.xlsx'
    output_xlsx = 'FMC_downloaded_objects.xlsx'
    output_acp_xlsx = 'FMC_ACP_rules_downloaded.xlsx'
    diff_before_filename = 'outputs/diff_before_FMC_objects'
    diff_after_filename = 'outputs/diff_after_FMC_objects'
    
    start_time = time.time()
    auth_token_start = time.time()
    api_counter = 0
    
    
    if Path('fmc_credentials.yaml').is_file():
        credentials_vars_file = 'fmc_credentials.yaml'
        credentials_vars = read_credentials(credentials_vars_file)
        fmc_ip = credentials_vars['fmc_ip']
        ''' call the token generating function and populate our header '''
        auth_header = token.get_token(
            credentials_vars['fmc_ip'],
            auth_token_path,
            credentials_vars['username'],
            credentials_vars['password'],
            
        )
    else:
        fmc_ip = input('enter FMC ip address: ')
        username = input('enter api username: ')
        password = getpass.getpass(prompt='enter api password: ')
        ''' call the token generating function and populate our header '''
        auth_header = token.get_token(
            fmc_ip,
            auth_token_path,
            username,
            password
        )
    # else:
    #     logging.info(f'no input file {input_xlsx} found ')
    #     raise FileNotFoundError(
    #         errno.ENOENT, os.strerror(errno.ENOENT), input_xlsx)
    
    system_hosts = ['any-ipv6']
    system_networks = ['any-ipv4',
                       'IPv4-Benchmark-Tests',
                       'IPv4-Link-Local',
                       'IPv4-Multicast',
                       'IPv4-Private-10.0.0.0-8',
                       'IPv4-Private-172.16.0.0-12',
                       'IPv4-Private-192.168.0.0-16',
                       'IPv6-IPv4-Mapped',
                       'IPv6-Link-Local',
                       'IPv6-Private-Unique-Local-Addresses',
                       'IPv6-to-IPv4-Relay-Anycast']
    system_networkgroups = ['IPv4-Private-All-RFC1918', 'any']
    system_ports = ['AOL',
                    'Bittorrent',
                    'DNS_over_TCP',
                    'DNS_over_UDP',
                    'FTP',
                    'HTTP',
                    'HTTPS',
                    'IMAP',
                    'LDAP',
                    'NFSD-TCP',
                    'NFSD-UDP',
                    'NTP-TCP',
                    'NTP-UDP',
                    'POP-2',
                    'POP-3',
                    'RADIUS',
                    'RIP',
                    'SIP',
                    'SMTP',
                    'SMTPS',
                    'SNMP',
                    'SSH',
                    'SYSLOG',
                    'TCP_high_ports',
                    'TELNET',
                    'TFTP',
                    'YahooMessenger_Voice_Chat_TCP',
                    'YahooMessenger_Voice_Chat_UDP',
                    'Yahoo_Messenger_Messages', ]
    
    system_objects = list()
    system_objects += system_hosts
    system_objects += system_networks
    system_objects += system_networkgroups

    object_types = [
        'hosts', 'ranges', 'networks', 'urls', 'networkgroups', 'urlgroups']
    headers_json = {"Accept": "application/json", "Content-Type": "application/json",
                    "X-auth-access-token": auth_header['X-auth-access-token'],
                    "X-auth-refresh-token": auth_header['X-auth-refresh-token']}

    global_domain_uuid = auth_header['DOMAIN_UUID']


def check_if_file_exist(filename):
    if Path(filename).is_file():
        return True
    else:
        return False

def read_credentials(credentials_yaml_file):
    with open(credentials_yaml_file) as src:
        credentials = yaml.safe_load(src)
    return credentials


if __name__ == "__main__":
    init()
