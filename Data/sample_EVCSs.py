import pandas as pd
import numpy as np

EVCSs = pd.read_csv(f'./EV_Charging_Stations.csv', dtype={'Longitude': float, 'Latitude': float, 'City': str}, low_memory=False)
EVCSs = EVCSs.rename(columns={'Station Name': 'StationName', 'EV Level2 EVSE Num':'Level2', 'EV DC Fast Count':'DCFast', 'EV Connector Types':'ConnectorTypes'})
EVCSs = EVCSs.dropna(subset=['City'])
# EVCSs = EVCSs[EVCSs['City'].str.contains('Seattle', case=False, regex=True)].iloc[:10,:] # REMOVE ILOC
EVCSs = EVCSs.sample(n=48)

EVCSs.to_csv("EVCSs.csv", index=False)