from django.test import TestCase

# Create your tests here.
import pymysql
import pandas as pd
import numpy as np
import os
path = 'D:/NWE/Molding_Manufacture_planning/test_sys/backend/data/'
name = 'daily_emergency_20200109'

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='tony1234',
                             db='planning_test')

cursor = connection.cursor()
df = pd.read_csv(path+name + '.csv')
cols = df.columns.tolist()
subset = df[cols]
tuples = [tuple(x) for x in subset.to_numpy()]

sql = "INSERT INTO `emergency` (`PN`, `tons`, `name`, `UPH`, `demand`, `work_time`, `color`, `mold_number`, `delivery`, `notes`)\
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

for t in tuples:
  cursor.execute(sql, t)
  connection.commit()

