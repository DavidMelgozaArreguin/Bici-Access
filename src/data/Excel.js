import * as XLSX from "xlsx";
import { saveAs } from "file-saver";

/**
 * Exporta un array de objetos a Excel
 * @param {Array} data - array de vehículos
 * @param {String} nombreArchivo - nombre del archivo
 */
export const exportToExcel = (data, nombreArchivo) => {
  const ws = XLSX.utils.json_to_sheet(data);
  const wb = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb, ws, "Datos");
  const wbout = XLSX.write(wb, { bookType: "xlsx", type: "array" });
  saveAs(new Blob([wbout], { type: "application/octet-stream" }), `${nombreArchivo}.xlsx`);
};