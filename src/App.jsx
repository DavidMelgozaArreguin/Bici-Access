import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Perfil from "./pages/Perfil";
import Registro from "./pages/Registro";

function App() {
  return (

    <BrowserRouter>

      <Routes>

        <Route path="/" element={<Login />} />

        <Route path="/perfil" element={<Perfil />} />

        <Route path="/registro" element={<Registro />} />

      </Routes>

    </BrowserRouter>

  );
}

export default App;