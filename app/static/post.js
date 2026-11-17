// Leo el slug de la dirección. Ejemplo: post.html?slug=previa-del-clasico-marplatense
const parametros = new URLSearchParams(window.location.search);
const slug = parametros.get("slug");

async function cargarPost() {
  const respuesta = await fetch(API + "/posts/post/" + slug);

  if (!respuesta.ok) {
    document.getElementById("titulo").textContent = "Post no encontrado";
    return;
  }

  const post = await respuesta.json();

  document.title = post.title + " - MdP Futbolera"; // título de la pestaña
  document.getElementById("titulo").textContent = post.title;
  document.getElementById("categoria").textContent =
    post.category ? post.category.name : "Sin categoría";

  const autor = post.user ? post.user.username : "anónimo";
  document.getElementById("datos").textContent =
    "Por " + autor + " · " + formatearFecha(post.created_at);

  // La imagen solo aparece si el post tiene una
  if (post.image_url) {
    const imagen = document.getElementById("imagen");
    imagen.src = post.image_url;
    imagen.alt = post.title;
    imagen.style.display = "block";
  }

  // Cada salto de línea del contenido se convierte en un párrafo
  const contenido = document.getElementById("contenido");
  const parrafos = post.content.split("\n");
  for (const texto of parrafos) {
    if (texto.trim() !== "") {
      const parrafo = document.createElement("p");
      parrafo.textContent = texto;
      contenido.appendChild(parrafo);
    }
  }

  // Un cartelito por cada tag
  const contenedorTags = document.getElementById("tags");
  for (const tag of post.tags) {
    const span = document.createElement("span");
    span.className = "tag";
    span.textContent = "#" + tag.name;
    contenedorTags.appendChild(span);
  }
}

cargarPost();
