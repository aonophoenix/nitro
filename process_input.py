
# coding: utf-8

# In[ ]:


import datetime
import os
import sys

import numpy as np
import pandas as pd

os.chdir('data/')


# Use Excel to open and save each of the data files prior to running this script. The software that outputs these files doesn't properly initialize the file, resulting in the file header indicating a data collection called the SSCS (Short Sector Container Stream) is empty, but the SSAT (Short Sector Allocation Table) used to access that collection is not empty.

# In[ ]:


outputIntermediateFiles = False

def determine_activeflow(row):
    if (row['low'] != 0 or row['full'] != 0 or row['high'] != 0):
        return True

print('building treatment frame')
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
    'irrigation_treatment':['low','high','high',
                            'full','high','full',
                            'low','full','low',
                            'high','full','low',
                            'full','high','high',
                            'low','low','full',
                            'full','low','full',
                            'full','high','high',
                            'high','low','low']
})
if (outputIntermediateFiles):
    treatment.to_csv('treatment.tsv', index=False, sep='\t')


# In[ ]:


print('building row1_back frame')
row1_back = pd.read_excel(io='Row1Back 18Jan18-1421.xls',
                          sheet_name=0,
                          header=None,
                          skiprows=[0,1,2],
                          names=['time', 'low', 'full', 'high'],
                          usecols=[0,1,2,3],
                          converters={'0':datetime,'1':np.int32,'2':np.int32,'3':np.int32})
row1_back['location'] = 'row1_back'
row1_back['activeflow'] = row1_back.apply(determine_activeflow, axis=1)

sums = pd.DataFrame({'low':[np.sum(row1_back['low'])],
                     'full':[np.sum(row1_back['full'])],
                     'high':[np.sum(row1_back['high'])]
                    })


# In[ ]:


print('building row1_front frame')
row1_front = pd.read_excel(io='Row1Frnt 18Jan18-1418.xls',
                           sheet_name=0,
                           header=None,
                           skiprows=[0,1,2],
                           names=['time', 
                                  'row1f_p1_vwc', 'row1f_p1_temp', 'row1f_p1_ec',
                                  'row1f_p2_vwc', 'row1f_p2_temp', 'row1f_p2_ec',
                                  'row1f_p3_vwc', 'row1f_p3_temp', 'row1f_p3_ec',
                                  'row1f_p4_630', 'row1f_p4_800', 'r1f_p4_ndvi',
                                  'row1f_p5_targ', 'row1f_p5_body'],
                           usecols=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14])
slice1 = row1_front[['time', 'row1f_p1_vwc', 'row1f_p1_temp', 'row1f_p1_ec']].copy(deep=True)
slice1.rename(columns={'row1f_p1_vwc':'vwc_64', 'row1f_p1_temp':'temp_soil_64', 'row1f_p1_ec':'ec_64'}, inplace=True)
slice1['location'] = 'p11'
slice1['measurement'] = slice1.index

slice2 = row1_front[['time', 'row1f_p2_vwc', 'row1f_p2_temp', 'row1f_p2_ec']].copy(deep=True)
slice2.rename(columns={'row1f_p2_vwc':'vwc_64', 'row1f_p2_temp':'temp_soil_64', 'row1f_p2_ec':'ec_64'}, inplace=True)
slice2['location'] = 'p12'
slice2['measurement'] = slice2.index

slice3 = row1_front[['time', 'row1f_p3_vwc', 'row1f_p3_temp', 'row1f_p3_ec']].copy(deep=True)
slice3.rename(columns={'row1f_p3_vwc':'vwc_64', 'row1f_p3_temp':'temp_soil_64', 'row1f_p3_ec':'ec_64'}, inplace=True)
slice3['location'] = 'p13'
slice3['measurement'] = slice3.index

slice4 = row1_front[['time', 'row1f_p4_630', 'row1f_p4_800', 'r1f_p4_ndvi']].copy(deep=True)
slice4.rename(columns={'row1f_p4_630':'630nm', 'row1f_p4_800':'800nm', 'r1f_p4_ndvi':'ndvi'}, inplace=True)
slice4['location'] = 'p13'
slice4['measurement'] = slice4.index

slice5 = row1_front[['time', 'row1f_p5_targ', 'row1f_p5_body']].copy(deep=True)
slice5.rename(columns={'row1f_p5_targ':'temp_targ', 'row1f_p5_body':'temp_body'}, inplace=True)
slice5['location'] = 'p13'
slice5['measurement'] = slice5.index
if (outputIntermediateFiles):
    row1_front.to_csv('row1_front.csv')
r1f = slice1.append(slice2, ignore_index=True)
r1f = r1f.append(slice3, ignore_index=True)
r1f = r1f.append(slice4, ignore_index=True)
r1f = r1f.append(slice5, ignore_index=True)
r1f = pd.merge(left=r1f, right=treatment, how='inner', on='location')
if (outputIntermediateFiles):
    r1f.to_csv('r1f.tsv', index=False, na_rep='N/A', sep='\t')


# In[ ]:


