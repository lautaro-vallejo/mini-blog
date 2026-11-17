const API = "/api/v1";

// Leo el slug de la dirección. Ejemplo: post.html?slug=previa-del-clasico
const parametros = new URLSearchParams(window.location.search);
const slug = parametros.get("slug");

async function cargarPost() {
  const respuesta = await fetch(API + "/posts/post/" + slug);

  if (!respuesta.ok) {
    document.getElementById("titulo").textContent = "Post no encontrado";
    return;
  }

  const post = await respuesta.json();

  document.title = post.title; // cambia el título de la pestaña
  document.getElementById("titulo").textContent = post.title;
  document.getElementById("contenido").textContent = post.content;

  // Categoría, autor y fecha
  const categoria = post.category ? post.category.name : "Sin categoría";
  const autor = post.user ? post.user.username : "anónimo";
  const fecha = new Date(post.created_at).toLocaleDateString("es-AR");
  document.getElementById("datos").textContent =
    categoria + " · por " + autor + " · " + fecha;

  // La imagen solo se muestra si el post tiene una
  if (post.image_url) {
    const imagen = document.getElementById("imagen");
    imagen.src = post.image_url;
    imagen.style.display = "block";
  }

  // Un cartelito amarillo por cada tag
  const contenedorTags = document.getElementById("tags");
  for (const tag of post.tags) {
    const span = document.createElement("span");
    span.className = "tag";
    span.textContent = "#" + tag.name;
    contenedorTags.appendChild(span);
  }
}

cargarPost();
