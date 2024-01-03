'''
    0. receive the data:
    1. make a 1 d array from the 2 d array
    2. make a 2 d index array from the 2 d array
    3. make a distance matrix
    4. compute the shoetest distance between every adjacent hierarchy
    5. send these as start ends to the algorithm class to calculate the path in every hierarchy (send over as addresses)
    6. recieve these (as addresses) and compile into one path
    7. respond back to the api call
'''
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import sys
import json
import urllib.request

def get_data():
    """Creates the data."""
    data = {}
    data['API_key'] = 'AIzaSyCPsqAOFiYHgfX0mKLHeOChxQkGY-03JWc'
    data['addresses'] = [['3610+Hacks+Cross+Rd+Memphis+TN'],
                        ['706+Union+Ave+Memphis+TN'],
                        ['814+Scott+St+Memphis+TN',
                        '926+E+McLemore+Ave+Memphis+TN'],
                        ['1005+Tillman+St+Memphis+TN']
                        ]


    return data

def create_distance_matrix(data):
    addresses = data["addresses"]
    API_key = data["API_key"]
    # Distance Matrix API only accepts 100 elements per request, so get rows in multiple requests.
    max_elements = 100
    num_addresses = len(addresses) # 16 in this example.
    # Maximum number of rows that can be computed per request (6 in this example).
    max_rows = max_elements // num_addresses
    # num_addresses = q * max_rows + r (q = 2 and r = 4 in this example).
    q, r = divmod(num_addresses, max_rows)
    dest_addresses = addresses 
    distance_matrix = []
    # Send q requests, returning max_rows rows per request.
    for i in range(q):
        origin_addresses = addresses[i * max_rows: (i + 1) * max_rows]
        response = send_request(origin_addresses, dest_addresses, API_key)
        distance_matrix += build_distance_matrix(response)

    # Get the remaining remaining r rows, if necessary.
    if r > 0:
        origin_addresses = addresses[q * max_rows: q * max_rows + r]
        response = send_request(origin_addresses, dest_addresses, API_key)
        distance_matrix += build_distance_matrix(response)
    return distance_matrix

def send_request(origin_addresses, dest_addresses, API_key):
    """ Build and send request for the given origin and destination addresses."""
    def build_address_str(addresses):
        # Build a pipe-separated string of addresses
        address_str = ''
        for i in range(len(addresses)):
            address_str += addresses[i] + '|'
            #address_str += addresses[-1]
        return address_str

    request = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial'
    origin_address_str = build_address_str(origin_addresses)
    #print(origin_address_str)
    dest_address_str = build_address_str(dest_addresses)
    request = request + '&origins=' + origin_address_str + '&destinations=' + \
                        dest_address_str + '&key=' + API_key
    with urllib.request.urlopen(request) as response:
        jsonResult = response.read()
        responseData = json.loads(jsonResult.decode('utf-8'))
    return responseData

def build_distance_matrix(response):
    distance_matrix = []
    for row in response['rows']:
        row_list = [row['elements'][j]['distance']['value'] for j in range(len(row['elements']))]
        distance_matrix.append(row_list)
    return distance_matrix

def create_data_model1(addresses_hierarchy, API_key):
    data = {}
    data['addresses'] = addresses_assemble(addresses_hierarchy)
    data['API_key'] = API_key
    """Stores the data for the problem."""
    data_model = {}
    data_model["distance_matrix"] = create_distance_matrix(data)
    addresses_hierarchy_index = create_index(addresses_hierarchy)
    addresses_no_start_end = addresses_hierarchy_index[1:-1]
    data_model["start_end"] = []
    for i in range(len(addresses_no_start_end) - 1):
        start = addresses_no_start_end[i]
        end = addresses_no_start_end[i + 1]
        data_model["start_end"].append(get_start_end(start, end, data_model["distance_matrix"]))
    data_model["start_end_addresses"] = []
    for index_tuple in data_model["start_end"]:
        start, end = index_tuple
        data_model["start_end_addresses"].append((data['addresses'][start], data['addresses'][end]))
    addresses_hierarchy_index = create_index(addresses_hierarchy)

    return data_model

def get_start_end(start, end, distance_matrix):
    min_value = float('inf')
    min_position = (-1, -1)

    for row in start:
        for col in end:
            if distance_matrix[row][col] < min_value:
                min_value = distance_matrix[row][col]
                min_position = (row, col)

    return min_position

def addresses_assemble(two_d_array):
    return [element for row in two_d_array for element in row]

def create_index(matrix):
    flattened_index = 0
    result_matrix = []

    for row in matrix:
        result_row = []
        for _ in row:
            result_row.append(flattened_index)
            flattened_index += 1
        result_matrix.append(result_row)

    return result_matrix

def create_data_model(addresses, API_key):
    data = {}
    data['addresses'] = addresses
    data['API_key'] = API_key
    """Stores the data for the problem."""
    data_model = {}
    data_model["distance_matrix"] = create_distance_matrix(data)
    data_model["num_vehicles"] = 1
    data_model["starts"] = [0]
    data_model["ends"] = [len(data['addresses']) - 1]
    return data_model

def print_solution(data_model, manager, routing, solution):
    """Prints solution on console."""
    print(f"Objective: {solution.ObjectiveValue()}")
    total_distance = 0
    for vehicle_id in range(data_model["num_vehicles"]):
        index = routing.Start(vehicle_id)
        plan_output = f"Route for vehicle {vehicle_id}:\n"
        route_distance = 0
        while not routing.IsEnd(index):
            plan_output += f" {manager.IndexToNode(index)} -> "
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id
            )
        plan_output += f"{manager.IndexToNode(index)}\n"
        plan_output += f"Distance of the route: {route_distance}m\n"
        print(plan_output)
        total_distance += route_distance
    print(f"Total Distance of all routes: {total_distance}m")

def solver():
    """Entry point of the program."""
    # Instantiate the data problem.
    data = create_data()
    data_model = create_data_model(data["addresses"], data["API_key"])

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data_model["distance_matrix"]), data_model["num_vehicles"], data_model["starts"], data_model["ends"]
    )

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Define cost of each arc.
    def distance_callback(from_index, to_index):
        """Returns the manhattan distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data_model["distance_matrix"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Distance constraint.
    dimension_name = "Distance"
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        sys.maxsize,  # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name,
    )
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION
    )

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(data_model, manager, routing, solution)
    else:
        print("There is no solution")

def main():
    """Entry point of the program."""
    # Instantiate the data problem.
    data = get_data()
    data_model = create_data_model1(data["addresses"], data["API_key"])

    # Create the routing index manager.
    def distance_callback(from_index, to_index):
        """Returns the manhattan distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data_model["distance_matrix"][from_node][to_node]
    


if __name__ == "__main__":
    main()
