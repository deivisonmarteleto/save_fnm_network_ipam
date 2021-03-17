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


class Get_Subnet:
    def __call__(self, _id=int):
        """ Coleta Subnet """
        _list = []
        for x in ipam.get(f'/sections/{_id}/subnets/'):
            if x['mask'] == 24 or  32 or  128:
               _list.append({'subnet':x['subnet'] + '/' + x['mask'], 'hop':NEXTHOP})
        return _list



class Get_Sections(Get_Subnet):
    def __call__(self):
        """ Coleta lista de ASN, HOP, ID """

        _list = []
        _get_subnet = Get_Subnet()
        _get_sections = ipam.get('/sections/')
        for x in _get_sections:
            _get_subnet = ipam.get(f'/sections/{x["id"]}/subnets/')
            for r in _get_subnet:
                if r['mask'] == 24 or  32 or  128:
                    _list.append({'asn':x['name'], 'net': r['subnet'] + '/'+r['mask'], 'hop': NEXTHOP_DEFAULT})
        return _list

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


class Get_Len(Get_Sections):
    def __call__(self):
        x = Get_Sections()
        return x().__len__()



class Find_Subnet:
    def __call__(self, net):
        try:
            subnet = net
            x = ipam.get(f'/subnets/search/{subnet}/')[0]
            return True

        except PhpIpamException as e:
            return False
          

class QueryIpamSub:
    def __call__(self, net):
        _list = []
        x = ipam.get(f'/subnets/search/{net}/')
        for r in x:
            res1 = r['sectionId']
            t = ipam.get(f'/sections/{res1}/')
            _list.append({'asn':t['name'], 'net': r['subnet'] + '/'+r['mask'], 'hop': NEXTHOP_DEFAULT })
        return _list





