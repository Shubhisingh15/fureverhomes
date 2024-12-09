
// Feedback Form Submission
document.getElementById("feedback-form").addEventListener("submit", function (event) {
    event.preventDefault();

    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const feedback = document.getElementById("feedback").value.trim();

    if (name && email && feedback) {
        alert(`Thank you, ${name}, for your feedback!`);
        document.getElementById("feedback-form").reset(); // Reset form
    } else {
        alert("Please fill out all fields before submitting.");
    }
});

// Contact Form Submission
document.querySelector("form[action='/contact']").addEventListener("submit", function (event) {
    event.preventDefault();

    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const purpose = document.getElementById("purpose").value.trim();

    if (name && email && purpose) {
        alert(`Thank you, ${name}, for reaching out! We’ll respond soon.`);
        this.reset(); // Reset form
    } else {
        alert("Please complete all fields.");
    }
});



// Function to open the adoption form and overlay
function openForm(dogName) {
    // Set the dog name in the form title
    document.getElementById("adoptFormTitle").innerText = "Adopt " + dogName;

    // Display the form and overlay
    document.getElementById("adoptForm").style.display = "block";
}

// Function to close the form and overlay
function closeForm() {
    // Hide the form and overlay
    document.getElementById("adoptForm").style.display = "none";
    
}

// Function to handle form submission
function handleSubmit(event) {
    event.preventDefault(); // Prevent the default form submission (for demo purposes)

    // Collect the form data
    const formData = {
        name: document.getElementById("name").value,
        phone: document.getElementById("phone").value,
        address: document.getElementById("address").value,
        email: document.getElementById("email").value
    };

    console.log("Form submitted:", formData);

    // Show a confirmation message
    alert("Thank you for your adoption request! We will contact you soon.");

    // Close the form after submission
    closeForm();
}

// Adding event listener to the form submit button
document.getElementById("adoptForm").addEventListener("submit", handleSubmit);



// Donate Form Submission
document.querySelector("form[action='/donate']").addEventListener("submit", function (event) {
    event.preventDefault();

    const donationAmount = document.getElementById("donation-amount").value;

    if (donationAmount && donationAmount > 0) {
        alert(`Thank you for your generous donation of ₹${donationAmount}!`);
        this.reset(); // Reset form
    } else {
        alert("Please enter a valid donation amount.");
    }
});

// Search Form (Optional: Enhance with JavaScript for instant results)
document.querySelector("form[action='/search']").addEventListener("submit", function (event) {
    const query = this.querySelector("input[name='query']").value.trim();

    if (!query) {
        event.preventDefault(); // Prevent submission if query is empty
        alert("Please enter a search term.");
    } else {
        alert(`Searching for "${query}"...`);
    }
});
const dogs = [
    {
      name: "Max",
      breed: "Indie",
      image: "https://via.placeholder.com/300?text=Labrador",
    },
    {
      name: "Bella",
      breed: "Indie",
      image: "https://via.placeholder.com/300?text=Poodle",
    },
    {
      name: "Rocky",
      breed: "indie",
      image: "https://via.placeholder.com/300?text=Bulldog",
    },
  ];
function searchDog() {
    const input = document.getElementById("breed-input").value.trim().toLowerCase();
    const dogDisplay = document.getElementById("dog-display");
    const dogImage = document.getElementById("dog-image");
    const dogName = document.getElementById("dog-name");
    const dogBreed = document.getElementById("dog-breed");

    const foundDog = dogs.find(dog => dog.breed.toLowerCase() === input);

  
  function displayDogs(dogs) {
    const dogGrid = document.getElementById('dog-grid');
    dogGrid.innerHTML = ''; // Clear previous results

    if (dogs.length > 0) {
      dogs.forEach(dog => {
        const dogCard = document.createElement('div');
        dogCard.classList.add('dog-card');

        dogCard.innerHTML = `
          <img src="${dog.image}" alt="${dog.name}">
          <h3>${dog.name}</h3>
          <p>${dog.breed}</p>
        `;

        dogGrid.appendChild(dogCard);
      });
    } else {
      dogGrid.innerHTML = '<p>No dogs found for this breed.</p>';
    }
  }

  // Function to handle breed search
  function searchBreed() {
    const searchValue = document.getElementById('breed-search').value.toLowerCase();
    
    // Filter dogs based on the breed entered
    const filteredDogs = allDogs.filter(dog => dog.breed.toLowerCase().includes(searchValue));

    // Display the filtered dogs
    displayDogs(filteredDogs);
  }
</script>