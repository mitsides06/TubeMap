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
        
        # Feel free to add anything else needed here.
    
    def convert_station_name_to_instance(self, station_name):
        for station in self.tubemap.stations.values():
            if station.name == station_name:
                return station
            
    def convert_station_id_to_instance(self, station_id):
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
        # TODO: Complete this method
        start_station_instance = self.convert_station_name_to_instance(start_station_name)
        end_station_instance = self.convert_station_name_to_instance(end_station_name)
        station_instances_list = list(self.tubemap.stations.values())

        # Check if either of the provided station names does not exist.
        if start_station_instance not in station_instances_list or end_station_instance not in station_instances_list:
            return 

        # Check if the start and end stations are the same, return a list with an instance of this station itself.
        if start_station_name == end_station_name:
            return [start_station_instance]
        
        return self.dijkstra_algo(start_station_instance, end_station_instance)
        

        



    def dijkstra_algo(self, start, end):
        graph = self.graph
        dist = {}
        prev = {}
        unvisited_stations = []
        for station_id in graph:
            station = self.convert_station_id_to_instance(station_id)
            dist[station] = float("inf")
            prev[station] = None
            unvisited_stations.append(station)
        
        dist[start] = 0

        stop = False
        while not stop:
            min_dist = min([dist[station] for station in unvisited_stations])

            # Set the station with the minimum distance as the current on and remove it from unvisited_stations list.
            curr_station = [station for station, dist in dist.items() if dist == min_dist and station in unvisited_stations][0]
            unvisited_stations.remove(curr_station) 
            
            # Investigate the connected stations of the current station (part of Dijkstra algorithm).
            for next_station_id in graph[curr_station.id]:
                next_station = self.convert_station_id_to_instance(next_station_id)
                curr_to_next_dist = min([station.time for station in graph[curr_station.id][next_station.id]])
                start_to_next_dist = dist[curr_station] + curr_to_next_dist
                if start_to_next_dist < dist[next_station]:
                    dist[next_station] = start_to_next_dist
                    prev[next_station] = curr_station

                    if next_station == end:
                        stop = True
                        break
        

        result = []
        curr_station = end
        while len(result) == 0 or result[-1] != start:
            result.append(curr_station)
            curr_station = prev[curr_station]

        # Result is the  shortest path from the final station to the initial station, so we need to reverse it.
        result.reverse()

        return result




        


        
    
tubemap = TubeMap()
tubemap.import_from_json("data/london.json")
a = PathFinder(tubemap)
print(a.get_shortest_path('Stockwell', 'South Kensington'))


#def test_shortest_path():
#    from tube.map import TubeMap
#    tubemap = TubeMap()
#    tubemap.import_from_json("data/london.json")
    
#    path_finder = PathFinder(tubemap)
#    stations = path_finder.get_shortest_path("Covent Garden", "Green Park")
#    print(stations)
    
#    station_names = [station.name for station in stations]
#    expected = ["Covent Garden", "Leicester Square", "Piccadilly Circus", 
#                "Green Park"]
#    assert station_names == expected


#if __name__ == "__main__":
#    test_shortest_path()
