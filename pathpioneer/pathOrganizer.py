from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import sys
import json
import urllib.request

def create_data(API_key, addresses):
        data = {}
        data['API_key'] = API_key
        data['addresses'] = addresses
        return data

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
    data_model['addresses'] = data['addresses']
    data_model["distance_matrix"] = create_distance_matrix(data)
    data_model["addresses_hierarchy_index"] = create_index(addresses_hierarchy)
    data_model["addresses_no_start_end"] = data_model["addresses_hierarchy_index"][1:-1]
    data_model["start_end"] = []
    for i in range(len(data_model["addresses_no_start_end"]) - 1):
        start = data_model["addresses_no_start_end"][i]
        end = data_model["addresses_no_start_end"][i + 1]
        data_model["start_end"].append(get_start_end(start, end, data_model["distance_matrix"]))
    data_model["start_end_full"] = restructure_array(data_model["start_end"], data_model)
    data_model["start_end_addresses"] = []
    #for index_tuple in data_model["start_end"]:
        #start, end = index_tuple
        #data_model["start_end_addresses"].append((data['addresses'][start], data['addresses'][end]))
    #print(data_model["start_end_addresses"])
    return data_model

def restructure_array(input_tuples, data_model):
    # Extracting the first and last elements from addresses_hierarchy_index
    first_element = data_model['addresses_hierarchy_index'][0][0]
    last_element = data_model['addresses_hierarchy_index'][-1][0]

    # Initializing the result array with the first element
    result = [(first_element, input_tuples[0][0])]

    # Looping through the input tuples and restructuring
    for i in range(len(input_tuples) - 1):
        # Adding a tuple with the second element of the current tuple and the first element of the next tuple
        result.append((input_tuples[i][1], input_tuples[i + 1][0]))

    # Adding the last element to the result array
    result.append((input_tuples[-1][1], last_element))

    return result

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
    data_model["addresses"] = addresses
    data_model["distance_matrix"] = create_distance_matrix(data)
    data_model["num_vehicles"] = 1
    data_model["starts"] = [0]
    data_model["ends"] = [1]
    return data_model

def get_vehicle_routes(data_model, manager, routing, solution):
    """Returns the routes for each vehicle."""
    routes = []
    for vehicle_id in range(data_model["num_vehicles"]):
        index = routing.Start(vehicle_id)
        route = []
        while not routing.IsEnd(index):
            route.append(data_model["addresses"][manager.IndexToNode(index)])
            index = solution.Value(routing.NextVar(index))
        route.append(data_model["addresses"][manager.IndexToNode(index)])  # Add the end node
        routes.append(route)
    return routes

def print_solution(data_model, manager, routing, solution):
    """Prints solution on console."""
    print(f"Objective: {solution.ObjectiveValue()}")
    total_distance = 0
    for vehicle_id in range(data_model["num_vehicles"]):
        index = routing.Start(vehicle_id)
        plan_output = f"Route for vehicle {vehicle_id}:\n"
        route_distance = 0
        while not routing.IsEnd(index):
            plan_output += f" {[manager.IndexToNode(index)]} -> "
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id
            )
        plan_output += f"{[manager.IndexToNode(index)]}\n"
        plan_output += f"Distance of the route: {route_distance}m\n"
        print(plan_output)
        total_distance += route_distance
    print(f"Total Distance of all routes: {total_distance}m")

def solver(API_key, addresses):
    """Entry point of the program."""
    # Instantiate the data problem.
    data = create_data(API_key, addresses)
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
        #print_solution(data_model, manager, routing, solution)
        vehicle_routes = get_vehicle_routes(data_model, manager, routing, solution)
        return vehicle_routes
    else:
        print("There is no solution")

def main():
    """Entry point of the program."""
    # Instantiate the data problem.
    data = get_data()
    data_model1 = create_data_model1(data["addresses"], data["API_key"])
    input_array_index = modify_arrays(data_model1["start_end_full"], data_model1["addresses_no_start_end"])
    input_array = map_indexes_to_elements(input_array_index, data_model1["addresses"])
    # Create the routing index manager.
    routes_2d = []
    for hierarchy in input_array:
        routes_2d += solver(data["API_key"], hierarchy)
    route = flatten_2d_array(routes_2d)
    print(route)

def modify_arrays(tuples_array, arrays_2d):
    modified_arrays = []

    for tup, arr in zip(tuples_array, arrays_2d):
        # Create a copy of the current array
        new_arr = arr.copy()

        # Iterate over the tuple elements in reverse order (to maintain order when inserting at the front)
        for element in reversed(tup):
            # If the element is already in the array, remove it
            if element in new_arr:
                new_arr.remove(element)

            # Insert the element at the beginning of the array
            new_arr.insert(0, element)

        # Add the modified array to the result list
        modified_arrays.append(new_arr)

    return modified_arrays

def map_indexes_to_elements(indexes_2d, elements):
    result = []

    for index_array in indexes_2d:
        # Fetch elements from the 1D array using the current index array
        mapped_elements = [elements[i] for i in index_array]
        # Add the fetched elements to the result
        result.append(mapped_elements)

    return result

def flatten_2d_array(arrays_2d):
    # Using list comprehension to flatten the 2D array
    flattened_array = [element for array in arrays_2d for element in array]
    return flattened_array

if __name__ == "__main__":
    main()
