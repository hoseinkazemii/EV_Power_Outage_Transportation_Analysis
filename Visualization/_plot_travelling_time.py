import pandas as pd
import matplotlib.pyplot as plt

def plot_travelling_time(**params):
    
    verbose = params.get("verbose")
    percentage_to_drop = params.get("percentage_to_drop")
    fig_font_size = params.get("fig_font_size")

    if verbose:
        print("Plotting distances histogram...")

    df = pd.read_csv(f'./Output/Distances_and_traveling_time_between_EVs_and_{int(100*(1-percentage_to_drop))}_percent_Charging_Stations.csv')

    # Create a single subplot
    fig, ax = plt.subplots(figsize=(12, 4))
    
    # Calculate average distances for each unique pair
    df['traveling_time'] = df['traveling_time'].str.extract('(\d+)').astype(int)
    min_traveling_time = df.groupby(['origin_longitude', 'origin_latitude'])['traveling_time'].min()

    # Convert x_values to a list and plot the data side by side
    x_values = list(range(1, len(min_traveling_time) + 1))
    bar_width = 0.4  # Adjust this value for the desired gap between bars
    ax.bar([x for x in x_values], min_traveling_time, width=bar_width)

    ax.set_xlabel('EV Number', fontsize=fig_font_size)
    ax.set_ylabel('Minimum Traveling Time (min)', fontsize=fig_font_size)
    ax.set_xticks(x_values)
    # ax.set_ylim(0, 25)
    # ax.set_yticks(range(0, 25))
    max_value = max(min_traveling_time)
    y_ticks = range(5, max_value + 5, 5) if max_value >= 5 else range(1, max_value + 1)
    ax.set_ylim(0, max_value + 5)
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_ticks)
    plt.tight_layout()
    plt.grid(True, axis='y')

    if percentage_to_drop == 0:
        plt.savefig(f'./Output/Minimum_Travelling_Time_Before_Outage.jpg',dpi=300)
    else:
        plt.savefig(f'./Output/Minimum_Travelling_Time_During_{int(100*percentage_to_drop)}_Percent_Outage.jpg',dpi=300)

    plt.show()