print('building row2 frame')
row2 = pd.read_excel(io='Row2 18Jan18-1423.xls',
                     sheet_name=0,
                     header=None,
                     skiprows=[0,1,2],
                     names=['time', 
                            'r2_p1_vwc', 'r2_p1_temp', 'r2_p1_ec',
                            'r2_p2_vwc', 'r2_p2_temp', 'r2_p2_ec',
                            'r2_p3_vwc', 'r2_p3_temp', 'r2_p3_ec',
                            'r2_p4_630', 'r2_p4_800', 'r2_p4_ndvi',
                            'r2_p5_targ', 'r2_p5_body'],
                     usecols=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14])

slice1 = row2[['time', 'r2_p1_vwc', 'r2_p1_temp', 'r2_p1_ec']].copy(deep=True)
slice1.rename(columns={'r2_p1_vwc':'vwc_64', 'r2_p1_temp':'temp_soil_64', 'r2_p1_ec':'ec_64'}, inplace=True)
slice1['location'] = 'p21'
slice1['measurement'] = slice1.index

slice2 = row2[['time', 'r2_p2_vwc', 'r2_p2_temp', 'r2_p2_ec']].copy(deep=True)
slice2.rename(columns={'r2_p2_vwc':'vwc_64', 'r2_p2_temp':'temp_soil_64', 'r2_p2_ec':'ec_64'}, inplace=True)
slice2['location'] = 'p22'
slice2['measurement'] = slice2.index

slice3 = row2[['time', 'r2_p3_vwc', 'r2_p3_temp', 'r2_p3_ec']].copy(deep=True)
slice3.rename(columns={'r2_p3_vwc':'vwc_64', 'r2_p3_temp':'temp_soil_64', 'r2_p3_ec':'ec_64'}, inplace=True)
slice3['location'] = 'p23'
slice3['measurement'] = slice3.index

slice4 = row2[['time', 'r2_p4_630', 'r2_p4_800', 'r2_p4_ndvi']].copy(deep=True)
slice4.rename(columns={'r2_p4_630':'630nm', 'r2_p4_800':'800nm', 'r2_p4_ndvi':'ndvi'}, inplace=True)
slice4['location'] = 'p23'
slice4['measurement'] = slice4.index

slice5 = row2[['time', 'r2_p5_targ', 'r2_p5_body']].copy(deep=True)
slice5.rename(columns={'r2_p5_targ':'temp_targ', 'r2_p5_body':'temp_body'}, inplace=True)
slice5['location'] = 'p23'
slice5['measurement'] = slice5.index
if (outputIntermediateFiles):
    row2.to_csv('row2.csv')
r2 = slice1.append(slice2, ignore_index=True)
r2 = r2.append(slice3, ignore_index=True)
r2 = r2.append(slice4, ignore_index=True)
r2 = r2.append(slice5, ignore_index=True)
r2 = pd.merge(left=r2, right=treatment, how='inner', on='location')
if (outputIntermediateFiles):
    r2.to_csv('r2.tsv', index=False, na_rep='N/A', sep='\t')


# In[ ]:


print('building row3 frame')
row3 = pd.read_excel(io='Row3 18Jan18-1426.xls',
                     sheet_name=0,
                     header=None,
                     skiprows=[0,1,2],
                     names=['time', 
                            'r3_p1_vwc', 'r3_p1_temp', 'r3_p1_ec',
                            'r3_p2_vwc', 'r3_p2_temp', 'r3_p2_ec',
                            'r3_p3_vwc', 'r3_p3_temp', 'r3_p3_ec',
                            'r3_p4_630', 'r3_p4_800', 'r3_p4_ndvi',
                            'r3_p5_targ', 'r3_p5_body'],
                     usecols=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14])

slice1 = row3[['time', 'r3_p1_vwc', 'r3_p1_temp', 'r3_p1_ec']].copy(deep=True)
slice1.rename(columns={'r3_p1_vwc':'vwc_64', 'r3_p1_temp':'temp_soil_64', 'r3_p1_ec':'ec_64'}, inplace=True)
slice1['location'] = 'p31'
slice1['measurement'] = slice1.index

slice2 = row3[['time', 'r3_p2_vwc', 'r3_p2_temp', 'r3_p2_ec']].copy(deep=True)
slice2.rename(columns={'r3_p2_vwc':'vwc_64', 'r3_p2_temp':'temp_soil_64', 'r3_p2_ec':'ec_64'}, inplace=True)
slice2['location'] = 'p32'
slice2['measurement'] = slice2.index

slice3 = row3[['time', 'r3_p3_vwc', 'r3_p3_temp', 'r3_p3_ec']].copy(deep=True)
slice3.rename(columns={'r3_p3_vwc':'vwc_64', 'r3_p3_temp':'temp_soil_64', 'r3_p3_ec':'ec_64'}, inplace=True)
slice3['location'] = 'p33'
slice3['measurement'] = slice3.index

