import { useState, useEffect } from 'react';

export default function RecentGamesTable() {
  const [partidas, setPartidas] = useState([]);
  const [busqueda, setBusqueda] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const maestroId = localStorage.getItem('userId');
    if (maestroId) {
      fetch(`/api/metrics/recent?maestroId=${maestroId}`)
        .then(res => res.json())
        .then(data => {
          if (data && data.sessions) {
            setPartidas(data.sessions);
          } else if (Array.isArray(data)) {
            setPartidas(data);
          } else {
            setPartidas([]);
          }
          setLoading(false);
        })
        .catch(err => {
          console.error("Error cargando partidas:", err);
          setLoading(false);
        });
    } else {
        setLoading(false);
    }
  }, []);

  const exportarCSV = () => {
    let csv = "ID,NOMBRE,RETO,TIEMPO,FECHA\n";
    partidas.forEach(p => {
      csv += `${p.id_usuario || 'N/A'},${p.nombre || 'N/A'},${p.memo_id || 'N/A'},${p.tiempo || 'N/A'},${p.fecha || 'N/A'}\n`;
    });
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'Reporte_Global_Partidas.csv';
    a.click();
  };

  const partidasFiltradas = partidas.filter(p => 
    Object.values(p).some(val => String(val).toLowerCase().includes(busqueda.toLowerCase()))
  );

  return (
    <>
      <section className="search-section">
        <div className="search-container">
          <input 
            type="text" 
            className="search-input" 
            placeholder="🔍 Ingrese id de usuario, nombre o clase"
            value={busqueda}
            onChange={(e) => setBusqueda(e.target.value)}
          />
        </div>
      </section>

      <section className="table-container card-style">
        <table className="recent-table">
          <thead>
            <tr>
              <th>ID USUARIO</th>
              <th>NOMBRE</th>
              <th>MEMORETO_ID</th>
              <th>TIEMPO</th>
              <th>FECHA</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td colSpan="5" style={{textAlign: 'center'}}>Cargando partidas...</td></tr>
            ) : partidasFiltradas.length > 0 ? (
              partidasFiltradas.map((p, i) => (
                <tr key={i}>
                  <td>{p.id_usuario || 'N/A'}</td>
                  <td>{p.nombre}</td>
                  <td>{p.memo_id}</td>
                  <td>{p.tiempo}</td>
                  <td>{p.fecha}</td>
                </tr>
              ))
            ) : (
              <tr><td colSpan="5" style={{textAlign: 'center'}}>No se encontraron resultados.</td></tr>
            )}
          </tbody>
        </table>
      </section>

      <footer className="export-footer">
        <span className="export-label">Exportar datos:</span>
        <button onClick={() => window.print()} className="btn-export pdf">PDF</button>
        <button onClick={exportarCSV} className="btn-export csv">CSV</button>
      </footer>
    </>
  );
}