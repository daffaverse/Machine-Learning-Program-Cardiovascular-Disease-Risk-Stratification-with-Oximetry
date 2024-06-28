function predictHealth() {
    const form = document.getElementById('health-form');
    const data = {
        'Gender / Sex': parseInt(form.gender.value),
        'Berat Badan (kg)': parseInt(form.weight.value),
        'Tinggi Badan (cm)': parseInt(form.height.value),
        'Detak Jantung (bpm)': parseInt(form.heart_rate.value),
        'Kadar Oksigen (%)': parseInt(form.oxygen_level.value)
    };

    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        document.getElementById('health-status').innerText = result['Predicted Health Status'];
        const diseaseProbabilities = document.getElementById('disease-probabilities');
        diseaseProbabilities.innerHTML = '';
        for (const [disease, probability] of Object.entries(result['Disease Probabilities'])) {
            const listItem = document.createElement('li');
            listItem.innerText = `${disease}: ${probability}%`;
            diseaseProbabilities.appendChild(listItem);
        }
    })
    .catch(error => console.error('Error:', error));
}
