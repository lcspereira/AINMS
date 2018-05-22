'''
Created on 9 de mar de 2018

@author: lucas
'''
from pysnmp.hlapi import *
from pysnmp.error import *
import time
import csv

def query (addr, comm, obj, idx):
    query = getCmd(SnmpEngine(), 
                    CommunityData(comm, mpModel=1), 
                    UdpTransportTarget((addr, 161)), 
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
    return ret


for oct in range (0, 255):
    ip = '192.168.' + str(oct) + '.253'
    try:
        print ("Consultado dispositivo " + ip + "...")
        num_ifaces = query(ip, 'public', 'ifNumber', 0)
        for iface in range(1, int(num_ifaces)):
            res = []
            aux = {}
            if query(ip, 'public', 'ifAdminStatus', iface) == 'up' and query(ip, 'public', 'ifOperStatus', iface) == 'up':
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
                    aux[obj].append (query(ip, 'public', obj, iface))
                time.sleep(5)

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
                    aux[obj].append (query(ip, 'public', obj, iface))

                aux['ifSpeed'] = query(ip, 'public', 'ifSpeed', iface)
                res.append (float(aux['ifSpeed']))
                #res.append ((((float (aux['ifInOctets'][1]) - float(aux['ifInOctets'][0])) + (float(aux['ifOutOctets'][1]) - float (aux['ifOutOctets'][0])) / 5) * 8))
                res.append ((float(aux['ifInOctets'][1]) - float(aux['ifInOctets'][0])) / (
                #TODO: Não faz sentido array para erros, ucastpkts e descartes
                try:
                    res.append (float(aux['ifInErrors'][1]) / (float(aux['ifInUcastPkts'][1]) + float(aux['ifInNUcastPkts'][1])))
                    res.append (float(aux['ifOutErrors'][1]) / (float(aux['ifOutUcastPkts'][1]) + float(aux['ifOutNUcastPkts'][1])))
                    res.append (float(aux['ifInDiscards'][1]) / (float(aux['ifInUcastPkts'][1]) + float(aux['ifInNUcastPkts'][1])))
                    res.append (float(aux['ifOutDiscards'][1]) / (float(aux['ifOutUcastPkts'][1]) + float(aux['ifOutNUcastPkts'][1])))
                    with open('c:\\train.csv', 'a') as arq:
                        writer = csv.writer(arq)
                        writer.writerow (res)
                        print (res)
                except ZeroDivisionError:
                    pass
                except Exception:
                    try:
                        res.append (float(aux['ifInErrors'][1]) / float(aux['ifInUcastPkts'][1]))
                        res.append (float(aux['ifOutErrors'][1]) / float(aux['ifOutUcastPkts'][1]))
                        res.append (float(aux['ifInDiscards'][1]) / float(aux['ifInUcastPkts'][1]))
                        res.append (float(aux['ifOutDiscards'][1]) / float(aux['ifOutUcastPkts'][1]))
                        with open('c:\\train.csv', 'a') as arq:
                            writer = csv.writer(arq)
                            writer.writerow(res)
                            print (res)
                    except ZeroDivisionError:
                        pass
            else:
                print ("Interface " + str(iface) + " não está operacional.")
    except Exception as ex:
        print (str(ex))
        pass