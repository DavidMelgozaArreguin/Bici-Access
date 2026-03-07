# API del Ciclopuerto 2V - Backend

## 🚀 Instalación y Ejecución

1. **Clonar el repositorio**
```bash
git clone <url-del-repositorio>
cd backend

python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt

cp .env.example .env
# Editar .env con tus configuraciones

uvicorn app.main:app --reload

#La API estará disponible en: http://localhost:8000