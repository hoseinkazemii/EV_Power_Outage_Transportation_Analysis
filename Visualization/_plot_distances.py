import pandas as pd
import matplotlib.pyplot as plt

def plot_distances(**params):
    
    verbose = params.get("verbose")
    percentage_to_drop = params.get("percentage_to_drop")

    if verbose:
        print("Plotting distances histogram...")


    df = pd.read_csv(f'./Output/Distances_and_traveling_time_between_EVs_and_{int(100*(1-percentage_to_drop))}_percent_Charging_Stations.csv')

    # Create a single subplot
    fig, ax = plt.subplots(figsize=(12, 4))
    
    min_distance = df.groupby(['origin_longitude', 'origin_latitude'])['distance'].min()

    # Convert x_values to a list and plot the data side by side
    x_values = list(range(1, len(min_distance) + 1))
    bar_width = 0.4  # Adjust this value for the desired gap between bars
    ax.bar([x for x in x_values], min_distance, width=bar_width)

    ax.set_xlabel('EV Number')
    ax.set_ylabel('Minimum Distance (km)')
    ax.set_xticks(x_values)
    max_value = int(max(min_distance))
    y_ticks = range(5, max_value + 5, 5) if max_value >= 5 else range(1, max_value + 1)
    ax.set_ylim(0, max_value + 5)
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_ticks)
    plt.tight_layout()
    plt.grid(True, axis='y')

    if percentage_to_drop == 0:
        plt.savefig(f'./Output/Minimum_Distance_Before_Outage.jpg',dpi=300)
    else:
        plt.savefig(f'./Output/Minimum_Distance_During_{int(100*percentage_to_drop)}_Percent_Outage.jpg',dpi=300)

    plt.show()