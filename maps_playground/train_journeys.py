import googlemaps
import polyline
import simplekml
import re
from geographiclib.geodesic import Geodesic

# Function to fetch route from Google Directions API
def fetch_route(api_key, origin, destination, mode):
    gmaps = googlemaps.Client(key=api_key)

    # Request driving or transit directions
    directions_result = gmaps.directions(
        origin,
        destination,
        mode=mode,
        alternatives=False
    )

    # Extract polyline from the first route
    if directions_result:
        steps = directions_result[0]['legs'][0]['steps']
        all_coords = []

        for step in steps:
            if 'polyline' in step and step['travel_mode'] != 'WALKING':
                decoded_coords = polyline.decode(step['polyline']['points'])  # Decode polyline
                all_coords.extend(decoded_coords)  # Append decoded coordinates to list

        # Re-encode combined coordinates into a single polyline
        combined_polyline = polyline.encode(all_coords)
        return combined_polyline
    else:
        print(f"No {mode} route found for {origin} to {destination}.")
        return None


# Function to geocode locations and get coordinates
def geocode_location(api_key, location):
    gmaps = googlemaps.Client(key=api_key)

    # Use the Geocoding API to fetch location coordinates
    geocode_result = gmaps.geocode(location)

    if geocode_result:
        lat = geocode_result[0]['geometry']['location']['lat']
        lng = geocode_result[0]['geometry']['location']['lng']
        print(f"Coordinates for {location}: ({lat}, {lng})")
        return (lat, lng)
    else:
        print(f"Failed to geocode location: {location}")
        return None


def generate_great_circle_points(origin_coords, destination_coords, num_points=100):
    geod = Geodesic.WGS84
    line = geod.InverseLine(origin_coords[0], origin_coords[1], destination_coords[0], destination_coords[1])

    waypoints = []
    for i in range(num_points + 1):
        point = line.Position(i * line.s13 / num_points)
        waypoints.append((point['lat2'], point['lon2']))

    return waypoints


# Function to create a curved KML flight path
def create_curved_flight_kml(origin_coords, destination_coords, output_file, route_name, line_color):
    kml = simplekml.Kml()

    # Generate great-circle waypoints
    waypoints = generate_great_circle_points(origin_coords, destination_coords)

    # Create line string with waypoints
    linestring = kml.newlinestring(name=route_name)
    linestring.coords = [(lon, lat) for lat, lon in waypoints]
    linestring.style.linestyle.color = line_color
    linestring.style.linestyle.width = 3

    # Save KML file
    kml.save(output_file)
    print(f"Curved flight KML saved: {output_file}")


# Function to create a KML file from a polyline
def create_kml_from_polyline(polyline_str, output_file, route_name, line_color):
    coordinates = polyline.decode(polyline_str)

    kml = simplekml.Kml()
    linestring = kml.newlinestring(name=route_name)
    linestring.coords = [(lng, lat) for lat, lng in coordinates]
    linestring.style.linestyle.color = line_color
    linestring.style.linestyle.width = 3

    kml.save(output_file)
    print(f"Route KML saved: {output_file}")


# Function to sanitize file names
def sanitize_filename(name):
    return re.sub(r'[^a-zA-Z0-9_]+', '_', name.lower())


# Main Function
def main():
    # Google API Key
    API_KEY = "INSERT_API_KEY"

    # Options for different journey types
    journeys = [
        {
            "type": "train",
            "destination": "Stratford International, Queen Elizabeth Olympic Park, International Wy, London E20 1YY",
            "origin": "Star Lane Station, London"
        },
        # {
        #     "type": "flight",
        #     "origin": "Dublin Airport",
        #     "destination": "London Stanstead International Airport",
        #     "name": "STD to DUB"
        # },

        # {
        #     "type": "drive",
        #     "origin": "Great Portland Street",
        #     "destination": "Heathrow Airport"
        # },
        # {
        #     "type": "drive",
        #     "origin": "E14 OXE London",
        #     "destination": "The Savoy"
        # },

    ]

    # Process each journey
    for journey in journeys:
        if journey["type"] == "train":
            print(f"Processing train route: {journey['origin']} to {journey['destination']}")
            polyline_str = fetch_route(API_KEY, journey["origin"], journey["destination"], "transit")

            if polyline_str:
                file_name = f"{sanitize_filename(journey['origin'])}_to_{sanitize_filename(journey['destination'])}.kml"
                create_kml_from_polyline(polyline_str, file_name, f"{journey['origin']} to {journey['destination']}", simplekml.Color.blue)

        elif journey["type"] == "flight":
            print(f"Processing flight route: {journey['origin']} to {journey['destination']}")
            origin_coords = geocode_location(API_KEY, journey["origin"])
            destination_coords = geocode_location(API_KEY, journey["destination"])

            if origin_coords and destination_coords:
                file_name = f"{sanitize_filename(journey['name'])}_flight.kml"
                create_curved_flight_kml(
                    origin_coords,
                    destination_coords,
                    file_name,
                    journey["name"],
                    simplekml.Color.green
                )

        elif journey["type"] == "drive":
            print(f"Processing driving route: {journey['origin']} to {journey['destination']}")
            polyline_str = fetch_route(API_KEY, journey["origin"], journey["destination"], "driving")

            if polyline_str:
                file_name = f"{sanitize_filename(journey['origin'])}_to_{sanitize_filename(journey['destination'])}_drive.kml"
                create_kml_from_polyline(polyline_str, file_name, f"{journey['origin']} to {journey['destination']}", simplekml.Color.red)


if __name__ == "__main__":
    main()