slice4 = row3[['time', 'r3_p4_630', 'r3_p4_800', 'r3_p4_ndvi']].copy(deep=True)
slice4.rename(columns={'r3_p4_630':'630nm', 'r3_p4_800':'800nm', 'r3_p4_ndvi':'ndvi'}, inplace=True)
slice4['location'] = 'p33'
slice4['measurement'] = slice4.index

slice5 = row3[['time', 'r3_p5_targ', 'r3_p5_body']].copy(deep=True)
slice5.rename(columns={'r3_p5_targ':'temp_targ', 'r3_p5_body':'temp_body'}, inplace=True)
slice5['location'] = 'p33'
slice5['measurement'] = slice5.index
if (outputIntermediateFiles):
    row3.to_csv('row3.csv')
r3 = slice1.append(slice2, ignore_index=True)
r3 = r3.append(slice3, ignore_index=True)
r3 = r3.append(slice4, ignore_index=True)
r3 = r3.append(slice5, ignore_index=True)
r3 = pd.merge(left=r3, right=treatment, how='inner', on='location')
if (outputIntermediateFiles):
    r3.to_csv('r3.tsv', index=False, na_rep='N/A', sep='\t')


# In[ ]:


print('building row4_back frame')
row4_back = pd.read_excel(io='Row4Back 18Jan18-1430.xls',
                      sheet_name=0,
                      header=None,
                      skiprows=[0,1,2],
                      names=['time', 
                             'r4b_p1_vwc', 'r4b_p1_temp', 'r4b_p1_ec',
                             'r4b_p2_vwc', 'r4b_p2_temp', 'r4b_p2_ec',
                             'r4b_p3_pot', 'r4b_p3_temp',
                             'r4b_p4_pot', 'r4b_p4_temp',
                             'r4b_p5_pot', 'r4b_p5_temp'],
                          usecols=[0,1,2,3,4,5,6,7,8,9,10,11,12,13])

slice1 = row4_back[['time', 'r4b_p1_vwc', 'r4b_p1_temp', 'r4b_p1_ec']].copy(deep=True)
slice1.rename(columns={'r4b_p1_vwc':'vwc_150', 'r4b_p1_temp':'temp_soil_150', 'r4b_p1_ec':'ec_150'}, inplace=True)
slice1['location'] = 'p43'
slice1['measurement'] = slice1.index

slice2 = row4_back[['time', 'r4b_p2_vwc', 'r4b_p2_temp', 'r4b_p2_ec']].copy(deep=True)
slice2.rename(columns={'r4b_p2_vwc':'vwc_300', 'r4b_p2_temp':'temp_soil_300', 'r4b_p2_ec':'ec_300'}, inplace=True)
slice2['location'] = 'p43'
slice2['measurement'] = slice2.index

slice3 = row4_back[['time', 'r4b_p3_pot', 'r4b_p3_temp']].copy(deep=True)
slice3.rename(columns={'r4b_p3_pot':'pot_64', 'r4b_p3_temp':'temp_soil_64'}, inplace=True)
slice3['location'] = 'p43'
slice3['measurement'] = slice3.index

slice4 = row4_back[['time', 'r4b_p4_pot', 'r4b_p4_temp']].copy(deep=True)
slice4.rename(columns={'r4b_p4_pot':'pot_150', 'r4b_p4_temp':'temp_soil_150'}, inplace=True)
slice4['location'] = 'p43'
slice4['measurement'] = slice4.index

slice5 = row4_back[['time', 'r4b_p5_pot', 'r4b_p5_temp']].copy(deep=True)
slice5.rename(columns={'r4b_p5_pot':'pot_300', 'r4b_p5_temp':'temp_soil_300'}, inplace=True)
slice5['location'] = 'p43'
slice5['measurement'] = slice5.index
if (outputIntermediateFiles):
    row4_back.to_csv('row4_back.csv')
r4b = slice1.append(slice2, ignore_index=True)
r4b = r4b.append(slice3, ignore_index=True)
r4b = r4b.append(slice4, ignore_index=True)
r4b = r4b.append(slice5, ignore_index=True)
r4b = pd.merge(left=r4b, right=treatment, how='inner', on='location')
if (outputIntermediateFiles):
    r4b.to_csv('r4b.tsv', index=False, na_rep='N/A', sep='\t')


# In[ ]:


print('building row4_front frame')
row4_front = pd.read_excel(io='Row4Frnt 18Jan18-1428.xls',
                           sheet_name=0,
                           header=None,
                           skiprows=[0,1,2],
                           names=['time', 
                                  'r4f_p1_vwc', 'r4f_p1_temp', 'r4f_p1_ec',
                                  'r4f_p2_vwc', 'r4f_p2_temp', 'r4f_p2_ec',
                                  'r4f_p3_vwc', 'r4f_p3_temp', 'r4f_p3_ec',
                                  'r4f_p4_630', 'r4f_p4_800', 'r4f_p4_ndvi',
                                  'r4f_p5_targ', 'r4f_p5_body'],
                           usecols=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14])

