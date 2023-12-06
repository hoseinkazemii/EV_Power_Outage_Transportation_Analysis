import pandas as pd
import random

# Load the CSV file
file_path = 'path/to/your/csv_file.csv'
data = pd.read_csv(file_path)

# Define boundaries of Los Angeles city
# Replace these coordinates with the actual boundaries
la_city_boundaries = {
    'min_lat': 34.0522, 'max_lat': 34.3373,
    'min_lon': -118.6835, 'max_lon': -118.1553
}

# Function to generate random latitude and longitude within LA city boundaries
def generate_random_coordinates():
    return {
        'latitude': random.uniform(la_city_boundaries['min_lat'], la_city_boundaries['max_lat']),
        'longitude': random.uniform(la_city_boundaries['min_lon'], la_city_boundaries['max_lon'])
    }

# Apply random coordinates to each row
data['latitude'] = data.apply(lambda _: generate_random_coordinates()['latitude'], axis=1)
data['longitude'] = data.apply(lambda _: generate_random_coordinates()['longitude'], axis=1)

# Save the updated data to a new CSV file
data.to_csv('path/to/save/updated_file.csv', index=False)
