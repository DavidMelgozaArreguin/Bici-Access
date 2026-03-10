import { useLocation } from "react-router-dom";
import "../styless/Perfil.css";
function Perfil() {

  const location = useLocation();
  const usuario = location.state;

  if (!usuario) {
    return <h2>No hay usuario</h2>;
  }

  return (
    <div>
      <div className="navbar"> 
        BICI-ACCESS
      </div>
      <div className="perfil-container">
        <div className="perfil-card">
          <h1>Perfil del Alumno</h1>
          <p className="perfil-info"><b>Nombre:</b> {usuario.nombre}</p>
          <p className="perfil-info"><b>Código:</b> {usuario.codigo}</p>
          <p className="perfil-info"><b>Carrera:</b> {usuario.carrera}</p>
          <p className="perfil-info"><b>Vehículo:</b> {usuario.vehiculo}</p>
        </div>
      </div>
    </div>
  );
}

export default Perfil;