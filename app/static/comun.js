// Cosas que usan todas las páginas

// Dirección de la API (es el mismo servidor, por eso no pongo el dominio)
const API = "/api/v1";

function obtenerToken() {
  return localStorage.getItem("token");
}

function cerrarSesion() {
  localStorage.removeItem("token");
  window.location.href = "index.html";
}

// Convierte "2026-11-17T17:00:00" en "17/11/2026"
function formatearFecha(texto) {
  return new Date(texto).toLocaleDateString("es-AR");
}

// Arriba a la derecha muestra el usuario logueado o el link de login
async function armarMenu() {
  const zona = document.getElementById("usuario");
  const token = obtenerToken();

  if (!token) {
    zona.innerHTML = '<a href="login.html">Iniciar sesión</a>';
    return;
  }

  // Le pregunto a la API quién es el dueño del token
  const respuesta = await fetch(API + "/auth/me", {
    headers: { Authorization: "Bearer " + token },
  });

  if (!respuesta.ok) {
    // El token venció: lo borro
    localStorage.removeItem("token");
    zona.innerHTML = '<a href="login.html">Iniciar sesión</a>';
    return;
  }

  const usuario = await respuesta.json();
  zona.textContent = "Hola, " + usuario.username + " (" + usuario.role + ")";

  const botonSalir = document.createElement("button");
  botonSalir.textContent = "Salir";
  botonSalir.onclick = cerrarSesion;
  zona.appendChild(botonSalir);
}

armarMenu();
