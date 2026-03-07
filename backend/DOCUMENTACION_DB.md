# Especificación de Base de Datos - Ciclopuerto 2V

## Colecciones MongoDB

### 1. usuarios son asi jsasadsja
```json
{
  "_id": "ObjectId",
  "codigo": "2213522292",
  "nombre": "David Melgoza",
  "email": "david.melgoza@alumnos.udg.mx",
  "password": "$2b$12$...",  // Hash bcrypt
  "fecha_registro": "2025-08-15T10:30:00Z",
  "activo": true
}

### 2. bicis
{
  "_id": "ObjectId",
  "propietario_id": "ObjectId del usuario",
  "marca": "Trek",
  "modelo": "Marlin 5",
  "color": "Rojo",
  "serial": "TRK123456",
  "fecha_registro": "2025-08-15T10:30:00Z",
  "activa": true
}

### 3. registros
{
  "_id": "ObjectId",
  "bicicleta_id": "ObjectId de la bicicleta",
  "usuario_id": "ObjectId del usuario",
  "usuario_nombre": "David Melgoza",
  "bicicleta_marca": "Trek",
  "bicicleta_modelo": "Marlin 5",
  "tipo": "entrada",  // o "salida"
  "fecha": "2025-08-16T09:15:00Z",
  "fecha_fin": null,  // null para entradas, datetime para salidas
  "activo": true
}