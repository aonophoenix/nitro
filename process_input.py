
# coding: utf-8

# In[1]:


#!/usr/bin/python3
import datetime
import os
import sys

import numpy as np
import pandas as pd


# Open and save each of the data files prior to running this script. The software that outputs these files doesn't properly initialize the file, resulting in the file header indicating a data collection called the SSCS (Short Sector Container Stream) is empty, but the SSAT (Short Sector Allocation Table) used to access that collection is not empty.

# In[2]:


row1_back = pd.read_excel(io='Row1Back 18Jan18-1421.xls',
                          sheetname=0,
                          header=None,
                          skiprows=[0,1,2],
                          names=['time', 'port1', 'port2', 'port3'],
                          usecols=[0,1,2,3],
                          converters={'0':datetime,'1':np.int32,'2':np.int32,'3':np.int32})
row1_back['location'] = 'row1_back'
# row1_back.head()


# In[41]:


treatment = pd.DataFrame({
    'location':['p11','p12','p13',
                'p21','p22','p23',
                'p31','p32','p33',
                'p41','p42','p43',
                'p51','p52','p53',
                'p61','p62','p63',
                'p71','p72','p73',
                'p81','p82','p83',
                'p91','p92','p93'],
    'nitrogen_treament':['deficient','excessive','deficient',
                         'deficient','optimum','excessive',
                         'optimum','optimum','excessive',
                         'excessive','excessive','optimum',
                         'deficient','deficient','optimum',
                         'excessive','deficient','optimum',
                         'optimum','excessive','deficient',
                         'optimum','deficient','excessive',
                         'excessive','optimum','deficient'],
    'irrigation_treatment':['full','high','high',
                            'low','high','low',
                            'full','low','full',
                            'high','low','full',
                            'low','high','high',
                            'full','full','low',
                            'low','full','low',
                            'low','high','high',
                            'high','full','full']
})


# In[44]:


row1_front = pd.read_excel(io='Row1Frnt 18Jan18-1418.xls',
                           sheetname=0,
                           header=None,
                           skiprows=[0,1,2],
                           names=['time', 
                                  'row1f_p1_vwc', 'row1f_p1_temp', 'row1f_p1_ec',
                                  'row1f_p2_vwc', 'row1f_p2_temp', 'row1f_p2_ec',
                                  'row1f_p3_vwc', 'row1f_p3_temp', 'row1f_p3_ec',
                                  'row1f_p4_630', 'row1f_p4_800', 'r1f_p4_ndvi',
                                  'row1f_p5_targ', 'row1f_p5_body'],
                           usecols=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14])
p11 = row1_front[['time', 'row1f_p1_vwc', 'row1f_p1_temp', 'row1f_p1_ec']].copy(deep=True)
p11.rename(columns={'row1f_p1_vwc':'vwc', 'row1f_p1_temp':'temp_soil', 'row1f_p1_ec':'ec'}, inplace=True)
p11['location'] = 'p11'

p12 = row1_front[['time', 'row1f_p2_vwc', 'row1f_p2_temp', 'row1f_p2_ec']].copy(deep=True)
p12.rename(columns={'row1f_p2_vwc':'vwc', 'row1f_p2_temp':'temp_soil', 'row1f_p2_ec':'ec'}, inplace=True)
p12['location'] = 'p12'

p13 = row1_front[['time', 'row1f_p3_vwc', 'row1f_p3_temp', 'row1f_p3_ec']].copy(deep=True)
p13.rename(columns={'row1f_p3_vwc':'vwc', 'row1f_p3_temp':'temp_soil', 'row1f_p3_ec':'ec'}, inplace=True)
p13['location'] = 'p13'

p14 = row1_front[['time', 'row1f_p4_630', 'row1f_p4_800', 'r1f_p4_ndvi']].copy(deep=True)
p14.rename(columns={'row1f_p4_630':'630nm', 'row1f_p4_800':'800nm', 'r1f_p4_ndvi':'ndvi'}, inplace=True)
p14['location'] = 'p13'

p15 = row1_front[['time', 'row1f_p5_targ', 'row1f_p5_body']].copy(deep=True)
p15.rename(columns={'row1f_p5_targ':'temp_targ', 'row1f_p5_body':'temp_body'}, inplace=True)
p15['location'] = 'p13'
row1_front.to_csv('row1_front.csv')
row1f = p11.append(p12, ignore_index=True)
row1f = row1f.append(p13, ignore_index=True)
row1f = row1f.append(p14, ignore_index=True)
row1f = row1f.append(p15, ignore_index=True)
row1f.to_csv('row1f.tsv', index=False, na_rep='#N/A', sep='\t')


