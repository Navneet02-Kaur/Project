document.getElementById("carbonForm").addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent page reload

    let formData = new FormData(this); // Collect form data

    fetch("/calculator/", {
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value  // Fetch CSRF Token from form
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.carbon_emission) {
            console.log("Received Data:", data); // Debugging - See what Django is sending

            document.getElementById("totalCarbon").innerText = data.carbon_emission.toFixed(2) + " tonnes CO2e";
            document.getElementById("energyCarbon").innerText = data.energy.toFixed(2);
            document.getElementById("transportCarbon").innerText = data.transport.toFixed(2);
            document.getElementById("wasteCarbon").innerText = data.waste.toFixed(2);
            document.getElementById("foodCarbon").innerText = data.food.toFixed(2);
            document.getElementById("waterCarbon").innerText = data.water.toFixed(2);
            document.getElementById("goodsCarbon").innerText = data.goods.toFixed(2);
            document.getElementById("renewableCarbon").innerText = data.renewable.toFixed(2);
            document.getElementById("lifestyleCarbon").innerText = data.lifestyle.toFixed(2);

            document.getElementById("results").classList.remove("hidden"); // Show results section
        } else {
            console.error("Error in response:", data);
            alert("Error calculating carbon footprint. Check console for details.");
        }
    })
    .catch(error => {
        console.error("Fetch error:", error);
        alert("Something went wrong! Check console for details.");
    });
});

// Function to get CSRF token from cookies
function getCSRFToken() {
    let cookieValue = null;
    if (document.cookie) {
        document.cookie.split(";").forEach(cookie => {
            let [name, value] = cookie.trim().split("=");
            if (name === "csrftoken") {
                cookieValue = decodeURIComponent(value);
            }
        });
    }
    return cookieValue;
}
