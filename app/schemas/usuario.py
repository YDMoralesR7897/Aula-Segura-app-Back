from pydantic import BaseModel

class UsuarioBase(BaseModel):
    username: str
    id_persona: int
    id_perfil: int

class UsuarioCreate(UsuarioBase):
    password: str


class UsuarioUpdate(BaseModel):
    username: str
    password: str
    id_perfil: int

class UsuarioResponse(UsuarioBase):
    id_usuario: int
    estado: bool

    class Config:
        from_attributes = True
