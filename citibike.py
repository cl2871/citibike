import time
import sqlite3


class Station:
    def __init__(self, station_id, name, latitude, longitude):
        self.station_id = station_id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.neighbors = []

    # --- getters ---

    def get_id(self):
        return self.station_id

    def get_neighbors(self):
        return self.neighbors


class Trip:
    def __init__(self, duration, start_time, end_time, start_station_id, end_station_id):
        self.duration = duration
        self.start_time = start_time
        self.end_time = end_time
        self.start_station_id = start_station_id
        self.end_station_id = end_station_id


def read_trips_csv(c):

    file_name = 'JC-201709-citibike-tripdata.csv'
    stations = {}
    trips = []
    edges = {}
    with open(file_name) as f:
        for n, line in enumerate(f):
            if n == 0:
                continue
            line_items = line.split(',')

            duration = int(line_items[0])
            start_time = line_items[1]
            end_time = line_items[2]
            start_station_id = int(line_items[3])
            end_station_id = int(line_items[7])

            new_trip = Trip(duration, start_time, end_time, start_station_id, end_station_id)
            trips.append(new_trip)

            if start_station_id not in stations:
                start_station_name = line_items[4]
                start_station_latitude = float(line_items[5])
                start_station_longitude = float(line_items[6])
                new_station = Station(start_station_id, start_station_name, start_station_latitude,
                                      start_station_longitude)
                stations[start_station_id] = new_station

            if end_station_id not in stations:
                end_station_name = line_items[8]
                end_station_latitude = float(line_items[9])
                end_station_longitude = float(line_items[10])
                new_station = Station(end_station_id, end_station_name, end_station_latitude,
                                      end_station_longitude)
                stations[end_station_id] = new_station

        for station_id, station in stations.items():

            t = (station_id, station.name, station.latitude, station.longitude,)
            c.execute('INSERT INTO stations VALUES (?,?,?,?)', t)

        for trip in trips:

            t = (trip.duration, trip.start_time, trip.end_time, trip.start_station_id, trip.end_station_id)
            c.execute('INSERT INTO trips VALUES (?,?,?,?,?)', t)

        with open('JC_edges.csv', 'w') as edge_file:
            c.execute('SELECT start_station_id, end_station_id, COUNT(duration) as num_trips, AVG(duration) as trip_avg '
                      'FROM trips GROUP BY start_station_id, end_station_id')
            for row in c.fetchall():
                start_station_id = row[0]
                end_station_id = row[1]
                if start_station_id not in edges:
                    edges[start_station_id] = {}
                if start_station_id in edges:
                    edges[start_station_id][end_station_id] = row[3]
                    edge_file.write(str(start_station_id) + ',' + str(end_station_id) + ',' + str(row[3]) + '\n')

        distances = {}
        next_vertex = {}
        run_floyd_warshall_path_reconstruction(stations.keys(), distances, edges, next_vertex)

        """
        print(distances[3183][3201])
        path = build_shortest_path(3183, 3201, next_vertex)
        print(path)
        """

        for station in distances.keys():
            for neighbor in distances[station].keys():
                t = (station, neighbor, distances[station][neighbor])
                c.execute('INSERT INTO distances VALUES (?,?,?)', t)

        """
        c.execute(
            'SELECT start_station_id, end_station_id, distance '
            'FROM distances WHERE start_station_id = 3183 AND end_station_id = 3201')
        print(c.fetchone())
        """

    with open('JC_distances.csv', 'w') as w:
        c.execute(
            'SELECT * FROM distances ')
        for item in c.fetchall():
            w.write(str(item[0]) + ',' + str(item[1]) + ',' + str(item[2]) + '\n')

    #moo


def run_floyd_warshall_path_reconstruction(vertices, distances, edges, next_vertex):
    """ Stores the minimum average trip time between 2 vertices in the distances data structure and stores the next
    vertex in a path between 2 vertices in the next_vertex data structure for path recovery.

    :param vertices: set of all vertices in graph
    :param distances: dict->dict that stores the minimum average trip time between 2 vertices
    :param edges: dict->dict that stores the direct average trip time (edge) between 2 vertices
    :param next_vertex:
    :return:
    """

    """
    Notes:
    - no negative cycles, smallest trip time is 60s
    - theta(n^3) runtime
    """

    # initialize inner dictionaries for each vertex and handle self-loops
    for vertex in vertices:
        distances[vertex] = {}
        distances[vertex][vertex] = 0
        next_vertex[vertex] = {}
        next_vertex[vertex][vertex] = None

    # for each vertex-vertex pairing, initialize distances and next_vertex
    for vertex_1 in vertices:
        for vertex_2 in vertices:
            if vertex_1 == vertex_2:
                continue
            if vertex_1 in edges and vertex_2 in edges[vertex_1]:
                distances[vertex_1][vertex_2] = edges[vertex_1][vertex_2]
                next_vertex[vertex_1][vertex_2] = vertex_2
            else:
                distances[vertex_1][vertex_2] = float('inf')
                next_vertex[vertex_1][vertex_2] = None

    for k in sorted(vertices):
        for i in sorted(vertices):
            for j in sorted(vertices):
                if distances[i][j] > distances[i][k] + distances[k][j]:
                    distances[i][j] = distances[i][k] + distances[k][j]
                    next_vertex[i][j] = next_vertex[i][k]


def build_shortest_path(vertex_1, vertex_2, next_vertex):
    # returns a list of vertices as shortest path
    if next_vertex[vertex_1] is None or next_vertex[vertex_1][vertex_2] is None:
        # no possible path
        return []
    path = [vertex_1]
    current_vertex = vertex_1
    while current_vertex != vertex_2:
        current_vertex = next_vertex[current_vertex][vertex_2]
        path.append(current_vertex)
    return path


def initialize(c):
    c.execute('DROP TABLE IF EXISTS stations')
    c.execute('DROP TABLE IF EXISTS trips')
    c.execute('DROP TABLE IF EXISTS distances')
    c.execute('''CREATE TABLE IF NOT EXISTS stations
                    (id integer, name text, latitude real, longitude real)''')
    c.execute('''CREATE TABLE IF NOT EXISTS trips
                    (duration integer, start_time date, end_time date, start_station_id integer, 
                    end_station_id integer)''')
    c.execute('''CREATE TABLE IF NOT EXISTS distances
                    (start_station_id integer, end_station_id integer, distance real)''')

    read_trips_csv(c)


def main():
    # initialize connection
    conn = sqlite3.connect('JC_citibike.db')
    c = conn.cursor()

    initialize(c)

    # save and close connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    start_time = time.time()
    main()
    duration = time.time() - start_time
    print('---- %s seconds ----' % duration)
