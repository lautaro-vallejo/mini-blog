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

  // Guardo el token en el navegador para usarlo en las otras páginas
  const datos = await respuesta.json();
  localStorage.setItem("token", datos.access_token);

  window.location.href = "nuevo.html";
};
