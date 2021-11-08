$("button").click(function () {
  swal ( "Oops" ,  "Something went wrong!" ,  "error" )
  var formElements = document.getElementById("noteForm").elements;
  var jsonObj = {};
  for (let i = 0; i < formElements.length - 2; i++) {
    jsonObj[formElements[i].name] = formElements[i].value;
    formElements[i].value = "";
  }
  for (let i = 0; i < formElements.length - 1; i++) {
    formElements[i].value = "";
  }
  var url = 'http://localhost:5000/registerUser';
  var data = jsonObj;
  
  fetch(url, {
    method: 'POST',
    body: JSON.stringify(data),
    headers:{
      'Content-Type': 'application/json'
    }
  }).then(res => res.json())
  .catch(error => console.error('Error:', error))
  .then(response => console.log('Success:', response));
})

