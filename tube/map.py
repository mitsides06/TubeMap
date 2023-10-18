import json
from tube.components import Station, Line, Connection

class TubeMap:
    """
    Task 1: Complete the definition of the TubeMap class by:
    - completing the "import_from_json()" method

    Don't hesitate to divide your code into several sub-methods, if needed.

    As a minimum, the TubeMap class must contain these three member attributes:
    - stations: a dictionary that indexes Station instances by their id 
      (key=id (str), value=Station)
    - lines: a dictionary that indexes Line instances by their id 
      (key=id, value=Line)
    - connections: a list of Connection instances for the TubeMap 
      (list of Connections)
    """

    def __init__(self):
        self.stations = {}  # key: id (str), value: Station instance
        self.lines = {}  # key: id (str), value: Line instance
        self.connections = []  # list of Connection instances

    def import_from_json(self, filepath):
        """ Import tube map information from a JSON file.
        
        During the import process, the `stations`, `lines` and `connections` 
        attributes should be updated.

        You can use the `json` python package to easily load the JSON file at 
        `filepath`

        Note: when the indicated zone is not an integer (for instance: "2.5"), 
            it means that the station belongs to two zones. 
            For example, if the zone of a station is "2.5", 
            it means that the station is in both zones 2 and 3.

        Args:
            filepath (str) : relative or absolute path to the JSON file 
                containing all the information about the tube map graph to 
                import. If filepath is invalid, no attribute should be updated, 
                and no error should be raised.

        Returns:
            None
        """
        # TODO: Complete this method

        # Load and read json file.
        try:
            with open(filepath, "r") as jsonfile:
                data = json.load(jsonfile)
        except Exception:
            return None
        else:
            # Update "stations" attribute
            for station in data["stations"]:
                zone_num = float(station["zone"])    # convert string to float
                if int(zone_num) != zone_num:  # check if zone_num is float
                    zone_list = [int(zone_num), int(zone_num)+1]
                    zone_set = set(zone_list)
                    self.stations[station["id"]] = Station(station["id"], station["name"], zone_set)
                else:
                    zone_list = [int(zone_num)]
                    zone_set = set(zone_list)
                    self.stations[station["id"]] = Station(station["id"], station["name"], zone_set)
            
            # Update "lines" attribute
            for line in data["lines"]:
                self.lines[line["line"]] = Line(line["line"], line["name"])
            
            # Update "connections" attribute
            for connection in data["connections"]:
                station_list = [self.stations[connection["station1"]], self.stations[connection["station2"]]]
                station_set = set(station_list)
                self.connections.append(Connection(station_set, self.lines[connection["line"]], connection["time"]))

        
        return
#temporarily for checking purposes   
#a = TubeMap()
#print(a.import_from_json(5))


def test_import():
    tubemap = TubeMap()
    tubemap.import_from_json("data/london.json")
    
    # view one example Station
    print(tubemap.stations[list(tubemap.stations)[0]])
    
    # view one example Line
    print(tubemap.lines[list(tubemap.lines)[0]])
    
    # view the first Connection
    print(tubemap.connections[0])
    
    # view stations for the first Connection
    print([station for station in tubemap.connections[0].stations])


if __name__ == "__main__":
    test_import()
