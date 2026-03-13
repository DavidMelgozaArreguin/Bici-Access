import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styless/Login.css";

const API_URL = "http://localhost:8000";

function Login() {

  const [codigo, setCodigo] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const navigate = useNavigate();

  const iniciarSesion = async (e) => {

    e.preventDefault();

    setLoading(true);
    setError("");

    if (!codigo || !password) {

      setError("Código y contraseña son obligatorios");
      setLoading(false);
      return;

    }

    const email = `${codigo}@alumnos.udg.mx`;

    try {

      const response = await fetch(`${API_URL}/auth/login`, {

        method: "POST",

        headers: {
          "Content-Type": "application/json"
        },

        body: JSON.stringify({
          email,//si recibe correo o email si conecta token pero no pasa de login a perfil
          password//si es por username o nombre en vez de codigo si pasa a perfil
        })

      });

      const data = await response.json();
      console.log("RESPUESTA BACKEND alv:", data);
          if (response.ok) {
            navigate("/perfil");
            const token = localStorage.getItem("token");     
          } else {
            setError(data.detail || "Credenciales incorrectas");
          }

    } catch (err) {

      setError("Error de conexión con el servidor");

    } finally {

      setLoading(false);

    }

  };

  return (

    <div className="login-container">

      <div className="login-box">

        <h1>BICI-ACCESS</h1>

        {error && (
          <div style={{ color: "red", marginBottom: "10px" }}>
            {error}
          </div>
        )}

        <form onSubmit={iniciarSesion}>
          <input
            type="text"
            placeholder="Código"
            value={codigo}
            onChange={(e) => setCodigo(e.target.value)}
            required
          />

          <input
            type="password"
            placeholder="Contraseña"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          <button type="submit" disabled={loading}>

            {loading ? "Entrando..." : "Iniciar sesión"}

          </button>

        </form>

        <p>

          ¿No tienes cuenta? <a href="/registro">Regístrate</a>

        </p>

      </div>

    </div>

  );

}

export default Login;