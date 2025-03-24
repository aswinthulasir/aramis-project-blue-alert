document.addEventListener("DOMContentLoaded", function () {
    document.querySelector("form").addEventListener("submit", async function (event) {
        event.preventDefault(); // Prevent default form submission

        loginStaff(); // Call login function
    });
});

// **Function to Handle Login**
async function loginStaff() {
    const email = document.getElementById("exampleInputEmail1").value;
    const password = document.getElementById("exampleInputPassword1").value;

    const payload = {
        email: email,
        password: password
    };

    console.log("Login Payload Sent:", JSON.stringify(payload));

    try {
        const response = await fetch("http://localhost:8000/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        const result = await response.json();

        if (response.ok) {
            alert("Login successful!");

            // Store JWT token in localStorage
            localStorage.setItem("jwt_token", result.jwt_token);
            localStorage.setItem("user_id", result.u_id); // Storing user ID for reference

            // Redirect to dashboard or home page
            window.location.href = "dashboard.html"; 
        } else {
            alert("Error: " + result.detail);
        }
    } catch (error) {
        console.error("Login Error:", error);
        alert("Failed to log in. Please try again.");
    }
}
