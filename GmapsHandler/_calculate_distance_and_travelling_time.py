import googlemaps



# Function to calculate distance using Google Maps API
def calculate_distance_and_travelling_time(point1, point2, **params):

    api_key = params.get("api_key")


    gmaps = googlemaps.Client(key=api_key)

    result = gmaps.distance_matrix((point1['Latitude'], point1['Longitude']),
                                    (point2['Latitude'], point2['Longitude']),
                                    mode='driving')  # We can change the mode to 'walking', 'bicycling', etc.

    if result['status'] == 'OK':
        distance = result['rows'][0]['elements'][0]['distance']['value'] / 1000.0  # Convert to kilometers
        travelling_time = result['rows'][0]['elements'][0]['duration']['text'] 
        return distance, travelling_time
    else:
        return None