const formulario = document.getElementById('formulario');
const inputs = document.querySelectorAll('#formulario input');

const expresiones = {
	nombre: /^[a-zA-ZÀ-ÿ\s]{1,50}$/,
	apellido: /^[a-zA-ZÀ-ÿ\s]{1,50}$/,
	edad: /^[0-9]{1,2}$/,
	sexo: /^[a-zA-ZÀ-ÿ\s]{1,20}$/,
	identificacion: /^[0-9]{10,11}$/,
	nacionalidad: /^[a-zA-ZÀ-ÿ\s]{1,50}$/,
	ciudad: /^[a-zA-ZÀ-ÿ\s]{1,50}$/,
	numero_telefonico: /^\d{7,14}$/,
	direccion_residencia: /^.{12,100}$/,
	ocupacion: /^[a-zA-ZÀ-ÿ\s]{1,50}$/,
	correo_electronico: /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/,
	contrasena: /^.{4,12}$/
}

const campos = {
	nombre: false,
	apellido: false,
	edad: false,
	sexo: false,
	identificacion: false,
	nacionalidad: false,
	ciudad: false,
	numero_telefonico: false,
	direccion_residencia: false,
	ocupacion: false,
	correo_electronico: false,
	contrasena: false
}

const validarFormulario = (e) => {
	switch (e.target.name) {
		case "nombre":
			validarCampo(expresiones.nombre, e.target, 'nombre');
			break;
		case "apellido":
			validarCampo(expresiones.apellido, e.target, 'apellido');
			break;
		case "edad":
			validarCampo(expresiones.edad, e.target, 'edad');
			break;
		case "sexo":
			validarCampo(expresiones.sexo, e.target, 'sexo');
			break;
		case "identificacion":
			validarCampo(expresiones.identificacion, e.target, 'identificacion');
			break;
		case "nacionalidad":
			validarCampo(expresiones.nacionalidad, e.target, 'nacionalidad');
			break;
		case "ciudad":
			validarCampo(expresiones.ciudad, e.target, 'ciudad');
			break;
		case "numero_telefonico":
			validarCampo(expresiones.numero_telefonico, e.target, 'numero_telefonico');
			break;
		case "ocupacion":
			validarCampo(expresiones.ocupacion, e.target, 'ocupacion');
			break;
		case "direccion_residencia":
			validarCampo(expresiones.direccion_residencia, e.target, 'direccion_residencia');
			break;
		case "correo_electronico":
			validarCampo(expresiones.correo_electronico, e.target, 'correo_electronico');
			break;
		case "contrasena":
			validarCampo(expresiones.contrasena, e.target, 'contrasena');
			validarContrasena2();
			break;
		case "contrasena2":
			validarContrasena2();
			break;
	}
}

const validarCampo = (expresion, input, campo) => {
	if (expresion.test(input.value)) {
		document.getElementById(`grupo__${campo}`).classList.remove('formulario__grupo-incorrecto');
		document.getElementById(`grupo__${campo}`).classList.add('formulario__grupo-correcto');
		document.querySelector(`#grupo__${campo} i`).classList.add('fa-check-circle');
		document.querySelector(`#grupo__${campo} i`).classList.remove('fa-times-circle');
		document.querySelector(`#grupo__${campo} .formulario__input-error`).classList.remove('formulario__input-error-activo');
		campos[campo] = true;
	} else {
		document.getElementById(`grupo__${campo}`).classList.add('formulario__grupo-incorrecto');
		document.getElementById(`grupo__${campo}`).classList.remove('formulario__grupo-correcto');
		document.querySelector(`#grupo__${campo} i`).classList.add('fa-times-circle');
		document.querySelector(`#grupo__${campo} i`).classList.remove('fa-check-circle');
		document.querySelector(`#grupo__${campo} .formulario__input-error`).classList.add('formulario__input-error-activo');
		campos[campo] = false;
	}
}

const validarContrasena2 = () => {
	const inputContrasena1 = document.getElementById('contrasena');
	const inputContrasena2 = document.getElementById('contrasena2');

	if (inputContrasena1.value !== inputContrasena2.value) {
		document.getElementById(`grupo__contrasena2`).classList.add('formulario__grupo-incorrecto');
		document.getElementById(`grupo__contrasena2`).classList.remove('formulario__grupo-correcto');
		document.querySelector(`#grupo__contrasena2 i`).classList.add('fa-times-circle');
		document.querySelector(`#grupo__contrasena2 i`).classList.remove('fa-check-circle');
		document.querySelector(`#grupo__contrasena2 .formulario__input-error`).classList.add('formulario__input-error-activo');
		campos['contrasena'] = false;
	} else {
		document.getElementById(`grupo__contrasena2`).classList.remove('formulario__grupo-incorrecto');
		document.getElementById(`grupo__contrasena2`).classList.add('formulario__grupo-correcto');
		document.querySelector(`#grupo__contrasena2 i`).classList.remove('fa-times-circle');
		document.querySelector(`#grupo__contrasena2 i`).classList.add('fa-check-circle');
		document.querySelector(`#grupo__contrasena2 .formulario__input-error`).classList.remove('formulario__input-error-activo');
		campos['contrasena'] = true;
	}
}

inputs.forEach((input) => {
	input.addEventListener('keyup', validarFormulario);
	input.addEventListener('blur', validarFormulario);
});

formulario.addEventListener('submit', (e) => {

	const terminos = document.getElementById('terminos');
	if (campos.nombre && campos.apellido && campos.edad && campos.sexo && campos.identificacion && campos.nacionalidad && campos.ciudad && campos.numero_telefonico && campos.direccion_residencia && campos.ocupacion && campos.correo_electronico && campos.contrasena && terminos.checked) {

		swal("Buen trabajo", "Cuenta registrada!", "success");

	} else {

		e.preventDefault();
		swal("Error!", "Por favor rellena el formulario correctamente, todos los campos son requeridos!", "error");
	}
});