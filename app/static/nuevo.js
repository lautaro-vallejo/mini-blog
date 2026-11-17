// Si no inició sesión, lo mando al login
if (!obtenerToken()) {
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

  const error = document.getElementById("error");
  const boton = document.getElementById("publicar");
  error.textContent = "";
  boton.disabled = true; // para que no lo aprieten dos veces
  boton.textContent = "Publicando...";

  // FormData porque mandamos texto y un archivo juntos (multipart, Módulo 8)
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
    headers: { Authorization: "Bearer " + obtenerToken() }, // token del login
    body: datos,
  });

  boton.disabled = false;
  boton.textContent = "Publicar";

  if (respuesta.status === 401) {
    // El token venció (dura 30 minutos): hay que loguearse de nuevo
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

  // Si salió bien, abro el post recién creado
  const post = await respuesta.json();
  window.location.href = "post.html?slug=" + post.slug;
};

cargarCategorias();
