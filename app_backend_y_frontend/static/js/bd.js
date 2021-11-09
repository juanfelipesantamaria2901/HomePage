$("button").click(function () {
  var formElements = document.getElementById("noteForm").elements;
  var jsonObj = {};
  for (let i = 0; i < formElements.length - 2; i++) {
    jsonObj[formElements[i].name] = formElements[i].value;
    formElements[i].value = "";
  }
  for (let i = 0; i < formElements.length - 1; i++) {
    formElements[i].value = "";
  }

  // var url = 'http://192.168.10.23:5000/login';
  var url = 'http://localhost:5000/login'; //Asi le sirve a Julián :)
  var data = jsonObj;

  fetch(url, {
    method: 'POST',
    body: JSON.stringify(data),
    headers: {
      'Content-Type': 'application/json'
    }
  }).then(res => res.json())
    .then(response => swal("Verifique", `${response.message}`, "warning"));


})

