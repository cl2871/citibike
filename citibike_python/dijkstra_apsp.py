import pandas as pd
from pandas.io import gbq
import os
from time import time
import heapq
import itertools


class PopFromEmptyQueueError(KeyError):
    pass


class PriorityQueue:

    """Implementation of a priority queue using heapq. Acts like a min-heap.

    Most code borrowed from below:
    https://docs.python.org/3/library/heapq.html#module-heapq

    entry:    [priority, count, element]

    """

    def __init__(self):
        self.queue = []
        heapq.heapify(self.queue)               # make into a heap
        self.entry_finder = {}                  # dict for finding an element's entry in priority queue
        self.counter = itertools.count()        # counter for priority tie-breaking
        self.REMOVED = "removed"                # for marking an element as removed

    def add_element(self, element, priority):

        """Add a new element or update the priority of an existing element"""

        # remove element if needed
        if element in self.entry_finder:
            try:
                self.remove_element(element)
            except KeyError:
                pass

        # map new entry and add element to queue
        count = next(self.counter)
        entry = [priority, count, element]
        self.entry_finder[element] = entry
        heapq.heappush(self.queue, entry)

    def remove_element(self, element):

        """Mark an existing element as REMOVED. Raises a KeyError if not found."""

        # remove the entry from entry_finder and set the element to REMOVED (since entry still in queue)
        entry = self.entry_finder.pop(element)
        entry[-1] = self.REMOVED

    def pop_element(self):

        """Remove and return the element with lowest priority value. Raise a KeyError if empty."""

        while self.queue:

            # return a valid min element from the queue
            priority, count, element = heapq.heappop(self.queue)
            if element is not self.REMOVED:
                del self.entry_finder[element]
                return element

        raise PopFromEmptyQueueError('pop from an empty priority queue')

    def length(self):
        return len(self.queue)


def dijkstra_min(vertices, source_distances, edges, prev, source):

    # Initialization
    source_distances[source] = 0
    queue = PriorityQueue()

    for vertex in vertices:
        if vertex != source:
            source_distances[vertex] = float("inf")                 # Initialize distance as infinity
            prev[vertex] = None                                     # Next node from vertex to source

        queue.add_element(vertex, source_distances[vertex])

    # run dijkstra until there are no more elements in queue.
    while queue.length() > 0:

        try:
            # pop vertex with lowest distance from source
            min_vertex = queue.pop_element()

            # min_vertex acts as an intermediary vertex between source and min_vertex's neighbors
            # update distances dict if needed
            if min_vertex in edges:
                for neighbor, edge in edges[min_vertex].items():

                    # update step: update source_distances and prev dicts, update priority of the neighbor in queue
                    alt = source_distances[min_vertex] + edge
                    if alt < source_distances[neighbor]:
                        source_distances[neighbor] = alt
                        prev[neighbor] = min_vertex
                        queue.add_element(neighbor, alt)

        except PopFromEmptyQueueError as e:
            # queue is empty, exit while loop
            break

        except KeyError as e:
            raise


def get_shortest_paths():

    """Generates a csv file containing the shortest paths between Citibike stations.

    Runs dijkstra on all Citibike stations. Dijkstra is better than Floyd-Warshall since the graph is sparse.
    The edges (average time between stations) are guaranteed to be positive (Citibike trip data only contains trips with
        at minimum 60 seconds of travel time).

    Notes:
    to run parallel code properly in Jupyter notebook, put functions in their own python file and import those functions
    https://stackoverflow.com/questions/47313732/jupyter-notebook-never-finishes-processing-using-multiprocessing
        -python-3/47374811#47374811
    """

    # aggregate data for trips in 2017 with durations <= hour and group by route (start station - end station)
    routes_query = """
    SELECT 
      start_station_name, start_station_id, start_station_latitude, start_station_longitude,
      end_station_name, end_station_id, end_station_latitude, end_station_longitude,
      COUNT(tripduration) AS num_trip, AVG(tripduration) AS avg_trip
    FROM 
      [bigquery-public-data:new_york.citibike_trips],
      [citibike_tripdata.tripdata_2016_10_to_2017_12], 
      [citibike_tripdata.tripdata_jc_2015_09_to_2017_12]
    WHERE YEAR(starttime) = 2017 AND tripduration <= 3600
    GROUP BY start_station_name, start_station_id, start_station_latitude, start_station_longitude,
      end_station_name, end_station_id, end_station_latitude, end_station_longitude 
    ORDER BY num_trip DESC
    """

    # execute query on Google BigQuery and store in routes DataFrame
    project_id = os.environ['project_id']
    routes = gbq.read_gbq(query=routes_query, dialect ='legacy', project_id=project_id)

    # include routes that have significant # of trips and avg trip times <= 30 mins
    usable_routes = routes.loc[(routes['num_trip'] > 5) & (routes['avg_trip'] <= 1800)]

    # exclude routes from and to unusual/test stations
    usable_routes = usable_routes.loc[(usable_routes['start_station_latitude'] != 0.0)
                                      & (usable_routes['end_station_latitude'] != 0.0)
                                      & (usable_routes['start_station_longitude'] != 0.0)
                                      & (usable_routes['end_station_longitude'] != 0.0)
                                      & (usable_routes["start_station_name"].str[:2] != "8D")
                                      & (usable_routes["end_station_name"].str[:2] != "8D")]

    print('Usable Routes Shape', usable_routes.shape)
    stations = set().union(usable_routes['start_station_id'], usable_routes['end_station_id'])
    print('Stations:', len(stations))

    """
    edges will be a dict of dict for avg travel times from usable_routes
        e.g.    edges[72][83] will give distance from station 72 to 83
    distances will be a dict of dict for best avg travel times
        e.g.    distances[72][83] will give distance from station 72 to station 82
    prev_station will be a dict of dict
        e.g.    prev_station[72][83] will give the next station from 83 to 72 
        
    each iteration of dijkstra will update distances and prev_station by adding new dicts for each source vertex
        distances[source] = source_distances
        prev_station[source] = prev
    """

    distances = {}
    prev_station = {}

    # put usable_routes avg trip durations into edges
    edges = {}
    for index, row in usable_routes.iterrows():

        start_station_id = row['start_station_id']
        end_station_id = row['end_station_id']

        # make an inner dict if needed
        if start_station_id not in edges:
            edges[start_station_id] = {}

        edges[start_station_id][end_station_id] = row['avg_trip']

    print("---- Starting Dijkstra APSP ----")

    start_time = time()
    for station in stations:
        station_distances = {}
        prev = {}
        dijkstra_min(stations, station_distances, edges, prev, station)
        distances[station] = station_distances
        prev_station[station] = prev
        #print("Station", station, "done")
    print("Algorithm Time: ", time() - start_time)

    print('Stations:', len(distances), 'Routes:', len(distances) ** 2)

    shortest_paths_list = []

    for start_station_id, end_stations in distances.items():
        for end_station_id, shortest_path in end_stations.items():
            shortest_paths_list.append([start_station_id, end_station_id, shortest_path])

    shortest_paths = pd.DataFrame(shortest_paths_list,
                                  columns=['start_station_id', 'end_station_id', 'shortest_path'])

    print('Generating Output File')

    shortest_paths.to_csv('../data/workspace/citibike_2017_shortest_paths_dijkstra.csv')


if __name__ == "__main__":
    get_shortest_paths()
