document.addEventListener('DOMContentLoaded', function () {
  // Trucks code (unchanged)
  const addTruckBtn = document.getElementById('addTruckBtn');
  const trucksContainer = document.getElementById('trucksContainer');
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

  // Locations code (updated for dropdowns)
  const addLocationBtn = document.getElementById('addLocationBtn');
  const locationSelect = document.getElementById('locationSelect');
  const extraLocationsContainer = document.getElementById('extraLocationsContainer');

  addLocationBtn.addEventListener('click', () => {
    // Optionally: Don't add if nothing is selected
    if (!locationSelect.value) {
      alert('Please select a location first.');
      return;
    }

    // Create new select (dropdown) element
    const newSelect = document.createElement('select');
    newSelect.name = 'locations[]';
    newSelect.style.marginTop = '10px';
    // Duplicate options from the original select
    Array.from(locationSelect.options).forEach(opt => {
      newSelect.appendChild(opt.cloneNode(true));
    });
    // Set selected to the last chosen
    newSelect.value = locationSelect.value;

    extraLocationsContainer.appendChild(newSelect);

    // Reset main select for next input
    locationSelect.value = '';
  });
});
