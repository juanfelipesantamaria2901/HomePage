$("button").click(function () {
    var formElements = document.getElementById("noteForm").elements;
    var jsonObj={};
    for (let i = 0; i < formElements.length; i++) {
        jsonObj[formElements[i].name]=formElements[i].value;
        formElements[i].value = "";
    }
    console.log(jsonObj);
})