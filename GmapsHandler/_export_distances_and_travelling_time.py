from ._calculate_distance_and_travelling_time import calculate_distance_and_travelling_time
from ._sample_cars import sample_cars

import re
import pandas as pd
import numpy as np
import math


def export_distances_and_travelling_time(**params):

    verbose = params.get("verbose")
    percentage_to_drop = params.get("percentage_to_drop")
    num_buildings_from_each_FIPS = params.get("num_buildings_from_each_FIPS")
 
    if verbose:
        print(f"Calculating and exproting the distances and traveling time between EVs and EV Charging Stations")

    EVs = pd.read_csv(f'./Data/Electric_Vehicle_Location_WA.csv')
    EVs = EVs.dropna(subset=['City'])
    EVs = EVs[EVs['City'].str.contains('Seattle', case=False, regex=True)]

    # Parsing the "Vehicle Location" column into latitude and longitude
    EVs['Longitude'] = EVs['Vehicle Location'].str.extract(r'POINT \((-?\d+\.\d+) \d+\.\d+\)')
    EVs['Latitude'] = EVs['Vehicle Location'].str.extract(r'POINT \(-?\d+\.\d+ (\d+\.\d+)\)')
    EVs = sample_cars(EVs, **params)

    EVCSs = pd.read_csv(f'./Data/EV_Charging_Stations.csv', dtype={'Longitude': float, 'Latitude': float, 'City': str}, low_memory=False)
    EVCSs = EVCSs.rename(columns={'Station Name': 'StationName', 'EV Level2 EVSE Num':'Level2', 'EV DC Fast Count':'DCFast', 'EV Connector Types':'ConnectorTypes'})
    EVCSs = EVCSs.dropna(subset=['City'])
    EVCSs = EVCSs[EVCSs['City'].str.contains('Seattle', case=False, regex=True)].iloc[:10,:] # REMOVE ILOC
    EVCSs['ConnectorTypes'] = EVCSs['ConnectorTypes'].apply(lambda x: x.split())

    EVCSs['CHADEMO'] = ''
    EVCSs['J1772'] = ''
    EVCSs['TESLA'] = ''

    for index, row in EVCSs.iterrows():
        connector_types = row['ConnectorTypes']
        level2 = row['Level2']
        dfast = row['DCFast']
        
        if 'J1772' in connector_types or 'J1772COMBO' in connector_types:
            if 'TESLA' in connector_types:
                if pd.notnull(level2) and level2 != 0:
                    if level2 % 2 == 0:  # Check if Level2 is even
                        EVCSs.at[index, 'J1772'] = level2 // 2
                        EVCSs.at[index, 'TESLA'] = level2 // 2
                    else:
                        EVCSs.at[index, 'J1772'] = level2 // 2
                        EVCSs.at[index, 'TESLA'] = (level2 // 2) + 1
                else:
                    EVCSs.at[index, 'J1772'] = level2 if pd.notnull(level2) else ''
                    EVCSs.at[index, 'TESLA'] = dfast
            else:
                EVCSs.at[index, 'J1772'] = level2 if pd.notnull(level2) else ''
                
        if 'CHADEMO' in connector_types:
            EVCSs.at[index, 'CHADEMO'] = dfast
            
        if 'TESLA' in connector_types and ('J1772' not in connector_types and 'J1772COMBO' not in connector_types):
            if pd.notnull(level2) and level2 != 0:
                EVCSs.at[index, 'TESLA'] = level2
            else:
                EVCSs.at[index, 'TESLA'] = dfast

    columns_to_replace = ['J1772', 'CHADEMO', 'TESLA']
    EVCSs[columns_to_replace] = EVCSs[columns_to_replace].fillna(0)

    np.random.seed(42)
    num_rows_to_drop = int(len(EVCSs) * percentage_to_drop)
    random_indices = np.random.choice(EVCSs.index, num_rows_to_drop, replace=False)
    EVCSs = EVCSs.drop(random_indices)

    # Create an empty DataFrame to store the distances and travelling time
    distances_and_traveling_time = pd.DataFrame(columns=['origin_latitude','origin_longitude','make','model','destination','J1772','TESLA','CHADEMO','distance','traveling_time'])

    if verbose:
        print("Calculating distances and travelling time through driving mode...")

    # Iterate through the points in both datasets and calculate distances        
    for _, row1 in EVs.iterrows():
        for _, row2 in EVCSs.iterrows():
            distance, traveling_time = calculate_distance_and_travelling_time(row1, row2,**params)
            if distance is not None:
                new_row = pd.DataFrame({'origin_latitude': [row1.Latitude], 'origin_longitude': [row1.Longitude], 
                                        'destination': [row2.StationName], 'make': [row1.Make], 'model': [row1.Model],
                                        'J1772': [row2.J1772], 'TESLA': [row2.TESLA], 'CHADEMO':[row2.CHADEMO], 'distance': [distance], 'traveling_time': [traveling_time]})
                distances_and_traveling_time = pd.concat([distances_and_traveling_time, new_row], ignore_index=True)

    # Now we have a DataFrame 'distances' with distances between all pairs of points
    distances_and_traveling_time.to_csv(f'./Output/Distances_and_traveling_time_between_EVs_and_{int(100*(1-percentage_to_drop))}_percent_Charging_Stations.csv', index=False)