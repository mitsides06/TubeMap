from tube.map import TubeMap

class NeighbourGraphBuilder:
    """
    Task 2: Complete the definition of the NeighbourGraphBuilder class by:
    - completing the "build" method below (don't hesitate to divide your code 
      into several sub-methods, if needed)
    """

    def __init__(self):
        pass

    def build(self, tubemap):
        """ Builds a graph encoding neighbouring connections between stations.

        ----------------------------------------------

        The returned graph should be a dictionary having the following form:
        {
            "station_A_id": {
                "neighbour_station_1_id": [
                                connection_1 (instance of Connection),
                                connection_2 (instance of Connection),
                                ...],

                "neighbour_station_2_id": [
                                connection_1 (instance of Connection),
                                connection_2 (instance of Connection),
                                ...],
                ...
            }

            "station_B_id": {
                ...
            }

            ...

        }

        ----------------------------------------------

        For instance, knowing that the id of "Hammersmith" station is "110",
        graph['110'] should be equal to:
        {
            '17': [
                Connection(Hammersmith<->Barons Court, District Line, 1),
                Connection(Hammersmith<->Barons Court, Piccadilly Line, 2)
                ],

            '209': [
                Connection(Hammersmith<->Ravenscourt Park, District Line, 2)
                ],

            '101': [
                Connection(Goldhawk Road<->Hammersmith, Hammersmith & City Line, 2)
                ],

            '265': [
                Connection(Hammersmith<->Turnham Green, Piccadilly Line, 2)
                ]
        }

        ----------------------------------------------

        Args:
            tubemap (TubeMap) : tube map serving as a reference for building 
                the graph.

        Returns:
            graph (dict) : as described above. 
                If the input data (tubemap) is invalid, 
                the method should return an empty dict.
        """
        # TODO: Complete this method

        result = {}
        try:
            # Set all the keys of the outer dictionary and set their values to be empty dictioaries
            for connection in tubemap.connections:
                stations = [station for station in connection.stations]
                result[stations[0].id] = {}
                result[stations[1].id] = {}
            # Set all the keys of each inner dictionary and set their values to be empty lists
            for connection in tubemap.connections:
                stations = [station for station in connection.stations]            
                result[stations[0].id].setdefault(stations[1].id, [])
                result[stations[1].id].setdefault(stations[0].id, [])
            # Fill in the dictionary as required.
            for connection in tubemap.connections:
                stations = [station for station in connection.stations]            
                result[stations[0].id][stations[1].id].append(connection)
                result[stations[1].id][stations[0].id].append(connection)

            return result
        
        except Exception:
            return dict()


def test_graph():
    from tube.map import TubeMap
    tubemap = TubeMap()
    tubemap.import_from_json("data/london.json")

    graph_builder = NeighbourGraphBuilder()
    graph = graph_builder.build(tubemap)

    print(graph)


if __name__ == "__main__":
    test_graph()
