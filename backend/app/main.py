from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.routers import auth, users, bicicletas, registros, admin
import time

limiter = Limiter(key_func=get_remote_address, default_limits=["5/minute"])

app = FastAPI(
    title="Ciclopuerto API",
    description="API para el control de acceso del ciclopuerto 2v",
    version="0.1.0"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Incluir routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(bicicletas.router)
app.include_router(registros.router)
app.include_router(admin.router)

@app.get("/")
@limiter.limit("10/minute")
async def read_root(request: Request):
    return {"message": "¡Bienvenido a la API del Ciclopuerto 2V! 🚴‍♂️"}

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response