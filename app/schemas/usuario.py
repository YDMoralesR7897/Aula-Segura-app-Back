from pydantic import BaseModel

class UsuarioBase(BaseModel):
    username: str
    id_persona: int
    id_perfil: int

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioResponse(UsuarioBase):
    id_usuario: int
    estado: bool

    class Config:
        from_attributes = True