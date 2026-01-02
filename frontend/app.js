function showPage(id) {
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.getElementById(id).classList.add('active');
}

// ----------- IMAGE PREVIEW ----------
function previewImage(event) {
    const file = event.target.files[0];
    if (!file) return;

    const img = document.getElementById("previewImg");
    img.src = URL.createObjectURL(file);
    img.classList.remove("hidden");
}
function previewSkincareImage(event) {
    const file = event.target.files[0];
    if (!file) return;

    const img = document.getElementById("skcarePreview");
    img.src = URL.createObjectURL(file);
    img.classList.remove("hidden");
}

// ----------- DISEASE DETECTION ----------
document.getElementById("detectBtn").addEventListener("click", async () => {

    const file = document.getElementById("diseaseInput").files[0];
    if (!file) return alert("Please upload an image first!");

    document.getElementById("detectLoader").classList.remove("hidden");

    const form = new FormData();
    form.append("file", file);

    try {
        const response = await fetch("http://127.0.0.1:8000/api/detect", {
            method: "POST",
            body: form
        });

        const data = await response.json();
        document.getElementById("detectLoader").classList.add("hidden");

        document.getElementById("diseaseName").textContent = data.disease;
        document.getElementById("confText").textContent = (data.confidence * 100).toFixed(2) + "%";
        document.getElementById("sevText").textContent = data.severity;
        document.getElementById("advText").textContent = data.advice;

        document.getElementById("diseaseResult").classList.remove("hidden");

    } catch (error) {
        document.getElementById("detectLoader").classList.add("hidden");
        alert("Error analyzing image.");
    }
});


// ----------- SKINCARE RECOMMENDATION ----------
document.getElementById("skincareBtn").addEventListener("click", async () => {

    const file = document.getElementById("skcareImage").files[0];
    if (!file) return alert("Please upload a face image!");

    const profile = {
        skin_type: document.getElementById("q_skin_type").value,
        sensitivity: document.getElementById("q_sensitivity").value,
        frequency_of_product_use: document.getElementById("q_frequency").value,
        sun_exposure: document.getElementById("q_sun").value,
        sleep_quality: document.getElementById("q_sleep").value,
        goal: document.getElementById("q_goal").value,
        diet_habits: document.getElementById("q_diet").value,
        current_skincare_routine: document.getElementById("q_routine").value,
        sun_exposure_hours: document.getElementById("q_sun_hours").value,
        medication_affecting_skin: document.getElementById("q_med_yes").value,
        medication_text: document.getElementById("q_med_text").value
    };

    document.getElementById("skincareLoader").classList.remove("hidden");

    const form = new FormData();
    form.append("image", file);
    form.append("profile", JSON.stringify(profile));

    try {
        const response = await fetch("http://127.0.0.1:8000/api/skincare/recommend", {
            method: "POST",
            body: form
        });

        const data = await response.json();
        document.getElementById("skincareLoader").classList.add("hidden");

        if (!data.ok) {
            alert("Error generating recommendations.");
            return;
        }

        // ---------------- RENDER ROUTINE ----------------
        const routineList = document.getElementById("routineList");
        routineList.innerHTML = "";

        data.recommendations.routine.forEach(step => {
            const card = `
                <div class="routine-card">
                    <div class="routine-step">Step ${step.step} (${step.when})</div>
                    <div class="routine-action">${step.action}</div>
                    ${step.notes ? `<div class="routine-notes">${step.notes}</div>` : ""}
                </div>
            `;
            routineList.innerHTML += card;
        });


        // ---------------- RENDER PRODUCTS ----------------
        const productList = document.getElementById("productList");
        productList.innerHTML = "";

        data.recommendations.products.forEach(p => {
            const card = `
                <div class="product-card">
                    <h4>${p.name}</h4>
                    <p class="why">${p.why}</p>

                    <strong>Key Ingredients:</strong>
                    <ul>
                        ${p.key_ingredients.map(i => `<li>${i}</li>`).join("")}
                    </ul>

                    <p><strong>Suitable for:</strong> ${p.suitable_for}</p>
                </div>
            `;
            productList.innerHTML += card;
        });


        // ---------------- SAFETY NOTES ----------------
        const safetyList = document.getElementById("safetyList");
        safetyList.innerHTML = "";

        data.recommendations.safety_notes.forEach(note => {
            safetyList.innerHTML += `<li>${note}</li>`;
        });

        document.getElementById("skincareResult").classList.remove("hidden");

    } catch (err) {
        document.getElementById("skincareLoader").classList.add("hidden");
        alert("Error contacting server.");
    }
});
