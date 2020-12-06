#!/usr/bin/env python
# coding: utf-8

# In[66]:


import pandas as pd
import numpy as np


# In[67]:


data = pd.read_csv("testData.csv")
data


# In[68]:


def get_responses(data):
    return data[['img', 'earlyResp', 'resp', 'lateResp']]


# In[69]:


def fill_row(row):
    if np.isnan(row['resp']):
        if not np.isnan(row['lateResp']):
            return row['lateResp']
        elif not np.isnan(row['earlyResp']):
            return row['earlyResp']
        else:
            return -1
    return row['resp']


# In[70]:


def clear_blanks(tbl):
    tbl['resp'] = tbl.apply(fill_row, axis=1)
    return tbl[tbl['resp'] != -1][['img', 'resp']]


# In[86]:


valid_resp = clear_blanks(get_responses(data))
valid_resp.loc[146, 'resp'] = 2
valid_resp


# In[87]:


def score_correctness(row):
    if 'a' in row['img']:
        if row['resp'] == 4 or row['resp'] == 3:
            return 1
        elif row['resp'] == 1 or row['resp'] == 2:
            return 0
    elif 'b' in row['img'] or 'foil' in row['img']:
        if row['resp'] == 4 or row['resp'] == 3:
            return 0
        elif row['resp'] == 1 or row['resp'] == 2:
            return 1


# In[88]:


def score_confidence(row):
    if row['resp'] == 1 or row['resp'] == 4:
        return 1
    else:
        return 0


# In[89]:


valid_resp['correctness'] = valid_resp.apply(score_correctness, axis=1)


# In[90]:


valid_resp


# In[91]:


valid_resp['confidence'] = valid_resp.apply(score_confidence, axis = 1)
valid_resp


# In[92]:


lures = valid_resp[valid_resp['img'].str.contains('b')]
targets = valid_resp[valid_resp['img'].str.contains('a')]
novels = valid_resp[valid_resp['img'].str.contains('foil')]


# In[108]:


lures


# In[109]:


targets


# In[95]:


novels


# In[96]:


output = {'total': np.zeros(6), 
         'percent': np.zeros(6),
         'high_conf': np.zeros(6),
         'low_conf': np.zeros(6),
          'high_conf_pct': np.zeros(6),
          'low_conf_pct': np.zeros(6)}
output_tbl = pd.DataFrame(output, index=["lure_hit", "lure_miss",
                                        "target_hit", "target_miss",
                                        "novel_hit", "novel_miss"])
output_tbl


# In[116]:


def compute_rows(tbl):
    """Returns a 2-item list RES of hit/miss data for a lure, target, or novel table.
    
    RES[0] is the hits. RES[1] is the misses.
    """
    hit_res = [0] * 6
    miss_res = [0] * 6
    hits = tbl[tbl['correctness'] == 1]
    misses = tbl[tbl['correctness'] == 0]
    # counts
    num_hits = len(hits.index)
    num_misses = len(misses.index)
    print(num_hits, num_misses)
    # percentages
    pct_hits = num_hits/(num_hits + num_misses)
    pct_misses = num_misses/(num_hits + num_misses)
    # confidence counts
    num_hc_hit = sum(hits['confidence'])
    num_lc_hit = num_hits - num_hc_hit
    num_hc_miss = sum(misses['confidence'])
    num_lc_miss = num_misses - num_hc_miss
    # confidence percents
    pct_hc_hit = num_hc_hit/num_hits
    pct_lc_hit = num_lc_hit/num_hits
    pct_hc_miss = num_hc_miss/num_misses
    pct_lc_miss = num_lc_miss/num_misses
    return [[num_hits, pct_hits, num_hc_hit, num_lc_hit, pct_hc_hit, pct_lc_hit], 
           [num_misses, pct_misses, num_hc_miss, num_lc_miss, pct_hc_miss, pct_lc_miss]]


# In[117]:


lure_res = compute_rows(lures)
target_res = compute_rows(targets)
novel_res = compute_rows(novels)


# In[123]:


output_tbl.loc['lure_hit'] = lure_res[0]
output_tbl.loc['lure_miss'] = lure_res[1]
output_tbl.loc['target_hit'] = target_res[0]
output_tbl.loc['target_miss'] = target_res[1]
output_tbl.loc['novel_hit'] = novel_res[0]
output_tbl.loc['novel_miss'] = novel_res[1]


# In[124]:


output_tbl



