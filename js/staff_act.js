// document.addEventListener("DOMContentLoaded", function () {
//     fetchRoles();
//     fetchStaffs(); 

//     document.getElementById("staffForm").addEventListener("submit", async function (event) {
//         event.preventDefault();
//         registerStaff();
//     });
// });

// // **Fetch Roles & Populate Dropdown**
// async function fetchRoles() {
//     try {
//         const response = await fetch("http://127.0.0.1:8000/roles/get");
//         const data = await response.json();
//         console.log("Roles Data:", data);

//         const roleDropdown = document.getElementById("roleDropdown");
//         roleDropdown.innerHTML = ""; // Clear existing options

//         data.roles.forEach(role => {
//             const option = document.createElement("option");
//             option.value = role.role_id;
//             option.textContent = role.role;
//             roleDropdown.appendChild(option);
//         });
//     } catch (error) {
//         console.error("Error fetching roles:", error);
//         alert("Failed to load roles.");
//     }
// }

// // **Fetch Staffs & Populate Table**
// async function fetchStaffs() {
//     try {
//         const response = await fetch("http://127.0.0.1:8000/staffs/get");
//         const data = await response.json();
//         console.log("Staff Data:", data);

//         const staffTableBody = document.getElementById("staffTableBody");
//         staffTableBody.innerHTML = "";

//         data.staffs.forEach(staff => {
//             const row = document.createElement("tr");

//             row.innerHTML = `
//                 <td>${staff.staff_id}</td>
//                 <td>${staff.s_name}</td>
//                 <td>${staff.role}</td>
//                 <td>
//                     <button class="btn ${staff.activity ? 'btn-danger' : 'btn-success'}" 
//                         onclick="toggleStaffActivity(${staff.staff_id}, ${staff.activity})">
//                         ${staff.activity ? 'Block' : 'Unblock'}
//                     </button>
//                 </td>
//             `;

//             staffTableBody.appendChild(row);
//         });
//     } catch (error) {
//         console.error("Error fetching staff data:", error);
//         alert("Failed to load staff data.");
//     }
// }

// // **Toggle Staff Activity (Block/Unblock)**
// async function toggleStaffActivity(staffId, currentActivity) {
//     const newActivity = !currentActivity; // Toggle activity

//     try {
//         const response = await fetch(`http://127.0.0.1:8000/staffs/update-activity/${staffId}`, {
//             method: "PUT", // Try PATCH if PUT is incorrect
//             headers: {
//                 "Content-Type": "application/json"
//             },
//             body: JSON.stringify({ activity: newActivity })
//         });

//         if (response.ok) {
//             alert(`Staff ${newActivity ? 'unblocked' : 'blocked'} successfully!`);
//             fetchStaffs(); // Refresh table
//         } else {
//             const errorMessage = await response.text();
//             console.error("Error updating staff activity:", errorMessage);
//             alert(`Failed to update staff activity: ${errorMessage}`);
//         }
//     } catch (error) {
//         console.error("Error:", error);
//         alert("Failed to update staff activity.");
//     }
// }
// document.addEventListener("DOMContentLoaded", function () {
//     fetchRoles();
//     fetchStaffs(); 

//     document.getElementById("staffForm").addEventListener("submit", async function (event) {
//         event.preventDefault();
//         registerStaff();
//     });
// });

// // **Fetch Roles & Populate Dropdown**
// async function fetchRoles() {
//     try {
//         const response = await fetch("http://127.0.0.1:8000/roles/get");
//         const data = await response.json();
//         console.log("Roles Data:", data);

//         const roleDropdown = document.getElementById("roleDropdown");
//         roleDropdown.innerHTML = ""; // Clear existing options

//         data.roles.forEach(role => {
//             const option = document.createElement("option");
//             option.value = role.role_id;
//             option.textContent = role.role;
//             roleDropdown.appendChild(option);
//         });
//     } catch (error) {
//         console.error("Error fetching roles:", error);
//         alert("Failed to load roles.");
//     }
// }

// // **Fetch Staffs & Populate Table**
// async function fetchStaffs() {
//     try {
//         const response = await fetch("http://127.0.0.1:8000/staffs/get");
//         const data = await response.json();
//         console.log("Staff Data:", data);

//         const staffTableBody = document.getElementById("staffTableBody");
//         staffTableBody.innerHTML = "";

//         data.staffs.forEach(staff => {
//             const row = document.createElement("tr");

//             row.innerHTML = `
//                 <td>${staff.staff_id}</td>
//                 <td>${staff.s_name}</td>
//                 <td>${staff.role}</td>
//                 <td>
//                     <button class="btn ${staff.activity ? 'btn-danger' : 'btn-success'}" 
//                         onclick="toggleStaffActivity(${staff.staff_id}, ${staff.activity})">
//                         ${staff.activity ? 'Block' : 'Unblock'}
//                     </button>
//                 </td>
//             `;

//             staffTableBody.appendChild(row);
//         });
//     } catch (error) {
//         console.error("Error fetching staff data:", error);
//         alert("Failed to load staff data.");
//     }
// }

// // **Toggle Staff Activity (Block/Unblock)**
// async function toggleStaffActivity(staffId, currentActivity) {
//     const newActivity = !currentActivity; // Toggle activity

//     try {
//         const response = await fetch(`http://127.0.0.1:8000/staffs/update-activity/${staffId}`, {
//             method: "PUT", // Try PATCH if PUT is incorrect
//             headers: {
//                 "Content-Type": "application/json"
//             },
//             body: JSON.stringify({ activity: newActivity })
//         });

//         if (response.ok) {
//             alert(`Staff ${newActivity ? 'unblocked' : 'blocked'} successfully!`);
//             fetchStaffs(); // Refresh table
//         } else {
//             const errorMessage = await response.text();
//             console.error("Error updating staff activity:", errorMessage);
//             alert(`Failed to update staff activity: ${errorMessage}`);
//         }
//     } catch (error) {
//         console.error("Error:", error);
//         alert("Failed to update staff activity.");
//     }
// }
