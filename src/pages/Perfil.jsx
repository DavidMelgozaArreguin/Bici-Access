import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styless/Perfil.css";
// import { exportToExcel } from "../data/Excel"; // Puta madre

const API_URL = "http://localhost:8000";

function Perfil() {
  const [usuario, setUsuario] = useState(null);
  const [bicicletas, setBicicletas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      navigate("/login");
      return;
    }

    const fetchPerfil = async () => {
      try {
        // Obtener datos del usuario
        const userRes = await fetch(`${API_URL}/users/me`, {
  headers: {
    'Authorization': `Bearer ${token}`   // <-- IMPORTANTE: "Bearer " con espacio y el token
  }
});

        if (!userRes.ok) {
          if (userRes.status === 401) {
            localStorage.removeItem("token");
            navigate("/login");
          }
          throw new Error("Error al obtener perfil");
        }

        const userData = await userRes.json();
        setUsuario(userData);

        // Obtener bicicletas del usuario
        const biciRes = await fetch(`${API_URL}/bicicletas/mis-bicicletas`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (biciRes.ok) {
          const biciData = await biciRes.json();
          setBicicletas(biciData);
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchPerfil();
  }, [navigate]);

  const handleExport = () => {
    if (bicicletas.length > 0) {
      // exportToExcel(bicicletas, "Mis_Bicicletas");
      alert("Función exportToExcel no implementada. Conéctala desde '../data/Excel'");
    } else {
      alert("No hay bicicletas para exportar");
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
          <p className="perfil-info">
            <b>Nombre:</b> {usuario.nombre}
          </p>
          <p className="perfil-info">
            <b>Código:</b> {usuario.codigo}
          </p>
          <p className="perfil-info">
            <b>Email:</b> {usuario.email}
          </p>
          <p className="perfil-info">
            <b>Rol:</b> {usuario.rol}
          </p>

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
                </tr>
              </thead>
              <tbody>
                {bicicletas.map((bici) => (
                  <tr key={bici.id}>
                    <td>{bici.marca}</td>
                    <td>{bici.modelo}</td>
                    <td>{bici.color}</td>
                    <td>{bici.serial}</td>
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