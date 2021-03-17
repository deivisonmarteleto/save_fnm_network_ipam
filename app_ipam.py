#!/usr/bin/python3


import sys
import logging
import json 
import time
from phpipam_client import PhpIpamClient, GET, PATCH, PhpIpamException
from datetime import datetime


#API
ipam = PhpIpamClient(
                    url='http://127.0.0.1:8080',
                    app_id='app',
                    token='SiabDO7F4sJwcQn6p_Iu-dHWh5E5in6l',
                    username='api_user',
                    password='temp2010',
                    encryption=False,
                    )

#VARIAVEL
NEXTHOP_DEFAULT = '10.1.0.2'


class SectionsSubnet:
    def __call__(self):
        """ Query Subnet / mask and ASN """

        _list = []
        on_sections = ipam.get('/sections/')
        for x in on_sections:
            on_subnet = ipam.get(f'/sections/{x["id"]}/subnets/')
            for r in on_subnet:
               _list.append({'asn': x['name'], 'net': r['subnet'] + '/'+r['mask'], 'hop': NEXTHOP_DEFAULT})
        return _list


         

class QueryIpamSub:
    def __call__(self, net):
        _list = []
        x = ipam.get(f'/subnets/search/{net}/')
        for r in x:
            res1 = r['sectionId']
            t = ipam.get(f'/sections/{res1}/')
            _list.append({'asn':t['name'], 'net': r['subnet'] + '/'+r['mask'], 'hop': NEXTHOP_DEFAULT })
        return _list





