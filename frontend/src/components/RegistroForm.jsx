import { useState } from 'react';

export default function RegistroForm() {
  const [rol, setRol] = useState('estudiante');
  const [mensaje, setMensaje] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const datosUsuario = Object.fromEntries(formData);
    
    if (rol !== 'estudiante') datosUsuario.group = null;

    try {
      const response = await fetch("/api/users", {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(datosUsuario)
      });

      const result = await response.json();

      if (response.ok) {
        if (rol === 'professor') {
          // Auto-login para maestros
          const loginRes = await fetch("/api/users/login", {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: datosUsuario.username, password: datosUsuario.password })
          });
          const loginData = await loginRes.json();
          
          if (loginRes.ok && loginData.valido) {
            localStorage.setItem('userId', loginData.userId);
            localStorage.setItem('userRol', loginData.rol);
            localStorage.setItem('userName', datosUsuario.username);
            alert("¡Registro exitoso! Bienvenido, profesor.");
            window.location.href = "/dashboard";
          } else {
            alert("¡Registro exitoso! Por favor, inicia sesión.");
            window.location.href = "/login";
          }
        } else {
          alert("¡Registro exitoso! Los estudiantes deben ingresar desde la aplicación de Unity.");
          window.location.href = "/login";
        }
      } else {
        alert("Error: " + (result.message || "No se pudo registrar"));
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="login-form">
      <div className="input-group">
        <label htmlFor="reg-user">Usuario:</label>
        <input type="text" id="reg-user" name="username" required />
      </div>
      
      <div className="input-group">
        <label htmlFor="reg-mail">Correo:</label>
        <input type="email" id="reg-mail" name="mail" required />
      </div>

      <div className="input-group">
        <label htmlFor="reg-pass">Contraseña:</label>
        <input type="password" id="reg-pass" name="password" required />
      </div>

      <div className="input-group">
        <label htmlFor="reg-rol">Rol:</label>
        <select 
          id="reg-rol" 
          name="rol" 
          value={rol} 
          onChange={(e) => setRol(e.target.value)}
        >
          <option value="estudiante">Estudiante</option>
          <option value="professor">Maestro</option>
        </select>
      </div>

      {rol === 'estudiante' && (
        <div className="input-group" id="group-container">
          <label htmlFor="reg-group">Grupo:</label>
          <input 
            type="text" 
            id="reg-group" 
            name="group" 
            placeholder="Ej: A, B, 2do C..." 
            required 
          />
        </div>
      )}

      <button type="submit" className="btn-entrar">Registrarme</button>
      <a href="/login" className="signup-link">Ya tengo cuenta, iniciar sesión</a>
    </form>
  );
}