slice1 = row4_front[['time', 'r4f_p1_vwc', 'r4f_p1_temp', 'r4f_p1_ec']].copy(deep=True)
slice1.rename(columns={'r4f_p1_vwc':'vwc_64', 'r4f_p1_temp':'temp_soil_64', 'r4f_p1_ec':'ec_64'}, inplace=True)
slice1['location'] = 'p41'
slice1['measurement'] = slice1.index

slice2 = row4_front[['time', 'r4f_p2_vwc', 'r4f_p2_temp', 'r4f_p2_ec']].copy(deep=True)
slice2.rename(columns={'r4f_p2_vwc':'vwc_64', 'r4f_p2_temp':'temp_soil_64', 'r4f_p2_ec':'ec_64'}, inplace=True)
slice2['location'] = 'p42'
slice2['measurement'] = slice2.index

slice3 = row4_front[['time', 'r4f_p3_vwc', 'r4f_p3_temp', 'r4f_p3_ec']].copy(deep=True)
slice3.rename(columns={'r4f_p3_vwc':'vwc_64', 'r4f_p3_temp':'temp_soil_64', 'r4f_p3_ec':'ec_64'}, inplace=True)
slice3['location'] = 'p43'
slice3['measurement'] = slice3.index

slice4 = row4_front[['time', 'r4f_p4_630', 'r4f_p4_800', 'r4f_p4_ndvi']].copy(deep=True)
slice4.rename(columns={'r4f_p4_630':'630nm', 'r4f_p4_800':'800nm', 'r4f_p4_ndvi':'ndvi'}, inplace=True)
slice4['location'] = 'p43'
slice4['measurement'] = slice4.index

slice5 = row4_front[['time', 'r4f_p5_targ', 'r4f_p5_body']].copy(deep=True)
slice5.rename(columns={'r4f_p5_targ':'temp_targ', 'r4f_p5_body':'temp_body'}, inplace=True)
slice5['location'] = 'p43'
slice5['measurement'] = slice5.index
if (outputIntermediateFiles):
    row4_front.to_csv('row4_front.csv')
r4f = slice1.append(slice2, ignore_index=True)
r4f = r4f.append(slice3, ignore_index=True)
r4f = r4f.append(slice4, ignore_index=True)
r4f = r4f.append(slice5, ignore_index=True)
r4f = pd.merge(left=r4f, right=treatment, how='inner', on='location')
if (outputIntermediateFiles):
    r4f.to_csv('r4f.tsv', index=False, na_rep='N/A', sep='\t')


# In[ ]:


print('building row5_back frame')
row5_back = pd.read_excel(io='Row5Back 18Jan18-1435.xls',
                          sheet_name=0,
                          header=None,
                          skiprows=[0,1,2],
                          names=['time', 
                                 'r5b_p1_vwc', 'r5b_p1_temp', 'r5b_p1_ec',
                                 'r5b_p2_vwc', 'r5b_p2_temp', 'r5b_p2_ec',
                                 'r5b_p3_pot', 'r5b_p3_temp',
                                 'r5b_p4_pot', 'r5b_p4_temp',
                                 'r5b_p5_pot', 'r5b_p5_temp'],
                          usecols=[0,1,2,3,4,5,6,7,8,9,10,11,12,13])

slice1 = row5_back[['time', 'r5b_p1_vwc', 'r5b_p1_temp', 'r5b_p1_ec']].copy(deep=True)
slice1.rename(columns={'r5b_p1_vwc':'vwc_150', 'r5b_p1_temp':'temp_soil_150', 'r5b_p1_ec':'ec_150'}, inplace=True)
slice1['location'] = 'p53'
slice1['measurement'] = slice1.index

slice2 = row5_back[['time', 'r5b_p2_vwc', 'r5b_p2_temp', 'r5b_p2_ec']].copy(deep=True)
slice2.rename(columns={'r5b_p2_vwc':'vwc_300', 'r5b_p2_temp':'temp_soil_300', 'r5b_p2_ec':'ec_300'}, inplace=True)
slice2['location'] = 'p53'
slice2['measurement'] = slice2.index

slice3 = row5_back[['time', 'r5b_p3_pot', 'r5b_p3_temp']].copy(deep=True)
slice3.rename(columns={'r5b_p3_pot':'pot_64', 'r5b_p3_temp':'temp_soil_64'}, inplace=True)
slice3['location'] = 'p53'
slice3['measurement'] = slice3.index

slice4 = row5_back[['time', 'r5b_p4_pot', 'r5b_p4_temp']].copy(deep=True)
slice4.rename(columns={'r5b_p4_pot':'pot_150', 'r5b_p4_temp':'temp_soil_150'}, inplace=True)
slice4['location'] = 'p53'
slice4['measurement'] = slice4.index

slice5 = row5_back[['time', 'r5b_p5_pot', 'r5b_p5_temp']].copy(deep=True)
slice5.rename(columns={'r5b_p5_pot':'pot_300', 'r5b_p5_temp':'temp_soil_300'}, inplace=True)
slice5['location'] = 'p53'
slice5['measurement'] = slice5.index
if (outputIntermediateFiles):
    row5_back.to_csv('row5_back.csv')
