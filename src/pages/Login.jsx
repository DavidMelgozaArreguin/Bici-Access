import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { usuarios } from "../data/usuarios";
import "../styless/Login.css";
function Login() {

  const [codigo, setCodigo] = useState("");
  const [password, setPassword] = useState("");

  const navigate = useNavigate();

  const iniciarSesion = (e) => {
    e.preventDefault();

    const usuario = usuarios.find(
      (u) => u.codigo === codigo && u.password === password
    );

    if (usuario) {
      navigate("/perfil", { state: usuario });
    } else {
      alert("Código o contraseña incorrectos");
    }
  };
  return (

      <div className="login-container">
        <div className="login-box">

          <h1>BICI-ACCESS</h1>

          <form onSubmit={iniciarSesion}>

            <input
              type="text"
              placeholder="Código de alumno"
              maxLength="9"
              value={codigo}
              onChange={(e) => setCodigo(e.target.value)}
            />

              <input
                type="password"
                placeholder="Contraseña"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
          <button type="submit">
            Iniciar sesión
          </button>

        </form>

      </div>

    </div>

);
}

export default Login;