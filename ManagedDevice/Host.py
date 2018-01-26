'''
Created on 16 de jan de 2018

@author: lucas
'''
import ManagedDevice.Device

class Host(ManagedDevice.Device):
    '''
    classdocs
    '''
    def __init__(self, addr, ports, community='public', version='2c'):
        super().__init__(addr, community, version)
        self.ports = ports
        
    def queryDevice (self, interval=5):
        ret = []
        for port in self.ports: 
            ret.append (super().queryDevice(port, interval))
        for obj in ('tcpMaxConn', 
                   'tcpCurrEstab', 
                   'tcpAttemptFails', 
                   'tcpEstabResets',
                   'tcpRetransSegs',
                   'tcpInErrs',
                   'tcpOutRsts'):
            ret.append(super()._query('TCP-MIB', obj, 0))
        for obj in ('udpNoPorts',
                   'udpInErrors', 
                   'tcpAttemptFails', 
                   'tcpEstabResets',
                   'tcpRetransSegs',
                   'tcpInErrs',
                   'tcpOutRsts'):
            ret.append(super()._query('UDP-MIB', obj, 0))
        return ret