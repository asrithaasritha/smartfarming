async function fetchFarmData() {
    try {
        const response = await fetch("http://127.0.0.1:5000/get_data");
        const data = await response.json();

        const dashboard = document.getElementById("dashboard");
        dashboard.innerHTML = ""; // Clear previous data

        for (const [farm, farmDetails] of Object.entries(data.farm_data)) {
            const farmSolutions = data.farm_solutions[farm];

            const farmContainer = document.createElement("div");
            farmContainer.className = "farm-container";
            farmContainer.innerHTML = `<h2>${farm.toUpperCase()}</h2>`;

            for (const [location, sensor] of Object.entries(farmDetails.sensors)) {
                const solutionText = farmSolutions?.actions
                    .filter(action => action.includes(`Direction: ${location}`))
                    .join(", ") || "No action needed";

                const farmCard = document.createElement("div");
                farmCard.className = "farm-card";
                farmCard.innerHTML = `
                    <h3>${location.toUpperCase()}</h3>
                    <p class="sensor-data">🌿 Soil Moisture: ${sensor.soil_moisture ?? "N/A"}%</p>
                    <p class="sensor-data">🌡️ Temperature: ${sensor.temperature ?? "N/A"}°C</p>
                    <p class="sensor-data">💧 Humidity: ${sensor.humidity ?? "N/A"}%</p>
                    <p class="sensor-data">☀️ Light Intensity: ${sensor.light_intensity ?? "N/A"} Lux</p>
                    <p class="sensor-data">🌧️ Rainfall: ${sensor.rainfall ?? "N/A"} mm</p>
                    <p class="solution">🚀 Solution: ${solutionText}</p>
                `;

                farmContainer.appendChild(farmCard);
            }

            dashboard.appendChild(farmContainer);
        }
    } catch (error) {
        console.error("Error fetching data:", error);
    }
}

// Refresh data every 5 seconds
setInterval(fetchFarmData, 5000);
fetchFarmData();