r5b = slice1.append(slice2, ignore_index=True)
r5b = r5b.append(slice3, ignore_index=True)
r5b = r5b.append(slice4, ignore_index=True)
r5b = r5b.append(slice5, ignore_index=True)
r5b = pd.merge(left=r5b, right=treatment, how='inner', on='location')
if (outputIntermediateFiles):
    r5b.to_csv('r5b.tsv', index=False, na_rep='N/A', sep='\t')


# In[ ]:


print('building row5_front frame')
row5_front = pd.read_excel(io='Row5Frnt 18Jan18-1432.xls',
                           sheet_name=0,
                           header=None,
                           skiprows=[0,1,2],
                           names=['time', 
                                  'r5f_p1_vwc', 'r5f_p1_temp', 'r5f_p1_ec',
                                  'r5f_p2_vwc', 'r5f_p2_temp', 'r5f_p2_ec',
                                  'r5f_p3_vwc', 'r5f_p3_temp', 'r5f_p3_ec',
                                  'r5f_p4_630', 'r5f_p4_800', 'r5f_p4_ndvi',
                                  'r5f_p5_targ', 'r5f_p5_body'],
                           usecols=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14])

slice1 = row5_front[['time', 'r5f_p1_vwc', 'r5f_p1_temp', 'r5f_p1_ec']].copy(deep=True)
slice1.rename(columns={'r5f_p1_vwc':'vwc_64', 'r5f_p1_temp':'temp_soil_64', 'r5f_p1_ec':'ec_64'}, inplace=True)
slice1['location'] = 'p51'
slice1['measurement'] = slice1.index

slice2 = row5_front[['time', 'r5f_p2_vwc', 'r5f_p2_temp', 'r5f_p2_ec']].copy(deep=True)
slice2.rename(columns={'r5f_p2_vwc':'vwc_64', 'r5f_p2_temp':'temp_soil_64', 'r5f_p2_ec':'ec_64'}, inplace=True)
slice2['location'] = 'p52'
slice2['measurement'] = slice2.index

slice3 = row5_front[['time', 'r5f_p3_vwc', 'r5f_p3_temp', 'r5f_p3_ec']].copy(deep=True)
slice3.rename(columns={'r5f_p3_vwc':'vwc_64', 'r5f_p3_temp':'temp_soil_64', 'r5f_p3_ec':'ec_64'}, inplace=True)
slice3['location'] = 'p53'
slice3['measurement'] = slice3.index

slice4 = row5_front[['time', 'r5f_p4_630', 'r5f_p4_800', 'r5f_p4_ndvi']].copy(deep=True)
slice4.rename(columns={'r5f_p4_630':'630nm', 'r5f_p4_800':'800nm', 'r5f_p4_ndvi':'ndvi'}, inplace=True)
slice4['location'] = 'p53'
slice4['measurement'] = slice4.index

slice5 = row5_front[['time', 'r5f_p5_targ', 'r5f_p5_body']].copy(deep=True)
slice5.rename(columns={'r5f_p5_targ':'temp_targ', 'r5f_p5_body':'temp_body'}, inplace=True)
slice5['location'] = 'p53'
slice5['measurement'] = slice5.index
if (outputIntermediateFiles):
    row5_front.to_csv('row5_front.csv')
r5f = slice1.append(slice2, ignore_index=True)
r5f = r5f.append(slice3, ignore_index=True)
r5f = r5f.append(slice4, ignore_index=True)
r5f = r5f.append(slice5, ignore_index=True)
r5f = pd.merge(left=r5f, right=treatment, how='inner', on='location')
if (outputIntermediateFiles):
    r5f.to_csv('r5f.tsv', index=False, na_rep='N/A', sep='\t')


# In[ ]:


print('building row6_back frame')
row6_back = pd.read_excel(io='Row6Back 18Jan18-1439.xls',
                          sheet_name=0,
                          header=None,
                          skiprows=[0,1,2],
                          names=['time', 
                                 'r6b_p1_vwc', 'r6b_p1_temp', 'r6b_p1_ec',
                                 'r6b_p2_vwc', 'r6b_p2_temp', 'r6b_p2_ec',
                                 'r6b_p3_pot', 'r6b_p3_temp',
                                 'r6b_p4_pot', 'r6b_p4_temp',
                                 'r6b_p5_pot', 'r6b_p5_temp'],
                          usecols=[0,1,2,3,4,5,6,7,8,9,10,11,12,13])

slice1 = row6_back[['time', 'r6b_p1_vwc', 'r6b_p1_temp', 'r6b_p1_ec']].copy(deep=True)
slice1.rename(columns={'r6b_p1_vwc':'vwc_150', 'r6b_p1_temp':'temp_soil_150', 'r6b_p1_ec':'ec_150'}, inplace=True)
slice1['location'] = 'p63'
slice1['measurement'] = slice1.index

