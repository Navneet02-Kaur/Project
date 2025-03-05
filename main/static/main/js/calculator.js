document.addEventListener("DOMContentLoaded", function () {
    let carbonForm = document.getElementById("carbonForm");

    if (carbonForm) {  // ✅ Ensure the form exists before adding event listener
        carbonForm.addEventListener("submit", function (event) {
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
                    if (data.remark) {
                        let remarkElement = document.createElement("p");
                        remarkElement.innerText = data.remark;
                        remarkElement.classList.add("remark");
                        document.querySelector(".results-section").appendChild(remarkElement);
                    }
                    
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
    } else {
        console.error("❌ Error: The form with ID 'carbonForm' was not found!");
    }
});
