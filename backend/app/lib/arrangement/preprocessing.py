import pandas as pd
import numpy as np
import os


class preprocessing():
    def __init__(self, path_source, path_daily_underdemand, path_basic, week, date):
        self.df = pd.read_excel(path_source + 'WK' + week + '_X' + '.xlsx', sheet_name="成型需求匯總")
        self.df = self.df[self.df['自製or外包'] == '廠內自制']
        self.basic_df =  pd.read_excel(path_basic + 'molding_basic_information.xlsx').drop_duplicates('鴻海料號')
        self.color_df = pd.read_csv(path_basic + 'plastic_color.csv')
        

    def delete_Duplicated_Element_From_List(self, list):
        resultList = []
        for item in list:
            if not item in resultList:
                resultList.append(item)
        return resultList

    def removespace(self, s):
        if type(s) != str:
            return ''
        result_str = ''
        if s[-1] == ' ':
            i = 0
            while(s[i] != ' '):
                result_str = result_str + s[i]
                i+=1
        return result_str

    def weekly_demand(self):

        dup_df = self.df[self.df.duplicated('下階')]
        dup_list = self.delete_Duplicated_Element_From_List(dup_df['下階'].tolist()) # get the list of duplicated part numbers

        # Recalculate the total amount for those duplicated parts
        total_amount = []

        for d in dup_list: # calculate total amount
            temp_df = self.df[self.df['下階'] == d]
            total_amount.append(temp_df['需求總量'].sum())


        self.df = self.df.drop_duplicates('下階')
        for i, d in enumerate(dup_list): # revise total amount
            ptr = 0
            ptr = self.df.index[self.df['下階'] == d]
            self.df.loc[ptr, '需求總量'] = total_amount[i]

        return     

    def get_color(self, partnumberlist):
        color = []
        ptr_plastic_number = 0
        ptr_plastic_color = 0
        for pn in partnumberlist:
            ptr_plastic_number = self.basic_df.index[self.basic_df['鴻海料號'] == pn]
            if pn == '':
                color.append('')
            else: # get plastic number by relating to "Molding Basic Information Sheet"
                plastic_number = self.basic_df.loc[ptr_plastic_number, '塑膠粒料號'].values
                if len(plastic_number) == 0:
                    color.append('') # if plastic number not recorded
                    continue
                else:
                    plastic_number = plastic_number[0]
                    plastic_number = self.removespace(plastic_number)

                # get plastic color by relating to "Molding Plastic Color Sheet"
                plastic_color = self.color_df[self.color_df['料號'] == plastic_number]['顏色'].values.tolist()
                if len(plastic_color) == 0:
                    color.append('') # if plastic color not recorded
                else:
                    color.append(plastic_color[0])
        return color

    def daily_underdemand(self, weekly_demand_df):
        self.underdemand_df = pd.read_excel(path_daily_underdemand + 'forD11_' + date + '.xlsx', sheet_name='組裝日計畫缺料匯總')
        # Get the rows that we need (Only get the rows that with positive demand)
        underdemand_df = self.underdemand_df[self.underdemand_df['total:'] != 0]
        underdemand_df = underdemand_df[underdemand_df['物料來源'] == '自制']

        dup_df = underdemand_df[underdemand_df.duplicated('成型料號')]
        dup_list = self.delete_Duplicated_Element_From_List(dup_df['成型料號'].tolist()) # get the list of duplicated part numbers

        # Recalculate the total demand for those duplicated parts
        total_demand = []

        for d in dup_list: # calculate the total demand
            temp_df = underdemand_df[underdemand_df['成型料號'] == d]
            total_demand.append(temp_df['total:'].sum())

        underdemand_df = underdemand_df.drop_duplicates('成型料號')
        for i,d in enumerate(dup_list): # revise total amount
            ptr = 0
            ptr = underdemand_df.index[underdemand_df['成型料號'] == d]
            underdemand_df.loc[ptr, '需求總量'] = total_demand[i]
            underdemand_df.loc[ptr, '欠量'] = (underdemand_df.loc[ptr, '廠內庫存DXS8'] + underdemand_df.loc[ptr, '廠外庫存DXS5']) - total_demand[i]

        # Make the dataframe with columns that we need
        partnumber_list = underdemand_df['成型料號'].tolist()
        underdemand_list = underdemand_df['欠量'].tolist()
        for i, demand in enumerate(underdemand_list):
            if demand >= 0:
                underdemand_list[i] = '' 
        underdemand_df = pd.DataFrame({'成型料號' : partnumber_list, '欠量' : underdemand_list})
        result_df = pd.merge(weekly_demand_df, underdemand_df, how='outer', left_on='鴻海料號', right_on='成型料號').drop('成型料號', axis=1)

        return result_df

    def get_planning_input(self):
        # Define needed columns
        part_number_list = []
        total_demand_list = []
        result_tons_list = []
        productivity_list = []
        part_name_list = []
        color_list = []

        
        self.weekly_demand() # 1. get weekly demand

        part_name_list = self.df['品名'].tolist()
        productivity_list = self.df['產能'].tolist()
        part_number_list = self.df['下階'].tolist()
        total_demand_list = self.df['需求總量'].tolist()
        result_tons_list = self.df['噸位'].tolist()
        color_list = self.get_color(self.df['下階'].tolist()) # 2. get plastic color
        
        # Make output dataframe
        result_df = pd.DataFrame({'鴻海料號' : part_number_list, '總需求' : total_demand_list, '噸位' : result_tons_list, \
                                  '產能' : productivity_list, '品名' : part_name_list, '顏色' : color_list})
        result_df = result_df[result_df['總需求'] != 0].reset_index().drop('index', axis=1)
        #result_df = self.daily_underdemand(result_df) # 3. get daily demand

        return result_df
