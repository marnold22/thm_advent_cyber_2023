#!/usr/env/bin python3

import pandas as pd
import matplotlib.pyplot as plt

# QUESTION 1
df = pd.read_csv('network_traffic.csv')
print(df.count())

# QUESTION 2
df= pd.read_csv('network_traffic.csv')
print(df['Source'].value_counts())

# QUESTION 3
df = pd.read_csv('network_traffic.csv')
print(df['Protocol'].value_counts())