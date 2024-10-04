document.addEventListener('DOMContentLoaded', function() {
    const countrySelect = document.querySelector('select[name="country"]');
    const stateSelect = document.querySelector('select[name="state"]');
    const citySelect = document.querySelector('select[name="city"]');

    countrySelect.addEventListener('change', function() {
        const country = this.value;
        fetch(`/location_data?country=${country}`)
            .then(response => response.json())
            .then(data => {
                stateSelect.innerHTML = '<option value="">Select a state</option>';
                citySelect.innerHTML = '<option value="">Select a city</option>';
                if (data.states) {
                    data.states.forEach(state => {
                        const option = document.createElement('option');
                        option.value = state;
                        option.textContent = state;
                        stateSelect.appendChild(option);
                    });
                }
            });
    });

    stateSelect.addEventListener('change', function() {
        const country = countrySelect.value;
        const state = this.value;
        fetch(`/location_data?country=${country}&state=${state}`)
            .then(response => response.json())
            .then(data => {
                citySelect.innerHTML = '<option value="">Select a city</option>';
                if (data.cities) {
                    data.cities.forEach(city => {
                        const option = document.createElement('option');
                        option.value = city;
                        option.textContent = city;
                        citySelect.appendChild(option);
                    });
                }
            });
    });
});
