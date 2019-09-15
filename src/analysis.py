# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 14:57:24 2019

@author: Joshua
"""

import json
import pandas as pd

class FixedlenList(list):
	'''
subclass from list, providing all features list has
the list size is fixed. overflow items will be discarded
	
	'''
	def __init__(self,l=0):
		super(FixedlenList,self).__init__()
		self.__length__=l #fixed length
		
	def pop(self,index=-1):
		super(FixedlenList, self).pop(index)
	
	def remove(self,item):
		self.__delitem__(item)
		
	def __delitem__(self,item):
		super(FixedlenList, self).__delitem__(item)
		#self.__length__-=1	
		
	def append(self,item):
		if len(self) >= self.__length__:
			super(FixedlenList, self).pop(0)
		super(FixedlenList, self).append(item)		
	
	def extend(self,aList):
		super(FixedlenList, self).extend(aList)
		self.__delslice__(0,len(self)-self.__length__)

	def insert(self):
		pass



pathname = 'C:\\Users\Joshua\Downloads\commute.json'
with open(pathname, 'r') as f:
    data = json.load(f)
    
pd.DataFrame.from_dict(data).groupby('name').get_group('steering_wheel_angle').plot(kind='line',x='timestamp',y='value',figsize=(25,15))



def process(x,memory):
    """
        updates memory based on inputs
        memory stores: weighted acc ped average, weighted speed average, 
                       latitude, longitude, Th history, dTh/dt history
    """
    r = 0.5
    if x['name'] == 'accelerator_pedal_position':
        memory['acc'] = r*x['value'] + (1-r)*memory['acc']
    elif x['name'] == 'vehicle_speed':
        memory['speed'] = r*x['value'] + (1-r)*memory['speed']
    elif x['name'] == 'latitude':
        memory['latitude'] = x['value']
    elif x['name'] == 'longitude':
        memory['longitude'] = x['value']
    elif x['name'] == 'steering_wheel_angle':
        if len(memory['Th']) > 0:
            memory['dTh'].append(x['value'] - memory['Th'][-1])
        memory['Th'].append(x['value'])


def calculate(memory):
    """
    calculate risk factor based on memory
    """
    ThThr = 15
    dThThr = 250
    dTh = 0
    
    if memory['speed'] > 20 and sum(memory['dTh']) > dThThr:
        print(memory['speed'])
        return True
    
    x = [max(0,abs(i+50)-ThThr) for i in memory['Th']]
    Th = len([i for i in range(len(x)-1) if (memory['Th'][i] == 0) & (memory['Th'][i+1] > 0) ])
    if Th > 5:
        print(Th)
        return True  
    return False
        
period = 0
for point in data:
    if point['name'] == 'steering_wheel_angle':
        if period == 0:
            period = point['timestamp']
        else:
            period = point['timestamp'] - period
            break

memory = {'acc': 0, 'speed': 0, 'latitude': 0, 'longitude': 0, 'Th': FixedlenList(int(50/period)), 'dTh': FixedlenList(int(0.3/period))}


for point in data:
    process(point,memory)
    calculate(memory)
    #if calculate(memory):
    #    print(True)
    



        




"""
df = pd.DataFrame.from_dict(data)
grouped = df.sort_values(by = ['name','timestamp']).groupby('name')
for name, group in grouped:
    if name in ['accelerator_pedal_position','vehicle_speed','steering_wheel_angle']:
        group[['time_change','steering_change']] = group[['timestamp','value']].astype(float).diff()

{'accelerator_pedal_position',
 'brake_pedal_status',
 'door_status',
 'engine_speed',
 'fine_odometer_since_restart',
 'fuel_consumed_since_restart',
 'fuel_level',
 'headlamp_status',
 'high_beam_status',
 'ignition_status',
 'latitude',
 'longitude',
 'odometer',
 'parking_brake_status',
 'powertrain_torque',
 'steering_wheel_angle',
 'transmission_gear_position',
 'vehicle_speed',
 'windshield_wiper_status'}
"""