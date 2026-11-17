const API = "/api/v1";

// Muestro si ya hay alguien logueado
function mostrarEstado() {
  const token = localStorage.getItem("token");
  if (token) {
    document.getElementById("estado").textContent = "Ya iniciaste sesión.";
  } else {
    document.getElementById("estado").textContent = "No iniciaste sesión.";
  }
}

document.getElementById("formulario").onsubmit = async (evento) => {
  evento.preventDefault(); // evita que la página se recargue

  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  // Mando email y contraseña en JSON
  const respuesta = await fetch(API + "/auth/login/json", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email: email, password: password }),
  });

  if (!respuesta.ok) {
    document.getElementById("error").textContent = "Email o contraseña incorrectos";
    return;
  }

  // Guardo el token en el navegador para usarlo después
  const datos = await respuesta.json();
  localStorage.setItem("token", datos.access_token);

  window.location.href = "nuevo.html";
};

document.getElementById("salir").onclick = () => {
  localStorage.removeItem("token");
  mostrarEstado();
};

mostrarEstado();
