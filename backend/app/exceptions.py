from fastapi import HTTPException, status

class CiclopuertoException(HTTPException):
    """Excepción base personalizada para el proyecto"""
    pass

class InvalidCredentialsException(CiclopuertoException):
    def __init__(self, detail="Credenciales inválidas"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )

class NotFoundException(CiclopuertoException):
    def __init__(self, resource: str, id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} con ID '{id}' no encontrado"
        )

class PermissionDeniedException(CiclopuertoException):
    def __init__(self, detail="No tienes permiso para realizar esta acción"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )

class ValidationException(CiclopuertoException):
    def __init__(self, detail="Error de validación"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )