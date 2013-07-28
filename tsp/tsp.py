"""Traveling Salesman solution with random start and greedy path selection
You can select how many iterations to run by doing the following:
python tsp.py 20 # run 20 times
"""

import sys
from random import choice
import numpy as np

# Data set: using stock tickers to represent cities
values = [
("AAPL", "CSCO", 14),
("AAPL", "CVX", 44),
("AAPL", "EBAY", 14),
("AAPL", "GOOG", 14),
("AAPL", "GPS", 59),
("AAPL", "HPQ", 14),
("AAPL", "INTC", 8),
("AAPL", "MCK", 60),
("AAPL", "ORCL", 26),
("AAPL", "PCG", 59),
("AAPL", "SFO", 46),
("AAPL", "SWY", 37),
("AAPL", "URS", 60),
("AAPL", "WFC", 60),

("CSCO","AAPL" ,14),
("CSCO", "CVX", 43),
("CSCO", "EBAY",0),
("CSCO", "GOOG",21),
("CSCO", "GPS",67),
("CSCO", "HPQ",26),
("CSCO", "INTC",6),
("CSCO", "MCK",68),
("CSCO", "ORCL",37),
("CSCO", "PCG",68),
("CSCO", "SFO",57),
("CSCO", "SWY",32),
("CSCO", "URS",68),
("CSCO", "WFC",68),

("CVX","AAPL" ,44),
("CVX", "CSCO",43),
("CVX", "EBAY",43),
("CVX", "GOOG",36),
("CVX", "GPS",43),
("CVX", "HPQ",40),
("CVX", "INTC",41),
("CVX", "MCK",46),
("CVX", "ORCL",39),
("CVX", "PCG",44),
("CVX", "SFO",45),
("CVX", "SWY",13),
("CVX", "URS",44),
("CVX", "WFC",44),

("EBAY","AAPL" ,14),
("EBAY", "CSCO",0),
("EBAY", "CVX",43),
("EBAY", "GOOG",21),
("EBAY", "GPS",67),
("EBAY", "HPQ",26),
("EBAY", "INTC",6),
("EBAY", "MCK",68),
("EBAY", "ORCL",37),
("EBAY", "PCG",68),
("EBAY", "SFO",57),
("EBAY", "SWY",32),
("EBAY", "URS",68),
("EBAY", "WFC",68),

("GOOG","AAPL",11),
("GOOG", "CSCO",21),
("GOOG", "CVX",36),
("GOOG", "EBAY",21),
("GOOG", "GPS",48),
("GOOG", "HPQ",6),
("GOOG", "INTC",15),
("GOOG", "MCK",49),
("GOOG", "ORCL",16),
("GOOG", "PCG",48),
("GOOG", "SFO",36),
("GOOG", "SWY",32),
("GOOG", "URS",49),
("GOOG", "WFC",49),

("GPS","AAPL" ,59),
("GPS", "CSCO",67),
("GPS", "CVX",43),
("GPS", "EBAY",67),
("GPS", "GOOG",48),
("GPS", "HPQ",45),
("GPS", "INTC",62),
("GPS", "MCK",03),
("GPS", "ORCL",34),
("GPS", "PCG",01),
("GPS", "SFO",18),
("GPS", "SWY",53),
("GPS", "URS",01),
("GPS", "WFC",01),

("HPQ","AAPL" ,14),
("HPQ", "CSCO",26),
("HPQ", "CVX",40),
("HPQ", "EBAY",26),
("HPQ", "GOOG",6),
("HPQ", "GPS",45),
("HPQ", "INTC",20),
("HPQ", "MCK",46),
("HPQ", "ORCL",12),
("HPQ", "PCG",46),
("HPQ", "SFO",32),
("HPQ", "SWY",37),
("HPQ", "URS",46),
("HPQ", "WFC",46),

("INTC","AAPL",8),
("INTC","CSCO",6),
("INTC", "CVX",41),
("INTC", "EBAY",6),
("INTC", "GOOG",15),
("INTC", "GPS",62),
("INTC", "HPQ",20),
("INTC", "MCK",63),
("INTC", "ORCL",31),
("INTC", "PCG",62),
("INTC", "SFO",51),
("INTC", "SWY",32),
("INTC", "URS",63),
("INTC", "WFC",63),

("MCK", "AAPL",60),
("MCK", "CSCO",68),
("MCK", "CVX",46),
("MCK", "EBAY",68),
("MCK", "GOOG",49),
("MCK", "GPS",03),
("MCK", "HPQ",46),
("MCK", "INTC",63),
("MCK", "ORCL",34),
("MCK", "PCG",3),
("MCK", "SFO",16),
("MCK", "SWY",56),
("MCK", "URS",3),
("MCK", "WFC",2),

("ORCL", "AAPL",22),
("ORCL", "CSCO",37),
("ORCL", "CVX",39),
("ORCL", "EBAY",37),
("ORCL", "GOOG",16),
("ORCL", "GPS",34),
("ORCL", "HPQ",12),
("ORCL", "INTC",31),
("ORCL", "MCK",34),
("ORCL", "PCG",35),
("ORCL", "SFO",20),
("ORCL", "SWY",40),
("ORCL", "URS",35),
("ORCL", "WFC",35),

("PCG", "AAPL",59),
("PCG", "CSCO",68),
("PCG", "CVX",44),
("PCG", "EBAY",68),
("PCG", "GOOG",48),
("PCG", "GPS",01),
("PCG", "HPQ",46),
("PCG", "INTC",62),
("PCG", "MCK",03),
("PCG", "ORCL",35),
("PCG", "SFO",18),
("PCG", "SWY",54),
("PCG", "URS",01),
("PCG", "WFC",01),

("SFO", "AAPL",46),
("SFO", "CSCO",57),
("SFO", "CVX",45),
("SFO", "EBAY",57),
("SFO", "GOOG",36),
("SFO", "GPS",18),
("SFO", "HPQ",32),
("SFO", "INTC",51),
("SFO", "MCK",16),
("SFO", "ORCL",20),
("SFO", "PCG",18),
("SFO", "SWY",52),
("SFO", "URS",18),
("SFO", "WFC",18),

("SWY", "AAPL",37),
("SWY", "CSCO",32),
("SWY", "CVX",13),
("SWY", "EBAY",32),
("SWY", "GOOG",32),
("SWY", "GPS",53),
("SWY", "HPQ",37),
("SWY", "INTC",32),
("SWY", "MCK",56),
("SWY", "ORCL",40),
("SWY", "PCG",54),
("SWY", "SFO",52),
("SWY", "URS",54),
("SWY", "WFC",54),

("URS", "AAPL",60),
("URS", "CSCO",68),
("URS", "CVX",44),
("URS", "EBAY",68),
("URS", "GOOG",49),
("URS", "GPS",01),
("URS", "HPQ",46),
("URS", "INTC",63),
("URS", "MCK",03),
("URS", "ORCL",35),
("URS", "PCG",01),
("URS", "SFO",18),
("URS", "SWY",54),
("URS", "WFC",0),

("WFC", "AAPL",60),
("WFC", "CSCO",68),
("WFC", "CVX",44),
("WFC", "EBAY",68),
("WFC", "GOOG",49),
("WFC", "GPS",01),
("WFC", "HPQ",46),
("WFC", "INTC",63),
("WFC", "MCK",02),
("WFC", "ORCL",35),
("WFC", "PCG",01),
("WFC", "SFO",18),
("WFC", "SWY",54),
("WFC", "URS",0),
]


# Create a data type object 
dt = np.dtype([('city_start', 'S10'), ('city_end', 'S10'), ('distance', int)])

# Values from routes are assigned as an array according to type dt
data_set = np.array(values, dtype=dt)

def all_cities(mdarray):
    """Take a multidimensional array in this format and finds unique cities
    
    array([["A", "A"],
           ["A", "B"]])
           """
    cities = {}
    city_set = set(data_set['city_end'])
    for city in city_set:
        cities[city] = ""   # Basically updating the cities list every time when city is added
    return cities

def randomize_city_start(all_cities):
    """Return a randomized city to start trip"""
    return choice(all_cities)
    
def get_shortest_route(routes):
    """Sort the list by distance and return shortest distance route"""
    route = sorted(routes, key=lambda dist: dist[2]).pop(0)
    return route
    
def greedy_path():
    """Select the next path to travel based on the shortest, nearest path"""
    itinerary = []
    cities = all_cities(data_set)
    starting_city = randomize_city_start(cities.keys()) # start from a random city
    # print "starting_city: %s" % starting_city
    cities_visited = {}
    
    # iterate through all cities
    count = 1
    while True:
        possible_routes = []
        #distance = []
        # print "starting_city: %s" % starting_city
        for path in data_set:
            # we only start with city that we have assigned in starting_city
            if starting_city in path['city_start']:
                # we don't go to cities we have visited
                if path['city_end'] in cities_visited:
                    continue
                else:
                    # print "path: ", path
                    possible_routes.append(path)    # add the city if not in the list
                    
        if not possible_routes:
            break
        # append this to itinerary
        route = get_shortest_route(possible_routes)
        count += 1
        itinerary.append(route)
        # add this city to visited_cities list
        cities_visited[route[0]] = count
        starting_city = route[1]
        
    return itinerary
    
def get_total_distance(complete_itinerary):
    distance = sum(z for x,y,z in complete_itinerary)
    return distance
    
def lowest_simulation(num):
    """Call greedy algorithm and generate route with shortest distance for num times"""
    routes = {}
    for i in range(num):
        itinerary = greedy_path()
        distance = get_total_distance(itinerary)
        routes[distance] = itinerary
    shortest_distance = min(routes.key())
    route = routes[shortest_distance]
    return shortest_distance, route
    
def main():
    """runs everything"""
    # If number of times is provided
    if len(sys.argv) == 2:
        iterations = int(sys.argv[1])
        print "Running simulation %s times" % iterations
        distance, route = lowest_simulation(iterations)
        print "Shortest distance: %s" % distance
        print "Optimal route: %s" % route
    else:
        itinerary = greedy_path()   # only run once because number of times is not specified
        print "itinerary: %s" % itinerary
        print "distance: %s" % get_total_distance(itinerary)

if __name__ == '__main__':
    main()

        