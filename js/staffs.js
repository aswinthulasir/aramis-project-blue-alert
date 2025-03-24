async function fetchStaffsAndRoles() {
    try {
        // Fetch staff details
        const staffResponse = await fetch("http://127.0.0.1:8000/staffs/get");
        const staffData = await staffResponse.json();

        console.log("Staff Data:", staffData); // Debugging line

        // Ensure staffData is an array
        const staffs = Array.isArray(staffData) ? staffData : staffData.staffs || [];

        // Fetch role details
        const roleResponse = await fetch("http://127.0.0.1:8000/roles/get");
        const rolesData = await roleResponse.json();

        console.log("Roles Data:", rolesData); // Debugging line

        // Convert role array into a map { role_id: role_name }
        const rolesMap = {};
        if (Array.isArray(rolesData.roles)) {
            rolesData.roles.forEach(role => {
                rolesMap[role.role_id] = role.role;
            });
        }

        populateStaffTable(staffs, rolesMap);
    } catch (error) {
        console.error("Error fetching staff/roles:", error);
    }
}

function populateStaffTable(staffs, rolesMap) {
    const tableBody = document.getElementById("staffTableBody");
    tableBody.innerHTML = ""; // Clear table before adding rows

    staffs.forEach(staff => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${staff.staff_id}</td>
            <td>${staff.s_name}</td>
            <td>${rolesMap[staff.role_id] || "Unknown Role"}</td>
            <td>
               <button 
    class="btn ${staff.activity ? 'btn-success' : 'btn-danger'} btn-sm" 
    onclick="toggleActivity(${staff.staff_id}, ${staff.activity ? 'true' : 'false'})"
>
    ${staff.activity ? "Active" : "Not Active"}
</button>

            </td>
        `;

        tableBody.appendChild(row);
    });
}

async function toggleActivity(staffId, currentStatus) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/staffs/update-activity/${staffId}`, {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ activity: !currentStatus }) // Toggle the value
        });

        if (response.ok) {
            await fetchStaffsAndRoles(); // Refresh table after update
        } else {
            alert("Failed to update activity.");
        }
    } catch (error) {
        console.error("Error updating activity:", error);
    }
}

// Load data when page loads
document.addEventListener("DOMContentLoaded", fetchStaffsAndRoles);
