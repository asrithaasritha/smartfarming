from flask import Flask, request, jsonify
from flask_cors import CORS
import socket
import json

app = Flask(__name__)
CORS(app)

# Store latest farm data & solutions dynamically
farm_data = {}
farm_solutions = {}

def send_to_tcp_server(data):
    """ Sends data to TCP Server and receives the solution """
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("localhost", 6000))  # Connect to TCP server
        client.send(json.dumps(data).encode())  # Send farm data as JSON
        
        # Receive response from TCP server (increase buffer size for large responses)
        response = client.recv(4096).decode()
        client.close()

        print(f"✅ Received Solution from TCP: {response}")  # Debugging output

        try:
            return json.loads(response)  # Convert response to JSON
        except json.JSONDecodeError:
            print("❌ Error: Invalid JSON from TCP Server")
            return {"error": "Invalid response from TCP Server"}
    except Exception as e:
        print(f"❌ Error connecting to TCP Server: {e}")  # Debugging output
        return {"error": f"TCP Server unreachable: {str(e)}"}

@app.route('/send_data', methods=['POST'])
def receive_data():
    """ Receives farm data and forwards it to TCP server """
    data = request.json
    farm_id = data.get("farm_id")

    if not farm_id:
        return jsonify({"error": "Farm ID is required"}), 400

    # Store latest farm data dynamically
    farm_data[farm_id] = data

    # Forward data to TCP server for processing
    response_from_server = send_to_tcp_server(data)

    # Store solution
    farm_solutions[farm_id] = response_from_server

    return jsonify({"message": "Data received", "server_response": response_from_server})

@app.route('/get_data', methods=['GET'])
def get_data():
    """ Returns stored farm data and their respective solutions """
    return jsonify({"farm_data": farm_data, "farm_solutions": farm_solutions})

@app.route('/get_solution/<farm_id>', methods=['GET'])
def get_solution(farm_id):
    """ Returns the latest solution for the requested farm """
    if farm_id not in farm_solutions:
        return jsonify({"error": "No solution available for this farm"}), 404

    return jsonify({"farm_id": farm_id, "solution": farm_solutions.get(farm_id, "No solution yet")})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
