document.getElementById("prediction-form").addEventListener("submit", async function(event) {
    event.preventDefault();

    const data = {
        crop: document.getElementById("crop").value,
        temperature: parseFloat(document.getElementById("temperature").value),
        rainfall: parseFloat(document.getElementById("rainfall").value),
        humidity: parseFloat(document.getElementById("humidity").value),
        soil_moisture: parseFloat(document.getElementById("soil_moisture").value),
        pH: parseFloat(document.getElementById("pH").value),
        sunlight: parseFloat(document.getElementById("sunlight").value),
        wind_speed: parseFloat(document.getElementById("wind_speed").value),
    };

    const response = await fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    });

    const result = await response.json();
    document.getElementById("result").textContent = result.result || result.error;
});
