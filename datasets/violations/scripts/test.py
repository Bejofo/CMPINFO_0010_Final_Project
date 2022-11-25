import numpy as np
import pandas as pd
import re
import itertools

business_list = pd.read_csv("/mnt/c/Users/thxs4/Downloads/business_list.csv")
geocoded_food_facilities = pd.read_csv("/mnt/c/Users/thxs4/Downloads/geo_coded.csv")

# def address_to_id(street_number,route,postal_code):


def compare_names(A,B):
  if A==B:
    return True
  if any( normalize_names(x) == normalize_names(y) for x,y in itertools.prod(A.split('/'),B.split('/'))):
    return True
  return False


def normalize_names(name):
  name = name.replace('é','e')
  name = re.sub('[^A-Za-z0-9]+', '', name.lower())
  suffxies = ['bar','restaurant','restaurante','cafe','bbq','diner']
  for s in suffxies:
    if name.endswith(s):
      name = name[:-len(s)]
  prefix = ['the']
  for p in prefix:
    if name.startswith(p):
      name = name[len(p):]
  return name

def address_to_id(R):
  fac_name = normalize_names(R['name'])
  street_number = R['street_number']
  postal_code = R['postal_code']
  # print(street_number,postal_code,fac_name)
  query = "num == @street_number and zip==@postal_code"
  row = geocoded_food_facilities.query(query)

  if row.shape[0] == 1:
    return row.iloc[0]['id']

  if row.shape[0] == 0:
    return
  
  if row.shape[0] > 1:
    for r in row.iterrows():
      if normalize_names(r[1]['facility_name']) == fac_name:
        return r[1]['id']

  return None

ids = business_list.apply(address_to_id,axis=1)
print(business_list[ids.isna()][['name','postal_code','street_number']])
print(ids.isna().sum())
