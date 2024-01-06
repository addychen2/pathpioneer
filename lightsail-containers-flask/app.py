from pathOrganizer import main
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/')
def hellopage():
    return "calculate route uploaded! 5"

@app.route('/haha', methods = ['POST'])
def haha():
    data = request.json
    Arg = data.get('API_key')
    return Arg

@app.route('/hehe', methods = ['GET'])
def hehe():
    Var = "Hello World"
    return jsonify(Var)

@app.route('/calculateRoute', methods = ['POST'])
def calculateRoute():
    # Extract the API key from the request
    data = request.json
    API_key = data.get('API_key')

    # Extract addresses as a JSON string and then parse it into a Python list of lists
    addresses_json = data.get('addresses')
    try:
        addresses = json.loads(addresses_json)
        if not all(isinstance(addr_list, list) and all(isinstance(addr, str) for addr in addr_list) for addr_list in addresses):
            raise ValueError("Invalid address format")
    except ValueError as e:
        return jsonify({'error': f'Invalid addresses format: {str(e)}'}), 400

    # Use the get_data function to process the API key and addresses
    # Note: You might need to modify the get_data function in pathOrganizer.py accordingly
    route_data = main(API_key, addresses)

    # Return the organized route as a JSON response
    return jsonify(route_data)

if __name__ == "__main__":
   app.debug = True
   app.run(host='0.0.0.0', port=5000)