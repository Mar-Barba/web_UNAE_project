import React, { useState, useEffect } from "react";
import createPlotlyComponent from "react-plotly.js/factory";
import Plotly from "plotly.js-basic-dist-min";

const Plot = createPlotlyComponent(Plotly);

export default function ComparativaPromediosClases() {
  const [dataBarras, setDataBarras] = useState([]);
  const [dataGraficas, setDataGraficas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const coloresPastel = [
    "#B8E2C8",
    "#D9C8EA",
    "#A8D0BC",
    "#C4B2D8",
    "#94C9A9",
    "#B6A5C9"
  ];

  useEffect(() => {
    const maestroId = localStorage.getItem("userId");
    if (!maestroId) {
        setError("La sesión no es válida. Por favor, inicia sesión de nuevo.");
        setLoading(false);
        return;
    }

    setLoading(true);

    fetch(`/api/clases?maestroId=${maestroId}`)
      .then((res) => res.json())
      .then((data) => {
        const clases = data?.clases || [];

        if (clases.length === 0) {
          setLoading(false);
          return [];
        }

        return Promise.all(
          clases.map((clase, index) =>
            fetch(`/api/metrics/clase/${clase.id}`)
              .then((res) => res.json())
              .then((metricRes) => {
                const tiempos = metricRes?.data?.tiempos || [];
                const idsAlumnos = metricRes?.data?.ids || [];
                const promedio = tiempos.length > 0
                  ? tiempos.reduce((a, b) => a + b, 0) / tiempos.length
                  : 0;

                return {
                  nombre: clase.nombre,
                  promedio: promedio,
                  totalAlumnos: idsAlumnos.length,
                  color: coloresPastel[index % coloresPastel.length]
                };
              })
          )
        );
      })
      .then((resultados) => {
        if (!resultados || resultados.length === 0) {
          setLoading(false);
          return;
        }

        resultados.sort((a, b) => b.promedio - a.promedio);

        setDataBarras([{
          x: resultados.map(r => r.nombre),
          y: resultados.map(r => r.promedio),
          type: 'bar',
          marker: { color: resultados.map(r => r.color), line: { width: 1, color: '#4b013e' } },
          text: resultados.map(r => r.promedio > 0 ? `${r.promedio.toFixed(1)}s` : "0s"),
          textposition: 'auto',
          textfont: { color: '#4b013e' }
        }]);

        setDataGraficas([{
          labels: resultados.map(r => r.nombre),
          values: resultados.map(r => r.totalAlumnos),
          type: 'pie',
          hole: 0.4,
          marker: { colors: resultados.map(r => r.color) },
          textinfo: 'percent',
          hoverinfo: 'label+value',
          textfont: { color: '#4b013e' }
        }]);

        setLoading(false);
      })
      .catch((err) => {
        console.error("Error en el Dashboard:", err);
        setError("Error al conectar con el servidor.");
        setLoading(false);
      });
  }, []);

  const commonLayout = {
    paper_bgcolor: "#f1ede4",
    plot_bgcolor: "#f1ede4",
    font: { color: "#4b013e" },
    margin: { t: 50, b: 50, l: 50, r: 50 }
  };

  if (loading) return <div style={estilos.centro}>Cargando estadísticas...</div>;
  if (error) return <div style={estilos.error}>{error}</div>;

  return (
    <div style={estilos.container}>
      <h2 style={estilos.titulo}>Panel para la toma de decisiones - Memoretos</h2>

      <div style={estilos.grid}>
        <div style={estilos.card}>
          <Plot
            data={dataBarras}
            layout={{ ...commonLayout, title: 'Tiempo Promedio por Clase', xaxis: { zeroline: false }, yaxis: { title: "Segundos" } }}
            config={{ responsive: true, displayModeBar: false }}
            style={estilos.plot}
            useResizeHandler
          />
          <p style={{ color: '#666', fontSize: '14px', marginTop: '15px', textAlign: 'center' }}>
            Esta comparativa muestra el tiempo promedio que cada grupo tarda en completar sus sesiones.
            Es útil para identificar qué grupos dominan los conceptos con mayor rapidez y cuáles requieren un refuerzo en estos.
          </p>
        </div>

        <div style={estilos.card}>
          <Plot
            data={dataGraficas}
            layout={{ ...commonLayout, title: 'Distribución de Alumnos', showlegend: true }}
            config={{ responsive: true, displayModeBar: false }}
            style={estilos.plot}
            useResizeHandler
          />
          <p style={{ color: '#666', fontSize: '14px', marginTop: '15px', textAlign: 'center' }}>
            Muestra la cantidad de estudiantes activos por clase. Permite visualizar el alcance de Videojuego en las clases registradas.
          </p>
        </div>
      </div>
    </div>
  );
}

const estilos = {
  container: {
    backgroundColor: "#f1ede4",
    height: "100vh",
    display: "flex",
    flexDirection: "column",
    padding: "20px",
    boxSizing: "border-box",
    overflow: "hidden"
  },
  titulo: {
    textAlign: "center",
    color: "#4b013e",
    marginBottom: "20px",
    fontSize: "28px",
    flexShrink: 0,
    fontWeight: "bold"
  },
  grid: {
    display: "flex",
    flexWrap: "wrap",
    gap: "25px",
    justifyContent: "center",
    overflowY: "auto",
    padding: "10px",
    flexGrow: 1,
    scrollbarWidth: "thin",
    scrollbarColor: "#4b013e #f1ede4"
  },
  card: {
    backgroundColor: "#f1ede4",
    borderRadius: "20px",
    boxShadow: "0 6px 15px rgba(0,0,0,0.08)",
    padding: "25px",
    flex: "1 1 450px",
    maxWidth: "650px",
    height: "fit-content",
    border: "1px solid rgba(75, 1, 62, 0.1)"
  },
  plot: {
    width: "100%",
    height: "350px"
  },
  centro: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    height: "100vh",
    color: "#4b013e",
    backgroundColor: "#f1ede4",
    fontSize: "20px"
  },
  error: {
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    alignItems: "center",
    height: "100vh",
    color: "#ff4136",
    backgroundColor: "#f1ede4",
    textAlign: "center",
    padding: "20px"
  }
};
