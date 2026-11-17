// Dirección de la API (es la misma página, por eso no pongo el dominio)
const API = "/api/v1";

let paginaActual = 1;
let categoriaElegida = ""; // vacío = todas las categorías

// Trae las categorías y arma un botón por cada una
async function cargarCategorias() {
  const respuesta = await fetch(API + "/categories");
  const categorias = await respuesta.json();

  const contenedor = document.getElementById("categorias");

  // Botón para ver todo
  const botonTodas = document.createElement("button");
  botonTodas.textContent = "Todas";
  botonTodas.onclick = () => elegirCategoria("");
  contenedor.appendChild(botonTodas);

  for (const categoria of categorias) {
    const boton = document.createElement("button");
    boton.textContent = categoria.name;
    boton.onclick = () => elegirCategoria(categoria.slug);
    contenedor.appendChild(boton);
  }
}

function elegirCategoria(slug) {
  categoriaElegida = slug;
  paginaActual = 1;
  cargarPosts();
}

// Trae los posts de la página actual y los muestra
async function cargarPosts() {
  let url = API + "/posts?per_page=5&order_by=id&direction=desc&page=" + paginaActual;
  if (categoriaElegida !== "") {
    url = url + "&category=" + categoriaElegida;
  }

  const respuesta = await fetch(url);
  const datos = await respuesta.json();

  const contenedor = document.getElementById("posts");
  contenedor.innerHTML = ""; // limpio lo que había antes

  if (datos.items.length === 0) {
    contenedor.textContent = "No hay posts todavía.";
  }

  for (const post of datos.items) {
    contenedor.appendChild(crearTarjeta(post));
  }

  // Actualizo la paginación
  document.getElementById("pagina").textContent =
    "Página " + datos.page + " de " + Math.max(datos.total_pages, 1);
  document.getElementById("anterior").disabled = !datos.has_prev;
  document.getElementById("siguiente").disabled = !datos.has_next;
}

// Arma el HTML de un post. Uso textContent para que nadie pueda meter HTML raro.
function crearTarjeta(post) {
  const tarjeta = document.createElement("div");
  tarjeta.className = "post";

  const titulo = document.createElement("h2");
  const enlace = document.createElement("a");
  enlace.textContent = post.title;
  enlace.href = "post.html?slug=" + post.slug;
  titulo.appendChild(enlace);
  tarjeta.appendChild(titulo);

  const datos = document.createElement("p");
  datos.className = "datos";
  const categoria = post.category ? post.category.name : "Sin categoría";
  const autor = post.user ? post.user.username : "anónimo";
  datos.textContent = categoria + " · por " + autor;
  tarjeta.appendChild(datos);

  if (post.image_url) {
    const imagen = document.createElement("img");
    imagen.src = post.image_url;
    tarjeta.appendChild(imagen);
  }

  // Muestro solo el principio del contenido
  const resumen = document.createElement("p");
  resumen.textContent = post.content.slice(0, 150) + "...";
  tarjeta.appendChild(resumen);

  return tarjeta;
}

document.getElementById("anterior").onclick = () => {
  paginaActual = paginaActual - 1;
  cargarPosts();
};

document.getElementById("siguiente").onclick = () => {
  paginaActual = paginaActual + 1;
  cargarPosts();
};

// Cuando abre la página
cargarCategorias();
cargarPosts();
