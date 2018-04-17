'''
Created on 9 de mar de 2018

@author: lucas
'''
from pysnmp.hlapi import *
import time
import csv
import sys
import os
import socket
import pickle
import numpy as np

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
            if ret == "No Such Instance currently exists at this OID":
                ret = 0
        finally:
            return ret


addr = sys.argv[1]
port = sys.argv[2]
comm = sys.argv[3]
poll = int(sys.argv[4])

try:
    print ("Consultado dispositivo " + addr + "...")
    num_ifaces = query(addr, port, comm, 'ifNumber', 0)
    for iface in range(1, int(num_ifaces)):
        res = []
        aux = {}

        ifAdminStatus = query(addr, port, comm, 'ifAdminStatus', iface)
        ifOperStatus  = query(addr, port, comm, 'ifOperStatus', iface)
        
        if ifAdminStatus == "'up'" and ifOperStatus == "'up'":
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
                aux[obj].append (query(addr, port, comm, obj, iface))
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
                aux[obj].append (query(addr, port, comm, obj, iface))

            aux['ifSpeed'] = query(addr, port, comm, 'ifSpeed', iface)
            res.append ((((((float (aux['ifInOctets'][1]) - float(aux['ifInOctets'][0])) + (float(aux['ifOutOctets'][1]) - float (aux['ifOutOctets'][0])) / poll) * 8)) / float (aux['ifSpeed'])) * 100)
            #TODO: Não faz sentido array para erros, ucastpkts e descartes
            try:
                res.append ((float(aux['ifInErrors'][1]) / (float(aux['ifInUcastPkts'][1]) + float(aux['ifInNUcastPkts'][1]))) * 100)
                res.append ((float(aux['ifOutErrors'][1]) / (float(aux['ifOutUcastPkts'][1]) + float(aux['ifOutNUcastPkts'][1]))) * 100)
                res.append ((float(aux['ifInDiscards'][1]) / (float(aux['ifInUcastPkts'][1]) + float(aux['ifInNUcastPkts'][1]))) * 100)
                res.append ((float(aux['ifOutDiscards'][1]) / (float(aux['ifOutUcastPkts'][1]) + float(aux['ifOutNUcastPkts'][1]))) * 100)
                #TODO: Transmitir os dados à rede neural
                sock = socket.socket (socket.AF_UNIX, socket.SOCK_STREAM)
                sock.connect ("/tmp/ainms.sock")
                data = np.array(res)
                serialized_data = pickle.dumps (data)
                sock.sendall (serialized_data)
                data = sock.recv (5192)
                print (pickle.loads(data))
                sock.close()
            except ZeroDivisionError:
                pass
        else:
            print ("Interface " + str(iface) + " não está operacional. (" + str(ifAdminStatus) + ", " + str(ifOperStatus) + ")")
except Exception as ex:
    raise (ex)