#!/usr/bin/python3

from app_ipam import SectionsSubnet, QueryIpamSub
from app_mongo import MongoSave, MongoQuerySubnet, MongoUpade, MongoFindPrefix, MongoDropPrefix
import sys
import logging
import os
import subprocess
import sched
import time



#VARIAVEL
LOG_FILE_DIR = '/home/deivison/Dropbox/jobs/projeto_fnm/bin/app_gravar.log'
FILE_NETWORK = '/home/deivison/Dropbox/jobs/projeto_fnm/bin/network_list'
LOG_LEVEL = logging.INFO


logging.basicConfig(level = LOG_LEVEL, filename = LOG_FILE_DIR, format='%(asctime)s:%(lineno)d - %(message)s')


scheduler = sched.scheduler(time.time,  
                            time.sleep)


def query_subnet_ipam():
    list_subnet_ipam = []
    on_subnet_ipam = SectionsSubnet()
    for x in on_subnet_ipam():
        list_subnet_ipam.append(x['net'])
    return list_subnet_ipam


def query_subnet_mongo():
    list_subnet_mongo = []
    on_subnet_mongo = MongoQuerySubnet()
    for x in on_subnet_mongo():
        list_subnet_mongo.append(x)
    return list_subnet_mongo

def on_save_mongo(dados=dict):
    collection = 'customer'
    save_mongo = MongoSave()
    save_mongo(collection, dados)
    

def on_save_file():
    x = query_subnet_ipam()
    _list = []
    for z in x:
        _list.append(z + '\n')
    with open(FILE_NETWORK, 'w+') as f:
        f.writelines(_list)
        f.truncate()
    subprocess.call("service fastnetmon restart", shell=True)
    logging.info('save in networs_list and restart fastnetmon')

def drop_subnet_mongo(subnet):
    drop_mongo = MongoDropPrefix()
    return drop_mongo(subnet)


def main():
    try:
        scheduler.enter(delay=30, priority=0, action=main)
        r1 =  query_subnet_mongo()
        r2 = query_subnet_ipam()
        s1 = list(set(r2) ^ set(r1))
        if len(s1) == 0:
            logging.info('no differences between db ipam and mongo!')
        if len(s1) >= 1:
            s2 = list(set(r2) - set(r1))
            s3 = list(set(r1) - set(r2))
            if len(s3) == 0:
                logging.info('no differences from db mongo to Ipam!')
            if len(s3) >= 1:
                for x in s3:
                    logging.info(f'there is inconsistency in the db mongo, removed the subnet: {x}')
                    drop_subnet_mongo(x)
                on_save_file()       
            if len(s2) == 0:
                logging.info('no differences from db Ipam to Mongo!') 
            if len(s2) >= 1:
                for z in s2:
                    subneting_ipam = QueryIpamSub()
                    for y in subneting_ipam(z):
                        on_save_mongo(y)
                        logging.info(f'Savo a rede {y} mongo!')
                on_save_file()
        else:
            logging.warning("None action matched with consts")
    except Exception as e:
        logging.critical(str(e))
        
main()


scheduler.run(blocking=True) 


