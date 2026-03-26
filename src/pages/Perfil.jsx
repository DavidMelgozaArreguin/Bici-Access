import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { QRCodeCanvas } from "qrcode.react";
import "../styless/Perfil.css";
//para excel 
import * as XLSX from "xlsx";
import { saveAs } from "file-saver";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function Perfil() {
  const [usuario, setUsuario] = useState(null);
  const [bicicletas, setBicicletas] = useState([]);
  const [registros, setRegistros] = useState([]);
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

        // Obtener historial de registros
        const registrosRes = await fetch(`${API_URL}/registros/mi-historial`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        if (registrosRes.ok) {
          const registrosData = await registrosRes.json();
         setRegistros(registrosData);
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
    if (bicicletas.length === 0) {
      alert("No hay bicicletas para exportar");
      return;
    }

    const cambiarEstado = async (biciId, tipo) => {
  const token = localStorage.getItem("access_token");
  if (!token) return;

  const endpoint = tipo === "entrada" ? "entrada" : "salida";
  try {
    const res = await fetch(`${API_URL}/registros/${endpoint}?bici_id=${biciId}`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` }
    });
    if (res.ok) {
      alert(`${tipo === "entrada" ? "Entrada" : "Salida"} registrada correctamente`);
      // Recargar historial
      const registrosRes = await fetch(`${API_URL}/registros/mi-historial`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (registrosRes.ok) {
        const registrosData = await registrosRes.json();
        setRegistros(registrosData);
      }
    } else {
      const error = await res.json();
      alert(`Error: ${error.detail || "No se pudo registrar"}`);
    }
  } catch (err) {
    console.error(err);
    alert("Error de conexión");
  }
};


    // Formatear datos
    const data = bicicletas.map((bici) => ({
      Marca: bici.marca,
      Modelo: bici.modelo,
      Color: bici.color,
      Serial: bici.serial,
      "Fecha Registro": formatearFecha(
        bici.fecha_registro || bici.created_at
      ),
    }));

    // Crear hoja
    const worksheet = XLSX.utils.json_to_sheet(data);

    // Crear libro
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, "Bicicletas");

    // Generar archivo
    const excelBuffer = XLSX.write(workbook, {
      bookType: "xlsx",
      type: "array",
    });

    const file = new Blob([excelBuffer], {
      type: "application/octet-stream",
    });

    saveAs(file, "mis_bicicletas.xlsx");
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
                {bicicletas.map((bici) => {
  const activo = registros.some(reg => reg.bicicleta_id === (bici.id || bici._id) && reg.activo === true);
  return (
    <tr key={bici.id || bici._id}>
      <td>{bici.marca}</td>
      <td>{bici.modelo}</td>
      <td>{bici.color}</td>
      <td>{bici.serial}</td>
      <td>{formatearFecha(bici.fecha_registro || bici.created_at)}</td>
      <td>
        {activo ? (
          <button onClick={() => cambiarEstado(bici.id || bici._id, "salida")}>
            Registrar salida
          </button>
        ) : (
          <button onClick={() => cambiarEstado(bici.id || bici._id, "entrada")}>
            Registrar entrada
          </button>
        )}
      </td>
    </tr>
  );
})}
              </tbody>
            </table>
          )}

          <button className="export-excel" onClick={handleExport}>
            Exportar mis bicicletas a Excel
          </button>

          <hr />

          <h2>Historial de accesos</h2>
          {registros.length === 0 ? (
            <p>No hay registros de entrada/salida.</p>
          ) : (
            <>
              <p><b>Último ingreso:</b> {formatearFecha(registros[0]?.fecha_entrada)}</p>
                {registros[0]?.fecha_salida && <p><b>Última salida:</b> {formatearFecha(registros[0].fecha_salida)}</p>}
              <details>
                <summary>Ver historial completo ({registros.length})</summary>
                     <ul>
                {registros.map((reg, idx) => (
                    <li key={reg.id || idx}>
                        Entrada: {formatearFecha(reg.fecha_entrada)}
                        {reg.fecha_salida ? ` | Salida: ${formatearFecha(reg.fecha_salida)}` : " (Dentro del ciclopuerto)"}
                    </li>
                ))}
            </ul>
        </details>
    </>
)}

        </div>
      </div>
    </div>
  );
}

export default Perfil;