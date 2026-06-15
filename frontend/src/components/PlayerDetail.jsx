import { useState, useEffect } from 'react';

export default function PlayerDetail() {
  const [busqueda, setBusqueda] = useState('');
  const [playerData, setPlayerData] = useState(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const studentId = params.get('studentId');
    if (studentId) {
      setBusqueda(studentId);
      const fetchPlayer = async () => {
        try {
          const response = await fetch(`/api/metrics/player/${studentId}`);
          const data = await response.json();
          if (!response.ok || data.status === "fail") {
            throw new Error("Jugador no encontrado");
          }
          setPlayerData(data);
        } catch (err) {
          console.error("Error en búsqueda inicial:", err);
          setError(true);
        }
      };
      fetchPlayer();
    }
  }, []);

  const buscarJugador = async (e) => {
    if (e.key === 'Enter' && busqueda.trim()) {
      try {
        const response = await fetch(`/api/metrics/player/${busqueda}`);
        const data = await response.json();
        
        if (!response.ok || data.status === "fail") {
           throw new Error("Jugador no encontrado");
        }
        
        setPlayerData(data);
      } catch (err) {
        console.error("Error en búsqueda:", err);
        setPlayerData(null);
        setError(true);
      }
    }
  };

  const exportarCSV = () => {
    if (!playerData || !playerData.sesiones) return;
    let csv = "ID SESION,NIVEL,FECHA,TIEMPO,PUNTAJE\n";
    playerData.sesiones.forEach(s => {
      csv += `${s.id_sesion},${s.memo_id},${s.fecha},${s.tiempo},${s.score || 0}\n`;
    });
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `Reporte_${playerData.resumen.nombre}.csv`;
    a.click();
  };

  return (
    <div style={{ backgroundColor: '#f1ede4', minHeight: '100vh', padding: '20px', color: 'white' }}>
      {/* Buscador por nombres */}
      <div className="search-container" style={{ marginBottom: '30px', textAlign: 'center' }}>
        <input 
          type="text" 
          className="search-input" 
          placeholder="🔍 Ingrese ID o Nombre del alumno y presione Enter"
          value={busqueda}
          onChange={(e) => setBusqueda(e.target.value)}
          onKeyDown={buscarJugador}
        />
      </div>

      {error && (
        <p style={{ color: '#ffeb3b', textAlign: 'center', marginBottom: '20px', fontWeight: 'bold' }}>
          No se encontró al jugador: "{busqueda}"
        </p>
      )}

      {/* Resumen del Jugador */}
      <section className="player-summary" style={{ 
        background: 'rgba(255,255,255,0.95)', 
        borderRadius: '15px', 
        padding: '25px', 
        color: '#4b013e',
        marginBottom: '30px',
        boxShadow: '0 8px 20px rgba(0,0,0,0.15)'
      }}>
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: '0.5fr 1.5fr 1fr 1fr 1fr 1fr', 
          textAlign: 'center', 
          fontWeight: 'bold',
          borderBottom: '2px solid #4b013e',
          paddingBottom: '10px',
          fontSize: '13px',
          textTransform: 'uppercase'
        }}>
          <span>ID</span><span>Nombre de Usuario</span><span>Grupo</span>
          <span>Sesiones</span><span>Tiempo Total</span><span>Nivel</span>
        </div>
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: '0.5fr 1.5fr 1fr 1fr 1fr 1fr', 
          textAlign: 'center', 
          paddingTop: '20px',
          fontSize: '18px'
        }}>
          <span>{playerData?.resumen?.id || '-'}</span>
          <span style={{ fontWeight: 'bold' }}>{playerData?.resumen?.nombre || '-'}</span>
          <span>{playerData?.resumen?.grupo || '-'}</span>
          <span>{playerData?.resumen?.total_sesiones || '-'}</span>
          <span>{playerData?.resumen?.tiempo_total || '-'}</span>
          <span>{playerData?.resumen?.retos_completados || '-'}</span>
        </div>
      </section>

      <div style={{ display: 'flex', gap: '25px', flexWrap: 'wrap' }}>
        {/* Tabla de Sesiones */}
        <section style={{ 
          background: 'white', 
          borderRadius: '15px', 
          padding: '25px', 
          color: '#333',
          flex: '1 1 650px',
          boxShadow: '0 8px 20px rgba(0,0,0,0.15)'
        }}>
          <h3 style={{ color: '#4b013e', marginTop: 0, paddingLeft: '10px' }}>
            Historial de Actividad
          </h3>
          <div style={{ maxHeight: '450px', overflowY: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
              <thead style={{ position: 'sticky', top: 0, background: 'white', zIndex: 1 }}>
                <tr style={{ borderBottom: '2px solid #f1ede4' }}>
                  <th style={{ padding: '12px' }}>ID SESIÓN</th>
                  <th>NIVEL</th>
                  <th>FECHA</th>
                  <th>TIEMPO</th>
                </tr>
              </thead>
              <tbody>
                {playerData?.sesiones?.map((s, i) => (
                  <tr key={i} style={{ borderBottom: '1px solid #eee' }}>
                    <td style={{ padding: '12px', color: '#666' }}>#{s.id_sesion}</td>
                    <td style={{ fontWeight: '500' }}>{s.memo_id}</td>
                    <td>{s.fecha}</td>
                    <td><span style={{ backgroundColor: '#f1ede4', padding: '4px 8px', borderRadius: '5px' }}>{s.tiempo}</span></td>
                  </tr>
                )) || (
                  <tr>
                    <td colSpan="4" style={{ padding: '60px', textAlign: 'center', color: '#999', fontStyle: 'italic' }}>
                      Ingrese un nombre de usuario para consultar los detalles.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </section>

        <aside style={{ 
          background: 'rgba(255,255,255,0.1)', 
          padding: '25px', 
          borderRadius: '15px',
          minWidth: '220px',
          display: 'flex',
          flexDirection: 'column',
          gap: '20px',
          height: 'fit-content'
        }}>
          <p style={{ margin: 0, fontWeight: 'bold', fontSize: '14px', color: '#333' }}>Exportar datos:</p>
          <button 
            onClick={() => window.print()} 
            style={{ 
              padding: '14px', borderRadius: '10px', border: 'none', cursor: 'pointer', 
              backgroundColor: '#B8E2C8', color: '#4b013e', fontWeight: 'bold',
              transition: 'transform 0.2s'
            }}
            onMouseOver={(e) => e.target.style.transform = 'scale(1.05)'}
            onMouseOut={(e) => e.target.style.transform = 'scale(1)'}
          >
            PDF
          </button>
          <button 
            onClick={exportarCSV} 
            disabled={!playerData}
            style={{ 
                padding: '14px', borderRadius: '10px', border: 'none', 
                cursor: playerData ? 'pointer' : 'not-allowed', 
                backgroundColor: '#D9C8EA', color: '#4b013e', fontWeight: 'bold',
                opacity: playerData ? 1 : 0.5
            }}
          >
            CSV
          </button>
        </aside>
      </div>
    </div>
  );
}