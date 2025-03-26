function loginButton() {
  window.location.href = "login.html";
}

// document.addEventListener("DOMContentLoaded", fetchServices);

// async function fetchServices() {
//     try {
//         const response = await fetch("http://127.0.0.1:8000/services/get");
//         if (!response.ok) {
//             throw new Error(`HTTP error! Status: ${response.status}`);
//         }
      
//         const data = await response.json();
//         const services = data.services; // Access the array inside "services"
//         const cardContainer = document.getElementById("cardContainer");
//         cardContainer.innerHTML = ""; // Clear previous content

//         services.forEach(service => {
//             if (service.ser_avl) { // Only display available services
//                 const card = document.createElement("div");
//                 card.classList.add("card");
//                 card.style.width = "18rem";

//                 card.innerHTML = `
//                     <img src="${service.ser_image}" class="card-img-top" alt="${service.ser_name}">
//                     <div class="card-body">
//                         <h5 class="card-title">${service.ser_name}</h5>
//                         <h4 class="card-amt">Rs.500/-</h4>
//                         <p class="card-text">${service.ser_desc}</p>
//                         <div class="btn-container">
//                             <button class="card-btn-1">Know More</button>
//                             <button class="card-btn-2">Book Now</button>
//                         </div>
//                     </div>
//                 `;

//                 cardContainer.appendChild(card);
//             }
//         });

//     } catch (error) {
//         console.error("Error fetching services:", error);
//     }
// }


fetch("http://127.0.0.1:8000/services/get")
.then(response => response.json())
.then(data => {
  const servicesContainer = document.getElementById("services-container");
  servicesContainer.innerHTML = "";

  data.services.forEach(service => {
    const card = document.createElement("div");
    card.classList.add("card");

    card.innerHTML = `
      <img src="${service.ser_image}" alt="${service.ser_name}" class="card-img">
      <h3>${service.ser_name}</h3>
      <p>${service.ser_desc}</p>
      <p><strong>Available:</strong> ${service.ser_avl ? "Yes" : "No"}</p>
    `;

    servicesContainer.appendChild(card);
  });
})
.catch(error => console.error("Error:", error));
