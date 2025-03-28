document.addEventListener("DOMContentLoaded", function () {
    fetchRoles(); // Fetch roles automatically when the page is loaded

    document.getElementById("staffForm").addEventListener("submit", async function(event) {
        event.preventDefault(); // Prevent default form submission / submit only if the button is pressed and values are inserted
        registerStaff();
    });
});


async function fetchRoles() {
    try {
        const response = await fetch("http://127.0.0.1:8000/roles/get");
        const data = await response.json();

        const roleDropdown = document.getElementById("roleDropdown");
        roleDropdown.innerHTML = ""; // clear existing options

        data.roles.forEach(role => {
            const option = document.createElement("option");
            option.value = role.role_id;
            option.textContent = role.role;
            roleDropdown.appendChild(option);
        });
    } catch (error) {
        console.error("Error fetching roles:", error);
        alert("Failed to load roles. Try again later.");
    }
}

// Register Staff
async function registerStaff() {
    const staffName = document.getElementById("staffName").value;
    const staffEmail = document.getElementById("staffEmail").value;
    const staffPassword = document.getElementById("staffPassword").value;
    const roleId = document.getElementById("roleDropdown").value;

    const payload = {
        email: staffEmail,
        password: staffPassword,
        username: null, 
        role_id: parseInt(roleId), 
        s_name: staffName
    };

    console.log("Payload Sent:", JSON.stringify(payload));

    try {
        const response = await fetch("http://127.0.0.1:8000/users/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        const result = await response.json();
        if (response.ok) {
            alert("Staff registered successfully!");
            document.getElementById("staffForm").reset();
        } else {
            alert("Error: " + result.detail);
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Failed to register staff.");
    }
}
