const API = "/api/v1";

const token = localStorage.getItem("token");

// Si no hay token, lo mando a loguearse
if (!token) {
  window.location.href = "login.html";
}

// Lleno el select con las categorías de la API
async function cargarCategorias() {
  const respuesta = await fetch(API + "/categories");
  const categorias = await respuesta.json();

  const select = document.getElementById("categoria");
  for (const categoria of categorias) {
    const opcion = document.createElement("option");
    opcion.value = categoria.id;
    opcion.textContent = categoria.name;
    select.appendChild(opcion);
  }
}

document.getElementById("formulario").onsubmit = async (evento) => {
  evento.preventDefault();

  // FormData porque mandamos texto + archivo (multipart, como en el Módulo 8)
  const datos = new FormData();
  datos.append("title", document.getElementById("titulo").value);
  datos.append("content", document.getElementById("contenido").value);
  datos.append("category_id", document.getElementById("categoria").value);
  datos.append("tags", document.getElementById("tags").value);

  const archivo = document.getElementById("imagen").files[0];
  if (archivo) {
    datos.append("image", archivo);
  }

  const respuesta = await fetch(API + "/posts", {
    method: "POST",
    headers: { Authorization: "Bearer " + token }, // el token del login
    body: datos,
  });

  const error = document.getElementById("error");

  if (respuesta.status === 401) {
    // El token venció (dura 30 minutos)
    localStorage.removeItem("token");
    window.location.href = "login.html";
    return;
  }

  if (respuesta.status === 403) {
    error.textContent = "Tu usuario no tiene permiso. Hace falta rol editor o admin.";
    return;
  }

  if (!respuesta.ok) {
    const detalle = await respuesta.json();
    error.textContent = "No se pudo publicar: " + JSON.stringify(detalle.detail);
    return;
  }

  // Si salió bien, abro el post nuevo
  const post = await respuesta.json();
  window.location.href = "post.html?slug=" + post.slug;
};

cargarCategorias();
