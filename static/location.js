function addPositionValuesToForm(position) {
  // Add geopt to form; uber ride will use location as starting point
  var latInput = document.createElement("input");
  latInput.name = "lat";
  latInput.value = position.coords.latitude;
  latInput.type = 'hidden';
  var lonInput = document.createElement("input");
  lonInput.name = "lon";
  lonInput.value = position.coords.longitude;
  lonInput.type = 'hidden';
  var form = document.getElementById('createRequest');
  form.appendChild(lonInput);
  form.appendChild(latInput);
}

navigator.geolocation.getCurrentPosition(addPositionValuesToForm);