# In[4]:


row2 = pd.read_excel(io='Row2 18Jan18-1423.xls',
                     sheetname=0,
                     header=None,
                     skiprows=[0,1,2],
                     names=['time', 
                            'r2_p1_vwc', 'r2_p1_temp', 'r2_p1_ec',
                            'r2_p2_vwc', 'r2_p2_temp', 'r2_p2_ec',
                            'r2_p3_vwc', 'r2_p3_temp', 'r2_p3_ec',
                            'r2_p4_630', 'r2_p4_800', 'r2_p4_ndvi',
                            'r2_p5_targ', 'r2_p5_body'],
                     usecols=[0,1,2,3,4,5,6,7,8,9,10,11,12,13])
row2['location'] = 'row2'
row2.head()


# In[5]:


row3 = pd.read_excel(io='Row3 18Jan18-1426.xls',
                     sheetname=0,
                     header=None,
                     skiprows=[0,1,2],
                     names=['time', 
                            'r3_p1_vwc', 'r3_p1_temp', 'r3_p1_ec',
                            'r3_p2_vwc', 'r3_p2_temp', 'r3_p2_ec',
                            'r3_p3_vwc', 'r3_p3_temp', 'r3_p3_ec',
                            'r3_p4_630', 'r3_p4_800', 'r3_p4_ndvi',
                            'r3_p5_targ', 'r3_p5_body'],
                     usecols=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14])
row3['location'] = 'row3'
row3.head()


# In[6]:


row4_back = pd.read_excel(io='Row4Back 18Jan18-1430.xls',
                      sheetname=0,
                      header=None,
                      skiprows=[0,1,2],
                      names=['time', 
                             'r4b_p1_vwc', 'r4b_p1_temp', 'r4b_p1_ec',
                             'r4b_p2_vwc', 'r4b_p2_temp', 'r4b_p2_ec',
                             'r4b_p3_pot', 'r4b_p3_temp',
                             'r4b_p4_pot', 'r4b_p4_temp',
                             'r4b_p5_pot', 'r4b_p5_temp'],
                          usecols=[0,1,2,3,4,5,6,7,8,9,10,11,12,13])
row4_back['location'] = 'row4_back'
row4_back.head()


# In[7]:


row4_front = pd.read_excel(io='Row4Frnt 18Jan18-1428.xls',
                           sheetname=0,
                           header=None,
                           skiprows=[0,1,2],
                           names=['time', 
                                  'r4f_p1_vwc', 'r4f_p1_temp', 'r4f_p1_ec',
                                  'r4f_p2_vwc', 'r4f_p2_temp', 'r4f_p2_ec',
                                  'r4f_p3_vwc', 'r4f_p3_temp', 'r4f_p3_ec',
                                  'r4f_p4_630', 'r4f_p4_800', 'r4f_p4_ndvi',
                                  'r4f_p5_targ', 'r4f_p5_body'],
                           usecols=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14])
row4_front['location'] = 'row4_front'
row4_front.head()


# In[8]:


row5_back = pd.read_excel(io='Row5Back 18Jan18-1435.xls',
                          sheetname=0,
                          header=None,
                          skiprows=[0,1,2],
                          names=['time', 
                                 'r4b_p1_vwc', 'r4b_p1_temp', 'r4b_p1_ec',
                                 'r4b_p2_vwc', 'r4b_p2_temp', 'r4b_p2_ec',
                                 'r4b_p3_pot', 'r4b_p3_temp',
                                 'r4b_p4_pot', 'r4b_p4_temp',
                                 'r4b_p5_pot', 'r4b_p5_temp'],
                          usecols=[0,1,2,3,4,5,6,7,8,9,10,11,12,13])
row5_back['location'] = 'row5_back'
row5_back.head()


# In[9]:


row5_front = pd.read_excel(io='Row5Frnt 18Jan18-1432.xls',
                           sheetname=0,
                           header=None,
                           skiprows=[0,1,2],
                           names=['time', 
                                  'r5f_p1_vwc', 'r5f_p1_temp', 'r5f_p1_ec',
                                  'r5f_p2_vwc', 'r5f_p2_temp', 'r5f_p2_ec',
                                  'r5f_p3_vwc', 'r5f_p3_temp', 'r5f_p3_ec',
                                  'r5f_p4_630', 'r5f_p4_800', 'r5f_p4_ndvi',
                                  'r5f_p5_targ', 'r5f_p5_body'],
                           usecols=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14])
row5_front['location'] = 'row5_front'
row5_front.head()


# In[10]:


