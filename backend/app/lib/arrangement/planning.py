import pandas as pd
import numpy as np
import os
import datetime
from molding import *
from setting import *
import math
from identification import Identification

Id = Identification()

class Planning():
    def __init__(self, total_weekly_planning):
        self.total_weekly_planning = total_weekly_planning
        self.record_ordered_part_number = []
        self.buffer_list = []
        self.urgent = False
        self.release = False
        self.buffer = False
        self.bind_machine = None
        self.if_stop = False
        self.mold_change = True
        self.plastic_change = True

    def planning(self, order):

        # Get fitted machine
        machine_chosen = self.find_fitted_machine(order)
                       
        if machine_chosen == None: # No machine available for this order
            return False

        # Time calculation
        start_time, end_time, time_needed = self.time_calculation(order, machine_chosen)
        
        # Put into order
        newOrder = Order(order['鴻海料號'], order['品名'], math.ceil(time_needed*order['產能']), math.ceil(time_needed*order['產能']), \
                         order['產能'], start_time, end_time, start_time, end_time, time_needed, urgent_tag=self.urgent)
        if self.release == True:
            machine_chosen.order_list.insert(1, newOrder)
            self.record_ordered_part_number.append(newOrder.part_number)
            self.release = False # release off
        else:
            machine_chosen.order_list.append(newOrder)
            self.record_ordered_part_number.append(newOrder.part_number)

        # Reset default status
        self.bind_machine = None
        self.mold_change = True
        self.plastic_change = True

        return True

    def find_fitted_machine(self, order):

        tons = order['噸位']
        color = order['顏色']

        # Find fittable machine
        machine_chosen_list = []
        machine_chosen = None
        
        #-1 Condition 1: Yesterday delayed
        if self.bind_machine:
            return self.bind_machine

        #-2 Condition 2: Buffer mode
        if self.buffer:
            buffer_machine_list = []
            for line in Factory_NWE.line_list:
                temp_list = line.get_zero_remaining_time()
                temp_list = line.get_machine_by_tons(tons, machine_list=temp_list)
                buffer_machine_list = buffer_machine_list + line.get_machine_by_color(color, machine_list=temp_list)

            if len(buffer_machine_list) > 0:
                for machine_chosen in buffer_machine_list:
                    if machine_chosen.order_list[-1].planning_time == 0:
                        continue
                    else:
                        return machine_chosen
                return None
            else:
                return None

        #-3 Condition 3: Normal
        for line in Factory_NWE.line_list:
            temp_list = line.get_ok_machine() # step 1: check if machines are able to be used
            temp_list = line.get_machine_by_tons(tons, machine_list=temp_list) # step 2: tons
            temp_list = line.get_machine_by_color(color, machine_list=temp_list) # step 3: color
            if temp_list != []:
                machine_chosen = line.get_biggest_remaining_time(machine_list=temp_list) # step 4: remaining time
            if machine_chosen != None:
                machine_chosen_list.append(machine_chosen)
        
        
        if machine_chosen_list == [] and self.urgent == True: #-3-(1) Type1: if it is in urgent mode and no usable machine, release on
            self.release = False # release on
            machine_chosen = None
            for line in Factory_NWE.line_list:
                temp_list = line.get_ok_machine()
                temp_list = line.get_machine_by_tons(tons, machine_list=temp_list)
                machine_chosen_list = line.get_machine_by_color(color, machine_list=temp_list)
                for m in machine_chosen_list:
                    if m.order_list[0].urgent_tag == False and m.order_list[0].planning_time == 24.0:
                        machine_chosen = m
                        break
                    else:
                        continue
            if machine_chosen:
                return machine_chosen
            else:
                print('Warning : Emergency part number : ' + order['鴻海料號'] + ' did not been ordered.')
                self.buffer_list.append(order)
                return None

        elif machine_chosen_list == []: #-3-(2) Type2: if no machine is usable, return None
            return None

        else: #-3-(3) Type3: plural machine is usable, find the best one (the longest remaining time); or the best machine had been found
            if machine_chosen == None:
                keep_max = machine_chosen_list[0]
                
                for m in machine_chosen_list:
                    if m.remaining_time > keep_max.remaining_time:
                        keep_max = m
                machine_chosen = keep_max
                return machine_chosen

            else:
                return machine_chosen
        

    
    def time_calculation(self, order, machine_chosen):

        # Calculate time needed
        time_needed = round((order['總需求'] / order['產能']), 2)

        # If release on
        if self.release == True:
            origin_order = machine_chosen.order_list[0]
            time_origin_order = round(origin_order.planning_time - time_needed + 4, 2)
            hour_urgent = int(str(time_needed).split('.')[0])
            minute_urgent = (int(str(time_needed).split('.')[1])/100)*60

            origin_order.end_time = origin_order.end_time - datetime.timedelta(hours=(hour_urgent+4), minutes=minute_urgent) # adjust the origin order time
            origin_order.planning_time = origin_order.planning_time - time_needed

            start_time = origin_order.end_time + datetime.timedelta(hours=4) # calculate the urgent order time
            end_time = start_time + datetime.timedelta(hours=hour_urgent, minutes=minute_urgent)

            return start_time, end_time, time_needed
        
        # If buffer mode on
        if self.buffer == True:
            start_time = order_start_time
            end_time = order_end_time
            time_needed = 0
            return start_time, end_time, time_needed 

        # Calculate start time, end time
        # if it is the first order of this machine
        if len(machine_chosen.order_list) == 0:
            if machine_chosen.intime_order[0] != None and machine_chosen.intime_order[0].part_number == order['鴻海料號']:
                machine_chosen.remaining_time = round((machine_chosen.remaining_time-time_needed), 2)
                if machine_chosen.remaining_time < 0:
                    machine_chosen.remaining_time = 0
                hour_needed = int(str(time_needed).split('.')[0])
                minute_needed = (int(str(time_needed).split('.')[1])/100)*60
                start_time = machine_chosen.m_start_time
                end_time = start_time + datetime.timedelta(hours=hour_needed, minutes=minute_needed)
            else:
                machine_chosen.remaining_time = round((machine_chosen.remaining_time-time_needed-4), 2)
                if machine_chosen.remaining_time < 0:
                    machine_chosen.remaining_time = 0
                hour_needed = int(str(time_needed).split('.')[0])
                minute_needed = (int(str(time_needed).split('.')[1])/100)*60
                start_time = machine_chosen.m_start_time + datetime.timedelta(hours=4)
                end_time = start_time + datetime.timedelta(hours=hour_needed, minutes=minute_needed)
        # if it is not the first order
        else:
            # if it is no need mold changing
            if self.mold_change == False:
                machine_chosen.remaining_time = round((machine_chosen.remaining_time-time_needed), 2)
                if machine_chosen.remaining_time < 0:
                    machine_chosen.remaining_time = 0
                hour_needed = int(str(time_needed).split('.')[0])
                minute_needed = (int(str(time_needed).split('.')[1])/100)*60
                start_time = machine_chosen.order_list[-1].end_time
                end_time = start_time + datetime.timedelta(hours=hour_needed, minutes=minute_needed)

            # if mold changing is required, another 4 hours is needed
            else:
                machine_chosen.remaining_time = round((machine_chosen.remaining_time-time_needed-4), 2)
                if machine_chosen.remaining_time < 0:
                    machine_chosen.remaining_time = 0
                hour_needed = int(str(time_needed).split('.')[0])
                minute_needed = (int(str(time_needed).split('.')[1])/100)*60
                start_time = machine_chosen.order_list[-1].end_time + datetime.timedelta(hours=4)
                end_time = start_time + datetime.timedelta(hours=hour_needed, minutes=minute_needed)
        
        order['總需求'] = order['總需求'] - time_needed*order['產能'] # calcuate the remained demand
        
        return start_time, end_time, time_needed
        
    def main_function(self):
        # 1. Yesterday delayed
        for line in Factory_NWE.line_list: # O(n), n = number of orders
            for m in line.machine_list:
                if m.intime_order:
                    for d_o in m.intime_order:
                        if d_o:
                            input = {'鴻海料號' : d_o.part_number, '品名' : d_o.part_name, '噸位' : m.tons, '顏色' : m.tons, '總需求' : d_o.remaining_amount, \
                                     '產能' : d_o.UPH}
                            self.bind_machine = m
                            if_succeed = self.planning(input)
                        else:
                            continue
                else:
                    continue

        # 2. Emergency
        Emergency = pd.read_csv('./basic_information/Emergency/WK' + week + '/' + 'daily_emergency_' + date + '.csv')
        index = Emergency.index

        # (2-1 Check the part number with same mold
        for i in index: # O(m*n) m = number of emergency orders, n = number of machines
            input = Emergency.loc[index[i]]
            for line in Factory_NWE.line_list:
                for m in line.machine_list:
                    if m.order_list == []:
                        continue
                    else:
                        if Id.same_mold(m.order_list[-1].part_number, input['鴻海料號']):
                            if input['鴻海料號'] in self.record_ordered_part_number and input['模具數'] == 1:
                                continue
                            else:
                                self.mold_change = False
                                self.plastic_change = False
                                self.bind_machine = m
                                if_succeed = self.planning(input)
                            Emergency.drop(Emergency.index[i])

        # (2-2 Input other emergency order
        self.urgent = False # urgent mode on
        for e in range(len(Emergency)):
            input = Emergency.loc[index[e]]
            if input['鴻海料號'] in self.record_ordered_part_number and input['模具數'] == 1:
                continue
            elif input['鴻海料號'] in self.record_ordered_part_number and input['模具數'] > 1:
                for m_n in range(input['模具數']-1):
                    if_succeed = self.planning(input)
            else:
                if_succeed = self.planning(input)
        self.urgent = False # urgent mode off

        # 3. Normal
        Normal = self.total_weekly_planning[((self.total_weekly_planning['噸位'] == '100T') | (self.total_weekly_planning['噸位'] == '130T'))]
        index = Normal.index
        for n in range(len(Normal)):
            input = Normal.loc[index[n]]
            if input['鴻海料號'] in self.record_ordered_part_number:
                continue
            else:
                if_succeed = self.planning(input)
            if self.if_stop == True:
                break

        # # 4. Add buffer
        # self.buffer = False # buffer mode on
        # for input in self.buffer_list:
        #     if_succeed = self.planning(input)
        # self.buffer = False # buffer mode off

        
        return self.total_weekly_planning