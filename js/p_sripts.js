
fetch("http://127.0.0.1:8000/patients/get")
    .then(response => response.json())
    .then(data => {
        console.log("Fetched Patients Data:", data);
        if (Array.isArray(data.patients)) {
            displayPatients(data.patients); 
        } else {
            console.error("Invalid data format:", data);
        }
    })
    .catch(error => console.error("Error fetching patient data:", error));

function displayPatients(patients) {
    let gridContainer = document.getElementById("patientGrid");
    gridContainer.innerHTML = ""; 

    let row;
    patients.forEach((patient, index) => {
        if (index % 3 === 0) {
            // Create a new row for every 3 items
            row = document.createElement("div");
            row.className = "row g-3"; // Bootstrap row with spacing ** acquired ++ bs 
            gridContainer.appendChild(row);
        }

        // Create patient card
        let col = document.createElement("div");
        col.className = "col-md-4"; // bootstrap pd fn

        col.innerHTML = `
            <div class="card shadow-sm">
                <div class="card-body">
                    <h5 class="card-title">${patient.p_name} (${patient.p_age} yrs)</h5>
                    <p class="card-text"><strong>Dept:</strong> ${patient.p_dept}</p>
                    <p class="card-text"><strong>Issue:</strong> ${patient.p_desc}</p>
                    <p class="card-text"><strong>Doctor:</strong> ${patient.p_doc}</p>
                    <a href="patient_bill.html?id=${patient.p_id}" class="btn btn-primary">View Bill</a>
                </div>
            </div>
        `;

        row.appendChild(col);
    });
}
