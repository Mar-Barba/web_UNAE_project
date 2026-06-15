import { useState } from 'react';

export default function LoginForm() {
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    const formData = new FormData(e.target);
    const { user, pass } = Object.fromEntries(formData);

    try {
      const respuesta = await fetch("/api/users/login", {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: user, password: pass })
      });

      const resultado = await respuesta.json();

      if (respuesta.ok && resultado.valido === true) {
        if (resultado.rol === 'professor') {
          alert("¡Bienvenido, profesor!");
          
          localStorage.setItem('userId', resultado.userId);
          localStorage.setItem('userRol', resultado.rol);
          localStorage.setItem('userName', user); 

          window.location.href = "/dashboard"; // Ruta de Astro
        } else {
          alert("Acceso denegado: Los estudiantes deben ingresar desde la aplicación de Unity.");
        }
      } else {
        alert("Error: " + (resultado.message || "Credenciales incorrectas"));
      }
    } catch (error) {
      console.error("Error de conexión:", error);
      alert("Error al conectar con el servidor.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="login-form" onSubmit={handleSubmit}>
      <div className="input-group">
        <label htmlFor="user">Usuario:</label>
        <input type="text" id="user" name="user" required />
      </div>
      <div className="input-group">
        <label htmlFor="pass">Contraseña:</label>
        <input type="password" id="pass" name="pass" required />
      </div>
      <button type="submit" className="btn-entrar" disabled={loading}>
        {loading ? 'Cargando...' : 'Entrar'}
      </button>
      <a href="/registro" className="signup-link">¿No tienes una cuenta?</a>
    </form>
  );
}