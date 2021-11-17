function guardar(){
var nombre = document.getElementById("Nombre").value;
var descripcion = document.getElementById("Descripcion").value;
var objetivo = document.getElementById("Objetivo").value;
var como = document.getElementById("Como").value;
var Departamento = document.getElementById("Departamento").value;
var Ciudad = document.getElementById("Ciudad").value;
var Duracion = document.getElementById("Duracion").value;
var Codigo_Postal = document.getElementById("Codigo_Postal").value;
var Donacion = document.getElementById("Donacion").value;
var PerfilColaboradores = document.getElementById("PerfilColaboradores").value;
var Recursos = document.getElementById("Recursos").value;
var Video = document.getElementById("Video").value;


let datos ={
    method: "POST",
    headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        nombre: nombre,
        descripcion: descripcion,
        objetivo: objetivo,
        como: como,
        Departamento: Departamento,
        Ciudad: Ciudad,
        Duracion: Duracion,
        Codigo_Postal: Codigo_Postal,
        Donacion: Donacion,
        PerfilColaboradores: PerfilColaboradores,
        Recursos: Recursos,
        Video: Video
      })
}
fetcher("http://localhost:3000/Proyectos", datos)
    .then(function(response){
        return response.json();
     });

}