// Wait for the DOM to load before attaching events (optional but good practice)
document.addEventListener('DOMContentLoaded', function () {
  const addTruckBtn = document.getElementById('addTruckBtn');
  const trucksContainer = document.getElementById('trucksContainer');
  const addLocationBtn = document.getElementById('addLocationBtn');
  const locationSelect = document.getElementById('locationSelect');
  const extraLocationsContainer = document.getElementById('extraLocationsContainer');

  // Add another truck row dynamically
  addTruckBtn.addEventListener('click', () => {
    const newTruckRow = document.createElement('div');
    newTruckRow.classList.add('truck-row');
    newTruckRow.innerHTML = `
      <input name="truckNumberPlate[]" type="text" placeholder="Number Plate" />
      <input name="truckWeight[]" type="number" min="0" placeholder="Weight" />
      <input name="truckVolume[]" type="number" min="0" placeholder="Volume" />
    `;
    trucksContainer.appendChild(newTruckRow);
  });

  // Add an extra location input based on selected dropdown location
  addLocationBtn.addEventListener('click', () => {
    const selectedValue = locationSelect.value;
    if (!selectedValue) {
      alert('Please select a location first.');
      return;
    }
    const locInput = document.createElement('input');
    locInput.type = 'text';
    locInput.name = 'extraLocations[]';
    locInput.value = locationSelect.options[locationSelect.selectedIndex].text;
    locInput.readOnly = true;
    locInput.style.marginTop = '10px';
    extraLocationsContainer.appendChild(locInput);
    locationSelect.value = '';
  });
});
