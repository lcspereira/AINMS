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
        
        return ret