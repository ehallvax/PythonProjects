"""
Find the coordinates of all places called "Brussels".
Complete the code below.

- Create a class that corresponds to a Location object.
  The field names are:
           location_id, country, region, city,
           postal_code, lat, lon, metro_code, area_code

- Create one generator that opens the file and yields
  locations one at a time.
  Use CSV.reader()
  https://docs.python.org/3.6/library/csv.html#csv.reader

- Create a second function that consumes the previous
  generator (or any generator of locations), filters
  on location names and yields the matching locations.
  (This should take a city name as input.)

- Create a third function that consumes the second one,
  and prints the coordinates for the matching locations.

Also see the following article about generators:
https://cisco.jiveon.com/blogs/jonathan/2016/09/12/too-much-memory-usage-what-to-do-now
"""
import csv

class Location(object):
    def __init__(self, location_id, country, region, city,
                 postal_code, lat, lon, metro_code, area_code):
        self.location_id = location_id
        self.country = country
        self.region = region
        self.city = city
        self.postal_code = postal_code
        self.lat = lat
        self.lon = lon
        self.metro_code = metro_code
        self.area_code = area_code

    def __repr__(self):
        return ('Location(location_id={!r}, region={!r}, city={!r}, '
                'postal_code={!r}, lat={!r}, lon={!r})'.format(
            self.location_id, self.region, self.city,
            self.postal_code, self.lat, self.lon))

def get_locations_from_file(file):
    with open(file,'r') as f:
        for row in csv.reader(f):
             yield Location(*row)

def filter_locations(locations, city_name: str):
    for location in locations:
        if location.city == city_name:
            yield location

def print_locations(locations):
    for location in locations:
        print(location.city, location.lat,location.lon)









def main():
    locations = get_locations_from_file('/Users/ehallvax/Desktop/locations.csv')
    filtered_locations = filter_locations(locations, 'Brussels')
    print_locations(filtered_locations)


if __name__ == '__main__':
    main()