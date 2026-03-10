import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { usuarios } from "../data/usuarios";

function Registro() {

  const [nombre, setNombre] = useState("");
  const [codigo, setCodigo] = useState("");
  const [carrera, setCarrera] = useState("");
  const [vehiculo, setVehiculo] = useState("");
  const [password, setPassword] = useState("");

  const navigate = useNavigate();

  const registrar = (e) => {
    e.preventDefault();

    const existe = usuarios.find((u) => u.codigo === codigo);

    if (existe) {
      alert("El alumno ya está registrado");
      return;
    }

    const nuevoUsuario = {
      nombre,
      codigo,
      carrera,
      vehiculo,
      password
    };

    usuarios.push(nuevoUsuario);

    alert("Registro exitoso");

    navigate("/");
  };

  return (

    <div className="login-container">

      <div className="login-box">

        <h1>Registro de Alumno</h1>

        <form onSubmit={registrar}>

          <input
            type="text"
            placeholder="Nombre"
            value={nombre}
            onChange={(e)=>setNombre(e.target.value)}
          />

          <input
            type="text"
            placeholder="Código"
            value={codigo}
            onChange={(e)=>setCodigo(e.target.value)}
          />

          <input
            type="text"
            placeholder="Carrera"
            value={carrera}
            onChange={(e)=>setCarrera(e.target.value)}
          />

          <input
            type="text"
            placeholder="Vehículo"
            value={vehiculo}
            onChange={(e)=>setVehiculo(e.target.value)}
          />

          <input
            type="password"
            placeholder="Contraseña"
            value={password}
            onChange={(e)=>setPassword(e.target.value)}
          />

          <button type="submit">
            REGISTRARSE
          </button>

          <button type="button" onClick={()=>navigate("/registro")}>
            Registrarse
          </button>

        </form>

      </div>

    </div>

  );
}

export default Registro;