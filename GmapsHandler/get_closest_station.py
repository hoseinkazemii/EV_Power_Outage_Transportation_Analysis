
# Function to determine closest station with required plug type
def get_closest_station(row, plug_type, stations):

    sorted_stations = stations.get_group(row['destination']).sort_values(by='distance')
    for index, station in sorted_stations.iterrows():
        if station[plug_type] > 0:
            return station['destination'], station['distance']

    return None, None




# def get_closest_station(row):
#     sorted_stations = stations.get_group(row['origin_latitude']).sort_values(by='distance')
#     plug_types = unique_make_model_df[
#         (unique_make_model_df['make'] == row['make']) &
#         (unique_make_model_df['model'] == row['model'])
#     ]
#     for plug in ['J1772', 'TESLA', 'CHADEMO']:
#         if plug_types[plug].iloc[0] > 0:
#             for index, station in sorted_stations.iterrows():
#                 if station[plug] > 0:
#                     return station['destination'], station['distance']
#     return None, None