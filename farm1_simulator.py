import requests
import random
import time

API_URL = "http://127.0.0.1:5000/send_data"
SOLUTION_URL = "http://127.0.0.1:5000/get_solution/farm1"

def generate_sensor_data():
    """ Generate extreme values to trigger solutions more often """
    return {
        "soil_moisture": round(random.choice([random.uniform(5, 20), random.uniform(85, 100), random.uniform(40, 80)]), 2),
        "temperature": round(random.choice([random.uniform(5, 10), random.uniform(36, 45), random.uniform(20, 35)]), 2),
        "humidity": round(random.choice([random.uniform(10, 29), random.uniform(81, 100), random.uniform(30, 80)]), 2),
        "light_intensity": round(random.choice([random.uniform(0, 20), random.uniform(80, 100), random.uniform(30, 70)]), 2),
        "rainfall": round(random.choice([random.uniform(0, 5), random.uniform(80, 100), random.uniform(20, 60)]), 2)
    }

def generate_farm_data():
    """ Generate data for all 5 sensors in the farm """
    return {
        "farm_id": "farm1",
        "sensors": {
            "north": generate_sensor_data(),
            "south": generate_sensor_data(),
            "east": generate_sensor_data(),
            "west": generate_sensor_data(),
            "center": generate_sensor_data()
        }
    }

while True:
    # Send farm data to API
    farm_data = generate_farm_data()
    response = requests.post(API_URL, json=farm_data)

    if response.status_code == 200:
        print(f"🌱 [Farm 1] Sent data: {farm_data}")
    else:
        print(f"❌ [Farm 1] Failed to send data: {response.text}")

    # Fetch solution from API
    solution_response = requests.get(SOLUTION_URL)
    if solution_response.status_code == 200:
        solution_data = solution_response.json()
        print(f"✅ [Farm 1] Received Solution: {solution_data['solution']}")
    else:
        print(f"❌ [Farm 1] Failed to fetch solution")

    time.sleep(5)  # Send data and fetch solution every 5 seconds
