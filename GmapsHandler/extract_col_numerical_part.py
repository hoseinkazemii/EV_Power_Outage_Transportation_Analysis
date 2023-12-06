
def extract_col_numerical_part(df, **params):

	verbose = params.get("verbose")

	if verbose:
		print("Extracting the numerical part of traveling_time column...")


	# Extract numerical part and convert to integer
	df['traveling_time'] = df['traveling_time'].str.split(' ').str[0].astype(int)

	return df