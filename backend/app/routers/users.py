from fastapi import APIRouter, Depends
from app.models import UserOut
from app.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

# Este endpoint devolverá el perfil del usuario actualmente autenticado
@router.get("/me", response_model=UserOut)
async def read_users_me(current_user: UserOut = Depends(get_current_user)):
    return current_user