slice2 = row6_back[['time', 'r6b_p2_vwc', 'r6b_p2_temp', 'r6b_p2_ec']].copy(deep=True)
slice2.rename(columns={'r6b_p2_vwc':'vwc_300', 'r6b_p2_temp':'temp_soil_300', 'r6b_p2_ec':'ec_300'}, inplace=True)
slice2['location'] = 'p63'
slice2['measurement'] = slice2.index

slice3 = row6_back[['time', 'r6b_p3_pot', 'r6b_p3_temp']].copy(deep=True)
slice3.rename(columns={'r6b_p3_pot':'pot_64', 'r6b_p3_temp':'temp_soil_64'}, inplace=True)
slice3['location'] = 'p63'
slice3['measurement'] = slice3.index

slice4 = row6_back[['time', 'r6b_p4_pot', 'r6b_p4_temp']].copy(deep=True)
slice4.rename(columns={'r6b_p4_pot':'pot_150', 'r6b_p4_temp':'temp_soil_150'}, inplace=True)
slice4['location'] = 'p63'
slice4['measurement'] = slice4.index

slice5 = row6_back[['time', 'r6b_p5_pot', 'r6b_p5_temp']].copy(deep=True)
slice5.rename(columns={'r6b_p5_pot':'pot_300', 'r6b_p5_temp':'temp_soil_300'}, inplace=True)
slice5['location'] = 'p63'
slice5['measurement'] = slice5.index
if (outputIntermediateFiles):
    row6_back.to_csv('row6_back.csv')
r6b = slice1.append(slice2, ignore_index=True)
r6b = r6b.append(slice3, ignore_index=True)
r6b = r6b.append(slice4, ignore_index=True)
r6b = r6b.append(slice5, ignore_index=True)
r6b = pd.merge(left=r6b, right=treatment, how='inner', on='location')
if (outputIntermediateFiles):
    r6b.to_csv('r6b.tsv', index=False, na_rep='N/A', sep='\t')


# In[ ]:


print('building row6_front frame')
row6_front = pd.read_excel(io='Row6Frnt 18Jan18-1437.xls',
                           sheet_name=0,
                           header=None,
                           skiprows=[0,1,2],
                           names=['time', 
                                  'r6f_p1_vwc', 'r6f_p1_temp', 'r6f_p1_ec',
                                  'r6f_p2_vwc', 'r6f_p2_temp', 'r6f_p2_ec',
                                  'r6f_p3_vwc', 'r6f_p3_temp', 'r6f_p3_ec',
                                  'r6f_p4_630', 'r6f_p4_800', 'r6f_p4_ndvi',
                                  'r6f_p5_targ', 'r6f_p5_body'],
                           usecols=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14])

slice1 = row6_front[['time', 'r6f_p1_vwc', 'r6f_p1_temp', 'r6f_p1_ec']].copy(deep=True)
slice1.rename(columns={'r6f_p1_vwc':'vwc_64', 'r6f_p1_temp':'temp_soil_64', 'r6f_p1_ec':'ec_64'}, inplace=True)
slice1['location'] = 'p61'
slice1['measurement'] = slice1.index

slice2 = row6_front[['time', 'r6f_p2_vwc', 'r6f_p2_temp', 'r6f_p2_ec']].copy(deep=True)
slice2.rename(columns={'r6f_p2_vwc':'vwc_64', 'r6f_p2_temp':'temp_soil_64', 'r6f_p2_ec':'ec_64'}, inplace=True)
slice2['location'] = 'p62'
slice2['measurement'] = slice2.index

slice3 = row6_front[['time', 'r6f_p3_vwc', 'r6f_p3_temp', 'r6f_p3_ec']].copy(deep=True)
slice3.rename(columns={'r6f_p3_vwc':'vwc_64', 'r6f_p3_temp':'temp_soil_64', 'r6f_p3_ec':'ec_64'}, inplace=True)
slice3['location'] = 'p63'
slice3['measurement'] = slice3.index

slice4 = row6_front[['time', 'r6f_p4_630', 'r6f_p4_800', 'r6f_p4_ndvi']].copy(deep=True)
slice4.rename(columns={'r6f_p4_630':'630nm', 'r6f_p4_800':'800nm', 'r6f_p4_ndvi':'ndvi'}, inplace=True)
slice4['location'] = 'p63'
slice4['measurement'] = slice4.index

slice5 = row6_front[['time', 'r6f_p5_targ', 'r6f_p5_body']].copy(deep=True)
slice5.rename(columns={'r6f_p5_targ':'temp_targ', 'r6f_p5_body':'temp_body'}, inplace=True)
slice5['location'] = 'p63'
slice5['measurement'] = slice5.index
if (outputIntermediateFiles):
    row6_front.to_csv('row6_front.csv')
r6f = slice1.append(slice2, ignore_index=True)
r6f = r6f.append(slice3, ignore_index=True)
r6f = r6f.append(slice4, ignore_index=True)
r6f = r6f.append(slice5, ignore_index=True)
r6f = pd.merge(left=r6f, right=treatment, how='inner', on='location')
if (outputIntermediateFiles):
    r6f.to_csv('r6f.tsv', index=False, na_rep='N/A', sep='\t')


