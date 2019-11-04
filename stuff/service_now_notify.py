#!/usr/bin/env python
# Service NOW

import sys
import requests
from requests.auth import HTTPBasicAuth
from cmk.notification_plugins import utils

def main():
    """
    Main part to sendout notification
    """
    context = utils.collect_context()

    api_url = context['PARAMETER_1']
    auth_user = context['PARAMETER_2']
    auth_password = context['PARAMETER_3']

    proxies = {}
    if 'PARAMETER_4' in context:
        proxies['https'] = context['PARAMETER_4']

    auth = HTTPBasicAuth(auth_user, auth_password)

    host_name = context['HOSTNAME']
    site_name = context['OMD_SITE']
    contacts = context['CONTACTS']
    service_account = site_name
    event_time = context['MICROTIME']
    long_plugin_output = ""

    if context['NOTIFICATIONTYPE'] == "PROBLEM":
        api_url += "checkmk/incident/create"
        if context['WHAT'] == "HOST":
            mngmt_pack = {
                "hostname": host_name,
                "contacts" : contacts,
                }
            source_id = "{}|{}".format(site_name, host_name)
            serverity = context['HOSTNAME']
            plugin_output = context['HOSTOUTPUT']
        else:
            service_name = context['SERVICEDESC']
            mngmt_pack = {
                "hostname": host_name,
                "servicename" : service_name,
                "contacts" : contacts,
                }
            source_id = "{}|{}|{}".format(site_name, host_name, service_name)
            serverity = context['SERVICESTATE']
            plugin_output = context['SERVICEOUTPUT']

        payload = {
            "QUELLE" : "Checkmk",
            "QUELLEID": source_id,
            "ZIEL" : "ServiceNow",
            "FUNKTION" : "create",
            "FQDN" : host_name,
            "MP" : mngmt_pack,
            "SERVERITY" : serverity,
            "DIENSTKONTO" : service_account,
            "EVENTZEITPUNKT" : event_time,
            "KURZBESCHREIBUNG" : plugin_output,
            "LANGBESCHREIBUNG" : long_plugin_output,
        }
    elif context['NOTIFICATIONTYPE'] == "RECOVERY":
        api_url += "checkmk/incident/close"
        if context['WHAT'] == "HOST":
            source_id = "{}|{}".format(site_name, host_name)
        else:
            service_name = context['SERVICEDESC']
            source_id = "{}|{}|{}".format(site_name, host_name, service_name)

        payload = {
            "QUELLEID": source_id,
            "ZIEL" : "ServiceNow",
            "ZIELID" : "TBD",
            "FUNKTION" : "close"
        }


    response = requests.post(api_url, json=payload, auth=auth, proxies=proxies)
    if response.status_code != 200:
        print(response.json())
        sys.exit(2)
    sys.exit(0)

main()
