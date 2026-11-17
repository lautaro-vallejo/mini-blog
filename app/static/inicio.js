let paginaActual = 1;
let categoriaElegida = ""; // vacío = todas
let textoBuscado = "";

// Trae las categorías y arma un botón por cada una
async function cargarCategorias() {
  const respuesta = await fetch(API + "/categories");
  const categorias = await respuesta.json();

  const contenedor = document.getElementById("categorias");
  contenedor.appendChild(crearBotonCategoria("Todas", ""));

  for (const categoria of categorias) {
    contenedor.appendChild(crearBotonCategoria(categoria.name, categoria.slug));
  }

  marcarCategoriaActiva();
}

function crearBotonCategoria(nombre, slug) {
  const boton = document.createElement("button");
  boton.textContent = nombre;
  boton.className = "categoria";
  boton.dataset.slug = slug; // guardo el slug en el botón para saber cuál es

  boton.onclick = () => {
    categoriaElegida = slug;
    paginaActual = 1;
    marcarCategoriaActiva();
    cargarPosts();
  };

  return boton;
}

// Pinta de verde el botón de la categoría elegida
function marcarCategoriaActiva() {
  const botones = document.querySelectorAll(".categoria");
  for (const boton of botones) {
    if (boton.dataset.slug === categoriaElegida) {
      boton.classList.add("activa");
    } else {
      boton.classList.remove("activa");
    }
  }
}

// Trae los posts de la página actual y los muestra
async function cargarPosts() {
  let url = API + "/posts?per_page=6&order_by=id&direction=desc&page=" + paginaActual;

  if (categoriaElegida !== "") {
    url = url + "&category=" + categoriaElegida;
  }
  // La API pide al menos 3 letras para buscar
  if (textoBuscado.length >= 3) {
    url = url + "&search=" + encodeURIComponent(textoBuscado);
  }

  const respuesta = await fetch(url);
  const contenedor = document.getElementById("posts");

  // Por ejemplo si buscan con signos raros, la API devuelve error 422
  if (!respuesta.ok) {
    contenedor.innerHTML = '<p class="mensaje">Probá buscar solo con letras y números.</p>';
    return;
  }

  const datos = await respuesta.json();
  contenedor.innerHTML = ""; // borro lo que había antes

  if (datos.items.length === 0) {
    contenedor.innerHTML = '<p class="mensaje">No hay posts para mostrar.</p>';
  }

  for (const post of datos.items) {
    contenedor.appendChild(crearTarjeta(post));
  }

  // Paginación
  document.getElementById("pagina").textContent =
    "Página " + datos.page + " de " + Math.max(datos.total_pages, 1);
  document.getElementById("anterior").disabled = !datos.has_prev;
  document.getElementById("siguiente").disabled = !datos.has_next;
}

// Arma la tarjeta de un post.
// Uso textContent (y no innerHTML) para que nadie pueda meter código en un post.
function crearTarjeta(post) {
  const linkDelPost = "post.html?slug=" + post.slug;

  const tarjeta = document.createElement("article");
  tarjeta.className = "tarjeta";

  // Foto del post, o una pelota si no tiene
  if (post.image_url) {
    const imagen = document.createElement("img");
    imagen.src = post.image_url;
    imagen.alt = post.title;
    tarjeta.appendChild(imagen);
  } else {
    const sinImagen = document.createElement("div");
    sinImagen.className = "sin-imagen";
    sinImagen.textContent = "⚽";
    tarjeta.appendChild(sinImagen);
  }

  const texto = document.createElement("div");
  texto.className = "tarjeta-texto";

  const categoria = document.createElement("span");
  categoria.className = "etiqueta-categoria";
  categoria.textContent = post.category ? post.category.name : "Sin categoría";
  texto.appendChild(categoria);

  const titulo = document.createElement("h2");
  const enlace = document.createElement("a");
  enlace.textContent = post.title;
  enlace.href = linkDelPost;
  titulo.appendChild(enlace);
  texto.appendChild(titulo);

  const datos = document.createElement("p");
  datos.className = "datos";
  const autor = post.user ? post.user.username : "anónimo";
  datos.textContent = "Por " + autor + " · " + formatearFecha(post.created_at);
  texto.appendChild(datos);

  // Solo el principio del contenido
  const resumen = document.createElement("p");
  resumen.textContent = post.content.slice(0, 120) + "...";
  texto.appendChild(resumen);

  const leerMas = document.createElement("a");
  leerMas.className = "leer-mas";
  leerMas.textContent = "Leer más →";
  leerMas.href = linkDelPost;
  texto.appendChild(leerMas);

  tarjeta.appendChild(texto);
  return tarjeta;
}

// Botones de paginación
document.getElementById("anterior").onclick = () => {
  paginaActual = paginaActual - 1;
  cargarPosts();
};

document.getElementById("siguiente").onclick = () => {
  paginaActual = paginaActual + 1;
  cargarPosts();
};

// Busca cuando el usuario escribe
document.getElementById("buscador").oninput = (evento) => {
  textoBuscado = evento.target.value.trim();
  paginaActual = 1;
  cargarPosts();
};

// Al abrir la página
cargarCategorias();
cargarPosts();
