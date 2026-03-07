# Ejemplos de Uso de API para Front-end

## Autenticación

### 1. Login
```javascript
// POST http://localhost:8000/auth/login
fetch('http://localhost:8000/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: "david.melgoza@alumnos.udg.mx",
    password: "secret"
  })
})
.then(response => response.json())
.then(data => {
  console.log("Token recibido:", data.access_token);
  // Guardar token en localStorage
  localStorage.setItem('token', data.access_token);
});

// GET http://localhost:8000/users/me
const token = localStorage.getItem('token');

fetch('http://localhost:8000/users/me', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }
})
.then(response => response.json())
.then(user => {
  console.log("Usuario:", user);
  // Mostrar: "Bienvenido, David Melgoza"
});

// POST http://localhost:8000/bicicletas/
fetch('http://localhost:8000/bicicletas/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    marca: "Trek",
    modelo: "Marlin 5",
    color: "Rojo",
    serial: "TRK123456"
  })
});

// GET http://localhost:8000/bicicletas/mis-bicicletas
fetch('http://localhost:8000/bicicletas/mis-bicicletas', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }
})
.then(response => response.json())
.then(bicicletas => {
  console.log("Mis bicicletas:", bicicletas);
});

// POST http://localhost:8000/registros/entrada
fetch('http://localhost:8000/registros/entrada', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    bicicleta_id: "bici_1"
  })
});

// POST http://localhost:8000/registros/salida
fetch('http://localhost:8000/registros/salida', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    bicicleta_id: "bici_1"
  })
});

// GET http://localhost:8000/registros/activos
fetch('http://localhost:8000/registros/activos', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }
})
.then(response => response.json())
.then(bicicletasDentro => {
  console.log("Bicicletas dentro del ciclopuerto:", bicicletasDentro);
});

## 🌍 Variables de Entorno en React

### Paso 1: Crear archivo .env
En la carpeta **raíz** de tu proyecto React, crea un archivo llamado `.env` (con el punto).

### Paso 2: Copiar este contenido
REACT_APP_API_URL=http://localhost:8000
REACT_APP_SITE_NAME=Ciclopuerto 2V
REACT_APP_TIMEOUT=10000


### Paso 3: Usarlas en tu código
```javascript
// Así accedes a las variables:
const API_URL = process.env.REACT_APP_API_URL;
// Resultado: "http://localhost:8000"

const SITE_NAME = process.env.ACT_APP_SITE_NAME;
// Resultado: "Ciclopuerto 2V"

// Ejemplo de uso:
fetch(`${process.env.REACT_APP_API_URL}/auth/login`, {
  method: 'POST',
  // ...
})