row6_back = pd.read_excel(io='Row6Back 18Jan18-1439.xls',
                          sheetname=0,
                          header=None,
                          skiprows=[0,1,2],
                          names=['time', 
                                 'r6b_p1_vwc', 'r6b_p1_temp', 'r6b_p1_ec',
                                 'r6b_p2_vwc', 'r6b_p2_temp', 'r6b_p2_ec',
                                 'r6b_p3_pot', 'r6b_p3_temp',
                                 'r6b_p4_pot', 'r6b_p4_temp',
                                 'r6b_p5_pot', 'r6b_p5_temp'],
                          usecols=[0,1,2,3,4,5,6,7,8,9,10,11,12,13])
row6_back['location'] = 'row6_back'
row6_back.head()


# In[11]:


row6_front = pd.read_excel(io='Row6Frnt 18Jan18-1437.xls',
                           sheetname=0,
                           header=None,
                           skiprows=[0,1,2],
                           names=['time', 
                                  'r6f_p1_vwc', 'r6f_p1_temp', 'r6f_p1_ec',
                                  'r6f_p2_vwc', 'r6f_p2_temp', 'r6f_p2_ec',
                                  'r6f_p3_vwc', 'r6f_p3_temp', 'r6f_p3_ec',
                                  'r6f_p4_630', 'r6f_p4_800', 'r6f_p4_ndvi',
                                  'r6f_p5_targ', 'r6f_p5_body'],
                           usecols=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14])
row6_front['location'] = 'row6_front'
row6_front.head()


# In[12]:


row7 = pd.read_excel(io='Row7 18Jan18-1441.xls',
                     sheetname=0,
                     header=None,
                     skiprows=[0,1,2],
                     names=['time', 
                            'r7_p1_vwc', 'r7_p1_temp', 'r7_p1_ec',
                            'r7_p2_vwc', 'r7_p2_temp', 'r7_p2_ec',
                            'r7_p3_vwc', 'r7_p3_temp', 'r7_p3_ec',
                            'r7_p4_630', 'r7_p4_800', 'r7_p4_ndvi',
                            'r7_p5_targ', 'r7_p5_body'],
                     usecols=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14])
row7['location'] = 'row7'
row7.head()


# In[13]:


row8 = pd.read_excel(io='Row8 18Jan18-1443.xls',
                     sheetname=0,
                     header=None,
                     skiprows=[0,1,2],
                     names=['time', 
                            'r8_p1_vwc', 'r8_p1_temp', 'r8_p1_ec',
                            'r8_p2_vwc', 'r8_p2_temp', 'r8_p2_ec',
                            'r8_p3_vwc', 'r8_p3_temp', 'r8_p3_ec',
                            'r8_p4_630', 'r8_p4_800', 'r8_p4_ndvi',
                            'r8_p5_targ', 'r8_p5_body'],
                     usecols=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14])
row8['location'] = 'row8'
row8.head()


# In[14]:


row9 = pd.read_excel(io='Row9 18Jan18-1445.xls',
                     sheetname=0,
                     header=None,
                     skiprows=[0,1,2],
                     names=['time', 
                            'r9_p1_vwc', 'r9_p1_temp', 'r9_p1_ec',
                            'r9_p2_vwc', 'r9_p2_temp', 'r9_p2_ec',
                            'r9_p3_vwc', 'r9_p3_temp', 'r9_p3_ec',
                            'r9_p4_630', 'r9_p4_800', 'r9_p4_ndvi',
                            'r9_p5_targ', 'r9_p5_body'],
                     usecols=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14])
row9['location'] = 'row9'
row9.head()


# In[20]:


# allrows = pd.merge(left=row1_front, right=row2, how='left', on='time')
# allrows = pd.merge(left=allrows, right=row3, how='left', on='time')
# allrows = pd.merge(left=allrows, right=row4_back, how='left', on='time')
# allrows = pd.merge(left=allrows, right=row4_front, how='left', on='time')
# allrows = pd.merge(left=allrows, right=row5_back, how='left', on='time')
# allrows = pd.merge(left=allrows, right=row5_front, how='left', on='time')
# allrows = pd.merge(left=allrows, right=row6_back, how='left', on='time')
# allrows = pd.merge(left=allrows, right=row6_front, how='left', on='time')
# allrows = pd.merge(left=allrows, right=row7, how='left', on='time')
# allrows = pd.merge(left=allrows, right=row8, how='left', on='time')
# allrows = pd.merge(left=allrows, right=row9, how='left', on='time')
# allrows.drop(labels=['location_x','location_y'], axis=1, inplace=True)
# allrows.to_csv('allrows.csv', index=False, na_rep='0')
# allrows.head()


# In[ ]:




