import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { QRCodeCanvas } from "qrcode.react";
import "../styless/Perfil.css";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function Perfil() {
  const [usuario, setUsuario] = useState(null);
  const [bicicletas, setBicicletas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const navigate = useNavigate();

  const generarQR = () => {
    if (!usuario) return "";
    const datosQR = {
      nombre: usuario.nombre,
      codigo: usuario.codigo,
      email: usuario.email,
      rol: usuario.rol
    };
    return JSON.stringify(datosQR);
  };

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      navigate("/login");
      return;
    }

    const fetchData = async () => {
      try {
        // Obtener datos del usuario
        const userRes = await fetch(`${API_URL}/users/me`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        if (!userRes.ok) {
          if (userRes.status === 401) {
            localStorage.removeItem("access_token");
            navigate("/login");
            return;
          }
          throw new Error("Error al obtener perfil");
        }
        const userData = await userRes.json();
        setUsuario(userData);

        // Obtener bicicletas del usuario
        const biciRes = await fetch(`${API_URL}/bicicletas/mis-bicicletas`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        if (biciRes.ok) {
          const biciData = await biciRes.json();
          setBicicletas(biciData);
        } else if (biciRes.status !== 404) {
          console.warn("Error al obtener bicicletas:", biciRes.status);
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [navigate]);

  const handleExport = () => {
    if (bicicletas.length > 0) {
      alert("Función exportToExcel no implementada");
    } else {
      alert("No hay bicicletas para exportar");
    }
  };

  // Formatear fecha para mostrar (ej. "15/03/2026 14:30")
  const formatearFecha = (fecha) => {
    if (!fecha) return "—";
    try {
      const date = new Date(fecha);
      return date.toLocaleString();
    } catch {
      return fecha; // si es string y no se puede parsear
    }
  };

  if (loading) return <div>Cargando perfil...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!usuario) return <div>No se pudo cargar el perfil</div>;

  return (
    <div>
      <div className="navbar">BICI-ACCESS</div>
      <div className="perfil-container">
        <div className="perfil-card">
          <h1>Perfil del Alumno</h1>
          <p className="perfil-info"><b>Nombre:</b> {usuario.nombre}</p>
          <p className="perfil-info"><b>Código:</b> {usuario.codigo}</p>
          <p className="perfil-info"><b>Rol:</b> {usuario.rol}</p>

          <hr />

          <h2>Mi QR de acceso</h2>
          <div style={{ textAlign: "center", marginTop: "20px" }}>
            <QRCodeCanvas value={generarQR()} size={220} />
            <p>Escanea este código para registrar entrada o salida</p>
          </div>

          <hr />

          <h2>Mis Bicicletas</h2>
          {bicicletas.length === 0 ? (
            <p>No tienes bicicletas registradas.</p>
          ) : (
            <table className="bicicletas-tabla">
              <thead>
                <tr>
                  <th>Marca</th>
                  <th>Modelo</th>
                  <th>Color</th>
                  <th>Serial</th>
                  <th>Fecha Registro</th>
                </tr>
              </thead>
              <tbody>
                {bicicletas.map((bici) => (
                  <tr key={bici.id || bici._id}>
                    <td>{bici.marca}</td>
                    <td>{bici.modelo}</td>
                    <td>{bici.color}</td>
                    <td>{bici.serial}</td>
                    <td>{formatearFecha(bici.fecha_registro || bici.created_at)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}

          <button className="export-excel" onClick={handleExport}>
            Exportar mis bicicletas a Excel
          </button>
        </div>
      </div>
    </div>
  );
}

export default Perfil;