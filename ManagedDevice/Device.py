'''
Created on 23 de dez de 2017

@author: lucas
'''
from pysnmp.hlapi import *
import time

class Device(object):
    '''
    classdocs
    '''
    
    def __init__(self, addr, community='public', version='2c'):
        self.addr = addr
        self.community = community
        self.version = version
        
    
    def _query(self, mod, obj, idx):
        if self.version == '1':
            query = getCmd(SnmpEngine(), 
                           CommunityData(self.community, mpModel=0), 
                           UdpTransportTarget(self.addr, 161), 
                           ContextData(),
                           ObjectType(ObjectIdentifier(mod, obj, idx),)
                          )
        elif self.version == '2c':
            query = getCmd(SnmpEngine(), 
                           CommunityData(self.community, mpModel=1), 
                           UdpTransportTarget(self.addr, 161), 
                           ContextData(),
                           ObjectType(ObjectIdentifier(mod, obj, idx))
                          )
        #TODO: SNMP versão 3
        errorIndication, errorStatus, errorIndex, varBinds = next(query)
        if errorIndication:
            raise (errorIndication)
        elif errorStatus:
            raise ('%s at %s' % (errorStatus.prettyPrint(), 
                                 errorIndex 
                                 and varBinds[int(errorIndex) - 1][0] or '?'))
        else:
            aux = str(varBinds[0])
            ret = aux.split(' = ', maxsplit=1)[1]
            return ret
    
    def queryDeviceData (self):
        ret = {
            'sysName': self._query('SNMPv2-MIB', 'sysName', 0), 
            'sysLocation': self._query('SNMPv2-MIB', 'sysLocation', 0)
        }
        return ret
    
    def queryDevice (self, idx, interval=5):
        ret = {
            'ifDescr' : self._query('IF-MIB', 'ifDescr', idx),
            'ifSpeed' : self._query('IF-MIB', 'ifSpeed', idx),
        }
        for obj in ('ifAdminStatus', 
                   'ifOperStatus', 
                   'ifInOctets', 
                   'ifOutOctets',
                   'ifInUcastPkts',
                   'ifInNUcastPkts',
                   'ifOutUcastPkts',
                   'ifOutNUcastPkts'
                   'ifInErrors',
                   'ifOutErrors',
                   'ifInDiscards',
                   'ifOutDiscards',
                   'ifOutQLen'):
            ret[obj][0] = self._query('IF-MIB', obj, idx)
        time.sleep(interval)
        for obj in ('ifAdminStatus', 
                   'ifOperStatus', 
                   'ifInOctets', 
                   'ifOutOctets',
                   'ifInUcastPkts',
                   'ifInNUcastPkts',
                   'ifOutUcastPkts',
                   'ifOutNUcastPkts'
                   'ifInErrors',
                   'ifOutErrors',
                   'ifInDiscards',
                   'ifOutDiscards',
                   'ifOutQLen'):
            ret[obj][1] = self._query('IF-MIB', obj, idx) 
        return ret