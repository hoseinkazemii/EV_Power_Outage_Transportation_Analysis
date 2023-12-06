from GmapsHandler import get_closest_station, extract_col_numerical_part

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import random


def plot_queue_length(**params):

    verbose = params.get("verbose")
    charging_station = params.get("charging_station")
    plot_x_lim = params.get("plot_x_lim")
    total_simulation_time = params.get("total_simulation_time")
    percentage_to_drop = params.get("percentage_to_drop")
    charging_times = params.get("charging_times")
    fig_font_size = params.get("fig_font_size")


    if verbose:
        print("Simulating the queue...")


    ev_data = pd.read_csv(f'./Output/Distances_and_traveling_time_between_EVs_and_{int(100*(1-percentage_to_drop))}_percent_Charging_Stations.csv')
    unique_make_model_df = pd.read_csv('./Data/unique_make_model_pairs.csv')


    # Modify traveling_time column
    ev_data =  extract_col_numerical_part(ev_data, **params)

    # Group stations by their location
    stations = ev_data.groupby(['destination'])

    # Simulate queue length for a specific charging station
    station_distances = ev_data[ev_data['destination'] == charging_station]


    # Simulate charging queue over the hours
    queue_length = defaultdict(int)
    total_simulation_time = total_simulation_time * 60
    for time_minute in range(total_simulation_time):
        # Determine cars arriving at this time
        arriving_cars = station_distances[
            (station_distances['traveling_time'] <= time_minute) & 
            (station_distances['traveling_time'] > time_minute - 1)
        ]



        # Queue cars that arrive
        for index, car in arriving_cars.iterrows():
            plug_types = unique_make_model_df[
                (unique_make_model_df['make'] == car['make']) & 
                (unique_make_model_df['model'] == car['model'])
            ]
            for plug in ['J1772', 'TESLA', 'CHADEMO']:
                if plug_types[plug].iloc[0] > 0:
                    dest, distance = get_closest_station(car, plug, stations)
                    if dest is not None:
                        queue_length[(time_minute, dest)] += 1
                        break

        # Cars finishing charging
        finished_cars = [key for key in queue_length.keys() if key[0] + charging_times[plug] <= time_minute]
        for car in finished_cars:
            del queue_length[car]

    # Plot queue length over time
    time_slots = sorted(set([key[0] for key in queue_length.keys()]))
    queue_at_station = [queue_length[(time, charging_station)] for time in time_slots]

    plt.figure(figsize=(10, 6))
    plt.plot(time_slots, queue_at_station, marker='o')
    plt.yticks(np.arange(1, max(queue_at_station) + 1, 1))
    plt.xlabel('Time (minutes)', fontsize=fig_font_size)
    plt.xlim(plot_x_lim)
    plt.ylabel('Queue Length', fontsize=fig_font_size)
    plt.title(f'Queue Length at Charging Station "{charging_station}"', fontsize=fig_font_size)
    plt.grid(True, axis='y')

    if percentage_to_drop == 0:
        plt.savefig(f'./Output/Queue_Length_Before_Outage_{charging_station}.jpg', dpi=300)
    else:
        plt.savefig(f'./Output/Queue_Length_{int(100*percentage_to_drop)}_Percent_Outage_{charging_station}.jpg',dpi=300)
    
    plt.show()