from network.graph import NeighbourGraphBuilder
from tube.map import TubeMap

class PathFinder:
    """
    Task 3: Complete the definition of the PathFinder class by:
    - completing the definition of the __init__() method (if needed)
    - completing the "get_shortest_path()" method (don't hesitate to divide 
      your code into several sub-methods)
    """
    def __init__(self, tubemap):
        """
        Args:
            tubemap (TubeMap) : The TubeMap to use.
        """
        self.tubemap = tubemap

        graph_builder = NeighbourGraphBuilder()
        self.graph = graph_builder.build(self.tubemap)

        # These are helper data structures for the Djikstra algorithm.
        self.dist = {}
        self.prev = {}
        self.unvisited_stations = []
    
    def convert_station_name_to_instance(self, station_name):
        """ Convert station name to station instance.

        Args:
            station_name (str): name of station

        Returns:
            Station : Station instance corresponing to the station name
        """
        for station in self.tubemap.stations.values():
            if station.name == station_name:
                return station
        
    def convert_station_id_to_instance(self, station_id):
        """ Convert station id to station instance.

        Args:
            station_id (str): station id

        Returns:
            Station : Station instance corresponing to the station id
        """
        for station in self.tubemap.stations.values():
            if station.id == station_id:
                return station
        
    def get_shortest_path(self, start_station_name, end_station_name):
        """ Find ONE shortest path from start_station_name to end_station_name.
        
        The shortest path is the path that takes the least amount of time.

        For instance, get_shortest_path('Stockwell', 'South Kensington') 
        should return the list:
        [Station(245, Stockwell, {2}), 
         Station(272, Vauxhall, {1, 2}), 
         Station(198, Pimlico, {1}), 
         Station(273, Victoria, {1}), 
         Station(229, Sloane Square, {1}), 
         Station(236, South Kensington, {1})
        ]

        If start_station_name or end_station_name does not exist, return None.
        
        You can use the Dijkstra algorithm to find the shortest path from
        start_station_name to end_station_name.

        Find a tutorial on YouTube to understand how the algorithm works, 
        e.g. https://www.youtube.com/watch?v=GazC3A4OQTE
        
        Alternatively, find the pseudocode on Wikipedia: https://en.wikipedia.org/wiki/Dijkstra's_algorithm#Pseudocode

        Args:
            start_station_name (str): name of the starting station
            end_station_name (str): name of the ending station

        Returns:
            list[Station] : list of Station objects corresponding to ONE 
                shortest path from start_station_name to end_station_name.
                Returns None if start_station_name or end_station_name does not 
                exist.
                Returns a list with one Station object (the station itself) if 
                start_station_name and end_station_name are the same.
        """
        start_station_instance = self.convert_station_name_to_instance(start_station_name)
        end_station_instance = self.convert_station_name_to_instance(end_station_name)
        station_instances_list = list(self.tubemap.stations.values())

        # Check if either of the provided station names does not exist.
        if start_station_instance not in station_instances_list or \
            end_station_instance not in station_instances_list:
            return 

        # Check if the start and end stations are the same, 
        # return a list with an instance of this station itself.
        if start_station_name == end_station_name:
            return [start_station_instance]
        
        # Run the Dijkstra algorithm and return result.
        return self.dijkstra_algo(start_station_instance, end_station_instance)
    
    def algo_preparation(self, start):
        """ Prepares the tools needed to run the Dijkstra algorithm.
            It updates the dist, prev, and unvisited_stations attributes.

        Args:
            start (Station) : Initial station instance
        
        Returns:
            None
        """
        # Fill in the data structures.
        for station_id in self.graph:
            station = self.convert_station_id_to_instance(station_id)
            self.dist[station] = float("inf")
            self.prev[station] = None
            self.unvisited_stations.append(station)
        
        self.dist[start] = 0

    def main_algo(self, curr_station):
        """ Main part of Dijkstra algorithm.
            
            It investigates the connected stations of the currenct station, 
            updating the dis, prev, and univisted_stations attributes.

            Args:
                curr_station (Station) : The station instance of the current station
                end (Station) : The station instance of the final station
            
            Returns:
                None
        """
        for next_station_id in self.graph[curr_station.id]:
            next_station = self.convert_station_id_to_instance(next_station_id)
            curr_to_next_dist = min([station.time for station in 
                                     self.graph[curr_station.id][next_station.id]])
            start_to_next_dist = self.dist[curr_station] + curr_to_next_dist

            if start_to_next_dist < self.dist[next_station]:
                self.dist[next_station] = start_to_next_dist
                self.prev[next_station] = curr_station

    def dijkstra_algo(self, start, end):
        """ This is the Dijkstra algorithm used to find the shortest path.

            Args:
                start (Station) : Initial station instance
                end (Station) : Final station instance
            
            Returns:
            list[Station] : list of Station objects corresponding to ONE 
                shortest path from start_station_name to end_station_name.
        """
        self.algo_preparation(start)
        while len(self.unvisited_stations) > 0:
            min_dist = min([self.dist[station] for station in self.unvisited_stations])

            # Set the station in the unvisited_list with the minimum distance as the current one,
            # and remove it from unvisited_stations list.
            curr_station = [station for station, dist in self.dist.items() if dist == 
                            min_dist and station in self.unvisited_stations][0]
            self.unvisited_stations.remove(curr_station) 
            self.main_algo(curr_station)

        result = []
        curr_station = end
        while len(result) == 0 or result[-1] != start:
            result.append(curr_station)
            curr_station = self.prev[curr_station]

        # Result is the  shortest path from the final station to the initial station, so we need to reverse it.
        result.reverse()
        return result
    
def test_shortest_path():
    from tube.map import TubeMap
    tubemap = TubeMap()
    tubemap.import_from_json("data/london.json")
    
    path_finder = PathFinder(tubemap)
    stations = path_finder.get_shortest_path('High Barnet', 'Upminster')
    print(stations)
    
    station_names = [station.name for station in stations]
    print(station_names)
    #expected = ["Covent Garden", "Leicester Square", "Piccadilly Circus", 
    #            "Green Park"]
    #assert station_names == expected

if __name__ == "__main__":
    test_shortest_path()
