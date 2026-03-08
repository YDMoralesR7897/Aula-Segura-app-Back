from pydantic import BaseModel

class RecuperarPasswordRequest(BaseModel):
    correo: str
    
class LoginRequest(BaseModel):
    username: str
    password: str
