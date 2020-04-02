import pandas as pd
import numpy as np
import pymongo

date = '20200326'
path = 'D:/NWE/Molding_Manufacture_planning/formal_sys/backend/data/'
name = 'planning_result_20200326'
df = pd.read_csv(path + name + '.csv')

machine_list = []
order_list = []
temp_name = 'A01透明'

for i, m in enumerate(df['機台號']):
  demand = str(df['數量'][i])
  work_time = str(df['生產時間'][i])
  order_dic = {
    'PN': df['鴻海料號'][i], 
    'name': df['品名'][i], 
    'start_time': df['起始時間'][i], 
    'end_time': df['結束時間'][i], 
    'demand': demand, 
    'work_time': work_time
  }
  if temp_name == m:
    order_list.append(order_dic)
  else:
    temp_name = m
    temp_dic = {
      'date': date,
      'order': order_list
    }
    machine_list.append(temp_dic)
    order_list = []
    order_list.append(order_dic)

machine_name = ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15']

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["MoldingMachines"]
print(machine_list)

for i, m in enumerate(machine_name):
  mycol = mydb[m]
  mycol.insert_one(machine_list[i])
