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
    
def distance(loc1,loc2):
    dy = (loc1[1] - loc2[1])/69 
    dx = (lat[0]-lat[0])/53
    return (dx**2+dy**2)**0.5

class Driver(object):
    def __init__(self,period):
        self.loc = [0,0]
        self.speed = 0
        self.Th = FixedlenList(int(50/period))
        self.dTh = FixedlenList(int(0.3/period))
        
    def update(self,x):
        """
            updates memory based on inputs
            memory stores: weighted acc ped average, weighted speed average, 
                           latitude, longitude, Th history, dTh/dt history
        """
        if x['name'] == 'vehicle_speed':
            self.speed = x['value']
        elif x['name'] == 'latitude':
            self.loc[1] = x['value']
        elif x['name'] == 'longitude':
            self.loc[0] = x['value']
        elif x['name'] == 'steering_wheel_angle':
            if len(self.Th) > 0:
                self.dTh.append(x['value'] - self.Th[-1])
            self.Th.append(x['value'])
    
    
    def unsafe(self):
        """
        determine whether driver is safe based on current state
        """
        ThThr = 15
        dThThr = 250
        
        if memory['speed'] > 25 and sum(memory['dTh']) > dThThr:
            print(memory['speed'])
            return True
        
        x = [max(0,abs(i+50)-ThThr) for i in memory['Th']]
        Th = len([i for i in range(len(x)-1) if (memory['Th'][i] == 0) & (memory['Th'][i+1] > 0) ])
        if Th > 5:
            print(Th)
            return True  
        return False
    
    def ping(self,cars):
        """
        determine which cars to ping if car is unsafe
        """
        if self.unsafe():
            dist = 10 * self.speed/3600
            for car in cars:
                if distance(car.loc,driver.loc) < dist:
                    send_ping(car)
    
def send_ping(car):
    """
    tell the server to send the other car a message?
    """
    car







pathname = 'C:\\Users\Joshua\Downloads\commute.json'
with open(pathname, 'r') as f:
    data = json.load(f)

"""
for actual app, set period to period of json inputs
"""        
period = 0
for point in data:
    if point['name'] == 'steering_wheel_angle':
        if period == 0:
            period = point['timestamp']
        else:
            period = point['timestamp'] - period
            break

memory = {'acc': 0, 'speed': 0, 'latitude': 0, 'longitude': 0, 'Th': FixedlenList(int(50/period)), 'dTh': FixedlenList(int(0.3/period))}
    
pd.DataFrame.from_dict(data).groupby('name').get_group('steering_wheel_angle').plot(kind='line',x='timestamp',y='value',figsize=(25,15))

car = Driver(period)
for point in data:
    car.update(point)
    car.unsafe()
    



        

