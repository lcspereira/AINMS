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
import csv

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
test_arr = []


try:
    print ("Consultado dispositivo " + addr + "...")
    num_ifaces = query(addr, port, comm, 'ifNumber', 0)
    for iface in range(1, int(num_ifaces)):
        res = []
        aux = {}
        test_arr = []
        ifAdminStatus = query(addr, port, comm, 'ifAdminStatus', iface)
        ifOperStatus  = query(addr, port, comm, 'ifOperStatus', iface)
        
        if ifAdminStatus == "up" and ifOperStatus == "up":
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
            #res.append ((((((float (aux['ifInOctets'][1]) - float(aux['ifInOctets'][0])) + (float(aux['ifOutOctets'][1]) - float (aux['ifOutOctets'][0])) / poll) * 8)) / float (aux['ifSpeed'])) * 100)
            res.append (((float(aux['ifInOctets'][1]) - float(aux['ifInOctets'][0])) * 8 * 100) / (poll * float(aux['ifSpeed'])))
            res.append (((float(aux['ifOutOctets'][1]) - float(aux['ifOutOctets'][0])) * 8 * 100) / (poll * float(aux['ifSpeed'])))
            #TODO: Não faz sentido array para erros, ucastpkts e descartes
            try:
                res.append(((float(aux['ifInErrors'][1]) - float(aux['ifInErrors'][0])) * 100) / (
                            (float(aux['ifInUcastPkts'][1]) - float(aux['ifInUcastPkts'][0])) + (
                                float(aux['ifInNUcastPkts'][1]) - float(aux['ifInNUcastPkts'][0]))))

                res.append(((float(aux['ifOutErrors'][1]) - float(aux['ifOutErrors'][0])) * 100) / (
                        (float(aux['ifInUcastPkts'][1]) - float(aux['ifInUcastPkts'][0])) + (
                        float(aux['ifInNUcastPkts'][1]) - float(aux['ifInNUcastPkts'][0]))))

                res.append(((float(aux['ifInDiscards'][1]) - float(aux['ifInDiscards'][0])) * 100) / (
                            (float(aux['ifInUcastPkts'][1]) - float(aux['ifInUcastPkts'][0])) + (
                                float(aux['ifInNUcastPkts'][1]) - float(aux['ifInNUcastPkts'][0]))))

                res.append(((float(aux['ifOutDiscards'][1]) - float(aux['ifOutDiscards'][0])) * 100) / (
                        (float(aux['ifInUcastPkts'][1]) - float(aux['ifInUcastPkts'][0])) + (
                        float(aux['ifInNUcastPkts'][1]) - float(aux['ifInNUcastPkts'][0]))))

                sock = socket.socket (socket.AF_UNIX, socket.SOCK_STREAM)
                sock.connect ("/tmp/ainms.sock")
                data = np.array(res)
                test_arr = data.tolist()
                serialized_data = pickle.dumps ([data])
                sock.sendall (serialized_data)
                data = sock.recv (5192)
                test_arr.append (pickle.loads(data)[0][0])
                print (test_arr)
                with open("if_test_data.csv", 'a') as csv_arq:
                    writer = csv.writer(csv_arq)
                    writer.writerow (test_arr)
                sock.close()
            except ZeroDivisionError:
                pass
        else:
            print ("Interface " + str(iface) + " não está operacional. (" + str(ifAdminStatus) + ", " + str(ifOperStatus) + ")")
except Exception as ex:
    raise (ex)