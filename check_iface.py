'''
Created on 9 de mar de 2018

@author: lucas
'''
from pysnmp.hlapi import *
from pysnmp.error import *
import time
import csv
import sys
import os
import socket

def query (addr, port, comm, obj, idx):
    query = getCmd(SnmpEngine(), 
                    CommunityData(comm, mpModel=1), 
                    UdpTransportTarget((addr, port)), 
                    ContextData(),
                    ObjectType(ObjectIdentity('IF-MIB', obj, idx))
            )
    errorIndication, errorStatus, errorIndex, varBinds = next(query)
    if errorIndication:
        raise (errorIndication)
    elif errorStatus:
        raise ('%s at %s' % (errorStatus.prettyPrint(), 
                            errorIndex 
                            and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        aux_val = str(varBinds[0])
        ret = aux_val.split(' = ', maxsplit=1)[1]
        try:
            aux = int(ret)
        except ValueError:
            ret = 0
        finally:
            return ret


addr = sys.argv[0]
port = sys.argv[1]
comm = sys.argv[2]
poll = sys.argv[3]

try:
    print ("Consultado dispositivo " + ip + "...")
    num_ifaces = query(ip, port, comm, 'ifNumber', 0)
    for iface in range(1, int(num_ifaces)):
        res = []
        aux = {}
        if query(ip, port, comm, 'ifAdminStatus', iface) == 'up' and query(ip, comm, 'ifOperStatus', iface) == 'up':
            for obj in ('ifInOctets',
                    'ifOutOctets',
                    'ifInUcastPkts',
                    'ifInNUcastPkts',
                    'ifOutUcastPkts',
                    'ifOutNUcastPkts',
                    'ifInErrors',
                    'ifOutErrors',
                    'ifInDiscards',
                    'ifOutDiscards'):
                aux[obj] = []
                aux[obj].append (query(ip, port, comm, obj, iface))
            time.sleep(poll)

            for obj in ('ifInOctets',
                    'ifOutOctets',
                    'ifInUcastPkts',
                    'ifInNUcastPkts',
                    'ifOutUcastPkts',
                    'ifOutNUcastPkts',
                    'ifInErrors',
                    'ifOutErrors',
                    'ifInDiscards',
                    'ifOutDiscards'):
                aux[obj].append (query(ip, port, comm, obj, iface))

            aux['ifSpeed'] = query(ip, port, comm, 'ifSpeed', iface)
            res.append (float(aux['ifSpeed']))
            res.append ((((float (aux['ifInOctets'][1]) - float(aux['ifInOctets'][0])) + (float(aux['ifOutOctets'][1]) - float (aux['ifOutOctets'][0])) / 5) * 8))
            #TODO: Não faz sentido array para erros, ucastpkts e descartes
            try:
                res.append (float(aux['ifInErrors'][1]) / (float(aux['ifInUcastPkts'][1]) + float(aux['ifInNUcastPkts'][1])))
                res.append (float(aux['ifOutErrors'][1]) / (float(aux['ifOutUcastPkts'][1]) + float(aux['ifOutNUcastPkts'][1])))
                res.append (float(aux['ifInDiscards'][1]) / (float(aux['ifInUcastPkts'][1]) + float(aux['ifInNUcastPkts'][1])))
                res.append (float(aux['ifOutDiscards'][1]) / (float(aux['ifOutUcastPkts'][1]) + float(aux['ifOutNUcastPkts'][1])))
                #TODO: Transmitir os dados à rede neural
            except ZeroDivisionError:
                pass
        else:
            print ("Interface " + str(iface) + " não está operacional.")
except Exception as ex:
    print (str(ex))
    pass