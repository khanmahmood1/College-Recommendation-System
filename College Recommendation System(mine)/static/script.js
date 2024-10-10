document.getElementById('recommendationForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the form from submitting

    // Get values from the form
    const percentile = document.getElementById('percentile').value;
    const branch = document.getElementById('branch').value;
    const gender = document.getElementById('gender').value;
    const category = document.getElementById('category').value;

    // Create a data object to send to the backend
    const data = {
        percentile: parseFloat(percentile),
        branch: branch,
        gender: gender,
        category: category
    };

    // Send a POST request to the Flask server
    fetch('/recommend', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(recommendations => {
        let resultDiv = document.getElementById('result');
        resultDiv.innerHTML = `<h3>Top Recommended Colleges:</h3>`;

        if (recommendations.length === 0) {
            resultDiv.innerHTML += `<p>No colleges found matching your criteria.</p>`;
        } else {
            recommendations.forEach(college => {
                resultDiv.innerHTML += `<p>${college.name} (Percentile: ${college.percentile} | Rank: ${college.rank})</p>`;
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
