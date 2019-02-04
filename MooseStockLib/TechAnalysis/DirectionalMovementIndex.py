# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 15:28:21 2019

@author: Mussina
"""
import logging
import pandas as pd
from pathlib import Path

class DMI():
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger("root")
        
    def create_DMI_Index(self, df_company, company):
        self.logger.info('[v] create DMI')
        
        # --- read and pre-process --- #
        self.logger.info('DMI process...[%s]',company)
    #    filePath = "../../CompanyData/" + company + "_DMI.xlsx"
        filePath = "/Users/Mussina/Documents/GitRepo/Self/TwStockAnalysis/CompanyData/2330_DMI.xlsx"
        sid_file = Path(filePath)
        if not sid_file.is_file():
            self.logger.info("file not exist...please create [%s] file first.",filePath)
            return
        
        #excel_writer = pd.ExcelWriter(filePath)
        df_DMI = pd.read_excel(filePath)
        
        #df_DMI = df_DMI.dropna()
        
        self._createDMI(df_company, df_DMI)
        
        #excel_writer.close()
        self.logger.info('[^] create DMI')
        
    def _createDMI(self, df_company, df_DMI):
        if df_DMI.last_valid_index() == None:
            dmi_idx = 0
        else:
            dmi_idx = df_DMI.last_valid_index() + 1
        
        row_num = len(df_company.index)
        for i in range(row_num):
            #TODO: encapsulate DMI var to a class
            if i == 0:
                DM_plus = 0
                DM_minus = 0
                DM_Plus_Pulan = 0
                DM_Minus_Pulan = 0
                Ht_Lt = 0
                Ht_Ct = 0
                Lt_Ct = 0
                TR = 0
            else:
                DM_plus = self._cal_DM_Plus(df_company.iloc[i]['最高價'], df_company.iloc[i-1]['最高價'])
                DM_minus = self._cal_DM_Minus(df_company.iloc[i-1]['最低價'], df_company.iloc[i]['最低價'])
                (DM_Plus_Pulan, DM_Minus_Pulan) = self._cal_DM_Plus_Minus_Pulan(DM_plus, DM_minus)
                (Ht_Lt, Ht_Ct, Lt_Ct, TR) = self._cal_TR(df_company.iloc[i]['最高價'], df_company.iloc[i]['最低價'],df_company.iloc[i-1]['收盤價'])
                
            df_DMI.loc[dmi_idx] = [df_company.iloc[i]['日期'],
                                   df_company.iloc[i]['最高價'],
                                   df_company.iloc[i]['最低價'],
                                   df_company.iloc[i]['收盤價'],
                                   DM_plus,
                                   DM_minus,
                                   DM_Plus_Pulan,
                                   DM_Minus_Pulan,
                                   Ht_Lt,
                                   Ht_Ct,
                                   Lt_Ct,
                                   TR,
                                   df_company.iloc[i]['最高價'],
                                   df_company.iloc[i]['最高價'],
                                   df_company.iloc[i]['最高價'],
                                   df_company.iloc[i]['最高價'],
                                   df_company.iloc[i]['最高價'],
                                   df_company.iloc[i]['最高價']                                
                                  ]
            #df_DMI.iloc[dmi_idx]['最低價'] = df_company.iloc[i]['最低價']
            dmi_idx += 1        
            print("Ht_Lt:{0} Ht_Ct:{1} Lt_Ct:{2} TR:{3}".format(Ht_Lt, Ht_Ct,Lt_Ct,TR))
            
            # --- get start index --- #
            
        #print(df_DMI)
        #--- set data to dataframe ---#
            #df_company['最高價']
            
    '''
    calaulate DM+
    '''
    def _cal_DM_Plus(self, highest_price, pre_highest_price):
        DM_plus = highest_price - pre_highest_price
        if DM_plus < 0:
            DM_plus = 0
        return DM_plus
    
    '''
    calaulate DM-
    '''
    def _cal_DM_Minus(self, pre_lowest_price, lowest_price):
        DM_minus = pre_lowest_price - lowest_price
        if DM_minus < 0:
            DM_minus = 0
        return DM_minus
    
    '''
    calaulate DM+' & DM-'
    '''
    def _cal_DM_Plus_Minus_Pulan(self, DM_plus, DM_minus):
        if DM_plus > DM_minus:
            DM_Plus_Pulan = DM_plus
            DM_Minus_Pulan = 0
        elif DM_plus < DM_minus:
            DM_Plus_Pulan = 0
            DM_Minus_Pulan = DM_minus
        else:
            DM_Plus_Pulan = 0
            DM_Minus_Pulan = 0
        
        return (DM_Plus_Pulan, DM_Minus_Pulan)
    
    '''
    calaulate TR(True Range)
    '''
    def _cal_TR(self, highest_price, lowest_price, pre_close_price):
        Ht_Lt = highest_price - lowest_price
        Ht_Ct = highest_price - pre_close_price   
        Lt_Ct = abs(lowest_price - pre_close_price)
        TR = max(Ht_Lt,Ht_Ct,Lt_Ct)
        return (Ht_Lt, Ht_Ct, Lt_Ct, TR)
    
    
    
    
    
    
    
    
    