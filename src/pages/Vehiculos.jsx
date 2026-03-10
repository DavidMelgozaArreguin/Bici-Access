import "../styless/Vehiculos.css";
import { vehiculos } from "../data/Vehiculos.js";
import { exportToExcel } from "../data/Excel.js";

function Vehiculos() {
  return (
    <div>
      <div className="navbar">BICI-ACCESS</div>

      <div style={{textAlign:"center", margin:"20px"}}>
        <button
          className="btn-export"
          onClick={() => exportToExcel(vehiculos, "Vehiculos_BiciAccess")}
        >
          Exportar Excel
        </button>
      </div>

      <div className="vehiculos-container">
        {vehiculos.map((v) => (
          <div className="vehiculo-card" key={v.id}>
            <h2>{v.tipo}</h2>
            <p><b>Modelo:</b> {v.modelo}</p>
            <p><b>Color:</b> {v.color}</p>
            <p><b>Propietario:</b> {v.propietario}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Vehiculos;