import socket
import json
import time

def process_farm_data(data):
    """ Analyze sensor data and determine farm actions. """
    farm_id = data["farm_id"]
    sensors = data["sensors"]
    actions = []

    # Loop through each sensor to process the data
    for direction, sensor_data in sensors.items():
        soil_moisture = sensor_data["soil_moisture"]
        temperature = sensor_data["temperature"]
        humidity = sensor_data["humidity"]
        light_intensity = sensor_data["light_intensity"]
        rainfall = sensor_data["rainfall"]

        # 🌱 Soil Moisture Control
        if soil_moisture < 40:
            actions.append(f"Start Irrigation 🚰 (Direction: {direction})")
        elif soil_moisture > 80:
            actions.append(f"Stop Irrigation 🚱 (Direction: {direction})")

        # 🌡️ Temperature Control
        if temperature > 35:
            actions.append(f"Activate Cooling 🌬️ (Direction: {direction})")
        elif temperature < 10:
            actions.append(f"Activate Heating 🔥 (Direction: {direction})")

        # 💧 Humidity Control
        if humidity > 80:
            actions.append(f"Improve Ventilation 💨 (Direction: {direction})")
        elif humidity < 30:
            actions.append(f"Start Mist Spray 💦 (Direction: {direction})")

        # ☀️ Light Intensity Control
        if light_intensity > 80:
            actions.append(f"Activate Shade 🌳 (Direction: {direction})")
        elif light_intensity < 20:
            actions.append(f"Increase Light Exposure 🔆 (Direction: {direction})")

        # 🌧️ Rainfall Monitoring
        if rainfall > 80:
            actions.append(f"Prepare for Flooding ⚠️ (Direction: {direction})")
        elif rainfall < 5:
            actions.append(f"Monitor Drought Risk 🔥 (Direction: {direction})")

    solution = {"farm_id": farm_id, "actions": actions}

    print(f"✅ Processed Solution for {farm_id}: {solution}")  # 🔍 Debugging output
    return solution

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 6000))
    server_socket.listen(5)
    server_socket.settimeout(1.0)  # Allows checking for Ctrl+C

    print("🚀 TCP Server running on port 6000... Press Ctrl+C to stop.")

    try:
        while True:
            try:
                client, addr = server_socket.accept()
                print(f"🌐 Connection from {addr}")

                data = client.recv(4096).decode()  # Increased buffer size
                if not data:
                    continue

                farm_data = json.loads(data)
                print(f"📥 Received Data: {json.dumps(farm_data, indent=2)}")  # Pretty print data

                # Process farm data
                response = process_farm_data(farm_data)

                # Send response back to API
                client.send(json.dumps(response).encode())  # ✅ Ensure response is sent
                client.close()

            except socket.timeout:
                pass  # Prevent blocking, allows server to shut down gracefully

    except KeyboardInterrupt:
        print("\n🛑 Server shutting down gracefully...")
        server_socket.close()
        time.sleep(1)
        print("✅ Server stopped successfully.")

if __name__ == "__main__":
    start_server()
