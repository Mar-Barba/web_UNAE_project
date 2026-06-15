import { useState, useEffect } from 'react';
import Plot from 'react-plotly.js';

export default function ClassDetail() {
  const [data, setData] = useState({ historial: [], metricas: null });
  const [busqueda, setBusqueda] = useState('');
  const [infoClase, setInfoClase] = useState({ id: '', nombre: 'Cargando...' });

  useEffect(() => {
    const id = localStorage.getItem('claseActualId');
    const nombre = localStorage.getItem('claseActualNombre');
    setInfoClase({ id, nombre });

    if (id) {
      fetch(`/api/metrics/clase/${id}`)
        .then(res => res.json())
        .then(json => {
          if (json && json.status === 'successful' && json.data) {
            const bData = json.data;
            
            const mapaAlumnos = {};
            const nivelesExistentes = new Set();

            bData.alumnos.forEach((nombre, i) => {
              const nivel = bData.level_ids ? bData.level_ids[i] : (i + 1); 
              nivelesExistentes.add(nivel);

              if (!mapaAlumnos[nombre]) {
                mapaAlumnos[nombre] = { 
                  puntajesPorNivel: {}, 
                  tiempos: [],
                  id: bData.ids[i],
                  ultimoPuntajeTotal: 0 
                };
              }
              mapaAlumnos[nombre].puntajesPorNivel[nivel] = bData.puntajes[i];
              mapaAlumnos[nombre].tiempos.push(bData.tiempos[i]);
            });

            const listaNiveles = Array.from(nivelesExistentes).sort((a, b) => a - b);
            const nombresUnicos = Object.keys(mapaAlumnos).sort();

            const matrizPuntajes = nombresUnicos.map(nombre => {
              return listaNiveles.map(nivel => mapaAlumnos[nombre].puntajesPorNivel[nivel] || null);
            });

            setData({
              historial: nombresUnicos.map(n => ({
                id_usuario: mapaAlumnos[n].id,
                nombre: n,
                tiempo: mapaAlumnos[n].tiempos.reduce((a, b) => a + b, 0),
                puntaje: Object.values(mapaAlumnos[n].puntajesPorNivel).reduce((a, b) => a + b, 0)
              })),
              metricas: {
                nombres: nombresUnicos,
                niveles: listaNiveles.map(n => `Nivel ${n}`),
                matriz: matrizPuntajes, 
                tiemposTotales: nombresUnicos.map(n => 
                  mapaAlumnos[n].tiempos.reduce((a, b) => a + b, 0)
                )
              }
            });
          }
        })
        .catch(err => console.error("Error cargando métricas:", err));
    }
  }, []);

  const exportarCSV = () => {
    let csv = "ID USUARIO,NOMBRE,TIEMPO TOTAL,PUNTAJE TOTAL\n";
    data.historial.forEach(u => {
      csv += `${u.id_usuario},${u.nombre},${u.tiempo},${u.puntaje}\n`;
    });
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `Reporte_${infoClase.nombre}.csv`;
    a.click();
  };

  const historialFiltrado = data.historial.filter(u => 
    (u.nombre || "").toLowerCase().includes(busqueda.toLowerCase())
  );

  return (
    <div style={{ 
      backgroundColor: '#f1ede4', 
      minHeight: '100vh', 
      padding: '100px 40px 60px 40px',
      marginTop: '60px', 
      fontFamily: 'Arial, sans-serif' }}>
      
      <header style={{ 
        display: 'flex', 
        alignItems: 'center', 
        gap: '20px', 
        marginTop: '0px',
        marginBottom: '40px' }}>
          
        <a href="/dashboard" style={{ 
          textDecoration: 'none', 
          fontSize: '28px', 
          color: '#4b013e' 
          }}>←</a>
        <h1 style={{ 
        color: '#4b013e', 
        margin: 0, 
        fontSize: '32px', 
        fontWeight: 'bold',
        }}>{infoClase.nombre}</h1>
      </header>

      {/* TABLA DE ALUMNOS */}
      <section style={{ 
        background: 'white', 
        borderRadius: '25px', 
        padding: '30px', 
        boxShadow: '0 10px 30px rgba(0,0,0,0.08)', 
        marginBottom: '40px'}}>
        <div style={{ 
          display: 'flex', 
          justifyContent: 'space-between', 
          alignItems: 'center', 
          marginBottom: '25px' }}>
          <h2 style={{ 
            color: '#4b013e', 
            margin: 0, 
            fontSize: '20px' }}>Lista de Alumnos</h2>
          <input 
            type="text" 
            placeholder="🔍 Buscar alumno..."
            style={{ 
              padding: '12px 15px', 
              borderRadius: '10px', 
              border: '1.5px solid #4b013e', 
              width: '300px' }}
            onChange={(e) => setBusqueda(e.target.value)}
          />
        </div>
        <div style={{ overflowX: 'auto' }}>
            <table style={{ 
              width: '100%', 
              borderCollapse: 'collapse', 
              textAlign: 'left' }}>
                <thead>
                    <tr style={{ 
                      borderBottom: '2px solid #f1ede4' }}>
                        <th style={{ 
                          padding: '15px', 
                          color: 'black' }}>ID USUARIO</th>
                        <th style={{ 
                          color: 'black' }}>NOMBRE DEL ALUMNO</th>
                        <th style={{ 
                          color: 'black' }}>TIEMPO TOTAL</th>
                        <th style={{ 
                          color: 'black' }}>PUNTAJE</th>
                    </tr>
                </thead>
                <tbody>
                    {historialFiltrado.map((u, i) => (
                        <tr key={i} style={{ 
                          borderBottom: '1px solid #eee' }}>
                            <td style={{ 
                              padding: '15px', 
                              color: 'black' }}>{u.id_usuario}</td>
                            <td style={{ color: 'black' }}>
                              <a href={`/resume-player?studentId=${u.id_usuario}`} style={{ color: '#4b013e', textDecoration: 'underline', cursor: 'pointer', fontWeight: 'bold' }}>
                                {u.nombre}
                              </a>
                            </td>
                            <td style={{ 
                              color: 'black' }}>{u.tiempo}s</td>
                            <td style={{ 
                              color: 'black' }}>{u.puntaje}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
        <div style={{ 
          display: 'flex', 
          gap: '10px', 
          marginTop: '25px' }}>
            <button onClick={() => window.print()} 
            style={{ 
              padding: '10px 20px', 
              backgroundColor: '#4b013e', 
              color: 'white', 
              border: 'none', 
              borderRadius: '8px' }}>Exportar PDF</button>
            <button onClick={exportarCSV} 
            style={{ 
              padding: '10px 20px', 
              backgroundColor: '#B8E2C8', 
              color: '#4b013e', 
              border: 'none', 
              borderRadius: '8px' }}>Exportar CSV</button>
        </div>
      </section>

      {/* GRÁFICA DE BARRAS DE TIEMPO */}
      {data.metricas && (
        <section style={{ 
          background: 'white', 
          borderRadius: '25px', 
          padding: '30px', 
          boxShadow: '0 10px 30px rgba(0,0,0,0.08)', 
          marginBottom: '40px' }}>
            <h2 style={{ 
              color: '#4b013e', 
              marginTop: 0, marginBottom: '10px', 
              fontSize: '20px' }}> Tiempo de Sesión De Cada Alumno</h2>
            <p style={{ color: '#666', fontSize: '14px', marginBottom: '20px' }}>
              Esta gráfica permite comparar la rapidez de ejecución entre los estudiantes. 
              Ayuda a identificar quiénes resuelven los retos con mayor agilidad y quiénes podrían necesitar apoyo.
            </p>
            <Plot
                data={[{
                    x: data.metricas.nombres,
                    y: data.metricas.tiemposTotales,
                    type: 'bar',
                    marker: { 
                      color: '#B8E2C8', 
                      line: { color: '#4b013e', width: 1 } }
                }]}
                layout={{ 
                    autosize: true,
                    paper_bgcolor: 'rgba(0,0,0,0)',
                    plot_bgcolor: 'rgba(0,0,0,0)',
                    xaxis: { tickangle: -45 }
                }}
                config={{ responsive: true, displayModeBar: false }}
                style={{ 
                  width: "100%", 
                  height: "350px" }}
            />
        </section>
      )}

      {/* HEATMAP DE PUNTUACIONES */}
      {data.metricas && (
        <section style={{ 
          background: 'white', 
          borderRadius: '25px', 
          padding: '30px', 
          boxShadow: '0 10px 30px rgba(0,0,0,0.08)' }}>
            <h2 style={{ 
              color: '#4b013e', 
              marginTop: 0, 
              marginBottom: '10px', 
              fontSize: '20px' }}> Puntajes De Los Alumos Por Nivel</h2>
            <p style={{ color: '#666', fontSize: '14px', marginBottom: '25px' }}>
              Visualización del desempeño de los estudiantes por nivel. Los colores más oscuros representan los puntajes más altos, 
              permitiendo detectar rápidamente niveles de alta dificultad o estudiantes con un mejor dominio del juego.
            </p>
            <div style={{ 
              width: '100%', 
              height: '500px', 
              overflowY: 'auto' }}>
                <Plot
                    data={[{
                        z: data.metricas.matriz, 
                        x: data.metricas.niveles,
                        y: data.metricas.nombres,
                        type: 'heatmap',
                        colorscale: [[0, '#f1ede4'], [0.5, '#B8E2C8'], [1, '#4b013e']],
                        showscale: true
                    }]}
                    layout={{ 
                        margin: { l: 150, r: 20, t: 30, b: 80 },
                        height: Math.max(500, data.metricas.nombres.length * 45),
                        xaxis: { title: 'Niveles' }
                    }}
                    config={{ responsive: true, displayModeBar: false }}
                    style={{ width: "100%" }}
                />
            </div>
        </section>
      )}
    </div>
  );
}