# In[ ]:


print('building row7 frame')
row7 = pd.read_excel(io='Row7 18Jan18-1441.xls',
                     sheet_name=0,
                     header=None,
                     skiprows=[0,1,2],
                     names=['time', 
                            'r7_p1_vwc', 'r7_p1_temp', 'r7_p1_ec',
                            'r7_p2_vwc', 'r7_p2_temp', 'r7_p2_ec',
                            'r7_p3_vwc', 'r7_p3_temp', 'r7_p3_ec',
                            'r7_p4_630', 'r7_p4_800', 'r7_p4_ndvi',
                            'r7_p5_targ', 'r7_p5_body'],
                     usecols=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14])

slice1 = row7[['time', 'r7_p1_vwc', 'r7_p1_temp', 'r7_p1_ec']].copy(deep=True)
slice1.rename(columns={'r7_p1_vwc':'vwc_64', 'r7_p1_temp':'temp_soil_64', 'r7_p1_ec':'ec_64'}, inplace=True)
slice1['location'] = 'p71'
slice1['measurement'] = slice1.index

slice2 = row7[['time', 'r7_p2_vwc', 'r7_p2_temp', 'r7_p2_ec']].copy(deep=True)
slice2.rename(columns={'r7_p2_vwc':'vwc_64', 'r7_p2_temp':'temp_soil_64', 'r7_p2_ec':'ec_64'}, inplace=True)
slice2['location'] = 'p72'
slice2['measurement'] = slice2.index

slice3 = row7[['time', 'r7_p3_vwc', 'r7_p3_temp', 'r7_p3_ec']].copy(deep=True)
slice3.rename(columns={'r7_p3_vwc':'vwc_64', 'r7_p3_temp':'temp_soil_64', 'r7_p3_ec':'ec_64'}, inplace=True)
slice3['location'] = 'p73'
slice3['measurement'] = slice3.index

slice4 = row7[['time', 'r7_p4_630', 'r7_p4_800', 'r7_p4_ndvi']].copy(deep=True)
slice4.rename(columns={'r7_p4_630':'630nm', 'r7_p4_800':'800nm', 'r7_p4_ndvi':'ndvi'}, inplace=True)
slice4['location'] = 'p73'
slice4['measurement'] = slice4.index

slice5 = row7[['time', 'r7_p5_targ', 'r7_p5_body']].copy(deep=True)
slice5.rename(columns={'r7_p5_targ':'temp_targ', 'r7_p5_body':'temp_body'}, inplace=True)
slice5['location'] = 'p73'
slice5['measurement'] = slice5.index
if (outputIntermediateFiles):
    row7.to_csv('row7.csv')
r7 = slice1.append(slice2, ignore_index=True)
r7 = r7.append(slice3, ignore_index=True)
r7 = r7.append(slice4, ignore_index=True)
r7 = r7.append(slice5, ignore_index=True)
r7 = pd.merge(left=r7, right=treatment, how='inner', on='location')
if (outputIntermediateFiles):
    r7.to_csv('r7.tsv', index=False, na_rep='N/A', sep='\t')


# In[ ]:


print('building row8 frame')
row8 = pd.read_excel(io='Row8 18Jan18-1443.xls',
                     sheet_name=0,
                     header=None,
                     skiprows=[0,1,2],
                     names=['time', 
                            'r8_p1_vwc', 'r8_p1_temp', 'r8_p1_ec',
                            'r8_p2_vwc', 'r8_p2_temp', 'r8_p2_ec',
                            'r8_p3_vwc', 'r8_p3_temp', 'r8_p3_ec',
                            'r8_p4_630', 'r8_p4_800', 'r8_p4_ndvi',
                            'r8_p5_targ', 'r8_p5_body'],
                     usecols=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14])

slice1 = row8[['time', 'r8_p1_vwc', 'r8_p1_temp', 'r8_p1_ec']].copy(deep=True)
slice1.rename(columns={'r8_p1_vwc':'vwc_64', 'r8_p1_temp':'temp_soil_64', 'r8_p1_ec':'ec_64'}, inplace=True)
slice1['location'] = 'p81'
slice1['measurement'] = slice1.index

slice2 = row8[['time', 'r8_p2_vwc', 'r8_p2_temp', 'r8_p2_ec']].copy(deep=True)
slice2.rename(columns={'r8_p2_vwc':'vwc_64', 'r8_p2_temp':'temp_soil_64', 'r8_p2_ec':'ec_64'}, inplace=True)
slice2['location'] = 'p82'
slice2['measurement'] = slice2.index

slice3 = row8[['time', 'r8_p3_vwc', 'r8_p3_temp', 'r8_p3_ec']].copy(deep=True)
slice3.rename(columns={'r8_p3_vwc':'vwc_64', 'r8_p3_temp':'temp_soil_64', 'r8_p3_ec':'ec_64'}, inplace=True)
slice3['location'] = 'p83'
slice3['measurement'] = slice3.index

