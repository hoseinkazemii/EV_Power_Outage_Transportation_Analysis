import pandas as pd
import numpy as np
import random

def sample_cars(df, **params):

	verbose = params.get("verbose")
	num_sample_cars = params.get("num_sample_cars")

	if verbose:
		print(f"Getting {num_sample_cars} sample EVs.")

	sampled_EV_locations = df[['Latitude', 'Longitude']].drop_duplicates().sample(n=num_sample_cars)
	df = pd.merge(df, sampled_EV_locations, on=['Latitude', 'Longitude'], how='inner')
	# Drop duplicates based on 'Longitude' and 'Latitude'
	unique_pairs = df.drop_duplicates(subset=['Longitude', 'Latitude'])
	# Select a random row for each unique pair
	random_indices = unique_pairs.groupby(['Longitude', 'Latitude']).apply(lambda x: np.random.choice(x.index)).values
	# Dataframe with randomly selected rows
	df = df.loc[random_indices]

	return df