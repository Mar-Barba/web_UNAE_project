import { useState, useEffect } from 'react';

export default function ClassManager() {
  const [clases, setClases] = useState([]);
  const [busqueda, setBusqueda] = useState('');
  const [nombreMaestro, setNombreMaestro] = useState('Maestr@');

  useEffect(() => {
    const userId = localStorage.getItem('userId') || 1;
    const storedName = localStorage.getItem('userName');
    if (storedName) setNombreMaestro(storedName);

    fetch(`/api/clases?maestroId=${userId}`)
      .then(res => res.ok ? res.json() : { clases: [] })
      .then(data => {
        if (data && data.clases) {
          setClases(data.clases);
        } else if (Array.isArray(data)) {
          setClases(data);
        } else {
          setClases([]);
        }
      })
      .catch(err => console.error("Error cargando clases:", err));
  }, []);

  const agregarClase = async () => {
    const nombreClase = prompt("Ingrese el nombre o código de la nueva clase:");
    if (!nombreClase?.trim()) return;

    const userId = localStorage.getItem('userId');
    try {
      const response = await fetch('/api/clases', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nombre: nombreClase.toUpperCase(), maestro_id: userId })
      });

      if (response.ok) {
        const nuevaClase = await response.json();
        setClases([...clases, nuevaClase]);
      }
    } catch (error) {
      console.error("Error al crear clase:", error);
    }
  };

  const irADetalle = (clase) => {
    localStorage.setItem('claseActualNombre', clase.nombre);
    localStorage.setItem('claseActualId', clase.id);
    window.location.href = '/detalle-clase';
  };

  const clasesFiltradas = clases.filter(c => 
    c && c.nombre && c.nombre.toLowerCase().includes(busqueda.toLowerCase())
  );

  return (
    <>
      <div className="title-group">
        <h1>DASHBOARD</h1>
        <p>Bienvenid@, {nombreMaestro}</p>
      </div>

      <div className="search-container">
        <input 
          type="text" 
          className="search-input" 
          placeholder="🔍 Ingrese id de la clase que busca"
          value={busqueda}
          onChange={(e) => setBusqueda(e.target.value)}
        />
      </div>

      <section className="class-carousel">
        <button className="class-btn add-btn" onClick={agregarClase}>
          <span className="plus-icon">+</span>
          <p>AGREGAR CLASE</p>
        </button>

        {clasesFiltradas.map((clase) => (
          <button 
            key={clase.id} 
            className="class-btn" 
            onClick={() => irADetalle(clase)}
          >
            <p>{clase.nombre}</p>
          </button>
        ))}
      </section>
    </>
  );
}