slice4 = row8[['time', 'r8_p4_630', 'r8_p4_800', 'r8_p4_ndvi']].copy(deep=True)
slice4.rename(columns={'r8_p4_630':'630nm', 'r8_p4_800':'800nm', 'r8_p4_ndvi':'ndvi'}, inplace=True)
slice4['location'] = 'p83'
slice4['measurement'] = slice4.index

slice5 = row8[['time', 'r8_p5_targ', 'r8_p5_body']].copy(deep=True)
slice5.rename(columns={'r8_p5_targ':'temp_targ', 'r8_p5_body':'temp_body'}, inplace=True)
slice5['location'] = 'p83'
slice5['measurement'] = slice5.index
if (outputIntermediateFiles):
    row8.to_csv('row8.csv')
r8 = slice1.append(slice2, ignore_index=True)
r8 = r8.append(slice3, ignore_index=True)
r8 = r8.append(slice4, ignore_index=True)
r8 = r8.append(slice5, ignore_index=True)
r8 = pd.merge(left=r8, right=treatment, how='inner', on='location')
if (outputIntermediateFiles):
    r8.to_csv('r8.tsv', index=False, na_rep='N/A', sep='\t')


# In[ ]:


print('building row9 frame')
row9 = pd.read_excel(io='Row9 18Jan18-1445.xls',
                     sheet_name=0,
                     header=None,
                     skiprows=[0,1,2],
                     names=['time', 
                            'r9_p1_vwc', 'r9_p1_temp', 'r9_p1_ec',
                            'r9_p2_vwc', 'r9_p2_temp', 'r9_p2_ec',
                            'r9_p3_vwc', 'r9_p3_temp', 'r9_p3_ec',
                            'r9_p4_630', 'r9_p4_800', 'r9_p4_ndvi',
                            'r9_p5_targ', 'r9_p5_body'],
                     usecols=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14])

slice1 = row9[['time', 'r9_p1_vwc', 'r9_p1_temp', 'r9_p1_ec']].copy(deep=True)
slice1.rename(columns={'r9_p1_vwc':'vwc_64', 'r9_p1_temp':'temp_soil_64', 'r9_p1_ec':'ec_64'}, inplace=True)
slice1['location'] = 'p91'
slice1['measurement'] = slice1.index

slice2 = row9[['time', 'r9_p2_vwc', 'r9_p2_temp', 'r9_p2_ec']].copy(deep=True)
slice2.rename(columns={'r9_p2_vwc':'vwc_64', 'r9_p2_temp':'temp_soil_64', 'r9_p2_ec':'ec_64'}, inplace=True)
slice2['location'] = 'p92'
slice2['measurement'] = slice2.index

slice3 = row9[['time', 'r9_p3_vwc', 'r9_p3_temp', 'r9_p3_ec']].copy(deep=True)
slice3.rename(columns={'r9_p3_vwc':'vwc_64', 'r9_p3_temp':'temp_soil_64', 'r9_p3_ec':'ec_64'}, inplace=True)
slice3['location'] = 'p93'
slice3['measurement'] = slice3.index

slice4 = row9[['time', 'r9_p4_630', 'r9_p4_800', 'r9_p4_ndvi']].copy(deep=True)
slice4.rename(columns={'r9_p4_630':'630nm', 'r9_p4_800':'800nm', 'r9_p4_ndvi':'ndvi'}, inplace=True)
slice4['location'] = 'p93'
slice4['measurement'] = slice4.index

slice5 = row9[['time', 'r9_p5_targ', 'r9_p5_body']].copy(deep=True)
slice5.rename(columns={'r9_p5_targ':'temp_targ', 'r9_p5_body':'temp_body'}, inplace=True)
slice5['location'] = 'p93'
slice5['measurement'] = slice5.index
if (outputIntermediateFiles):
    row9.to_csv('row9.csv')
r9 = slice1.append(slice2, ignore_index=True)
r9 = r9.append(slice3, ignore_index=True)
r9 = r9.append(slice4, ignore_index=True)
r9 = r9.append(slice5, ignore_index=True)
r9 = pd.merge(left=r9, right=treatment, how='inner', on='location')
if (outputIntermediateFiles):
    r9.to_csv('r9.tsv', index=False, na_rep='N/A', sep='\t')


# In[ ]:

os.chdir('../results')
print('building allrows frame')
allrows = r1f.append(r2, ignore_index=True)
allrows = allrows.append(r3, ignore_index=True)
allrows = allrows.append(r4b, ignore_index=True)
allrows = allrows.append(r4f, ignore_index=True)
allrows = allrows.append(r5b, ignore_index=True)
allrows = allrows.append(r5f, ignore_index=True)
allrows = allrows.append(r6b, ignore_index=True)
allrows = allrows.append(r6f, ignore_index=True)
allrows = allrows.append(r7, ignore_index=True)
allrows = allrows.append(r8, ignore_index=True)
allrows = allrows.append(r9, ignore_index=True)
allrows.to_csv('allrows.tsv', index=False, na_rep='N/A', sep='\t')
print('done')

