from pydantic import BaseModel, ConfigDict

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

    # Permite crear este esquema desde objetos (por ejemplo, instancias ORM),
    # leyendo atributos como obj.id_usuario en lugar de requerir un dict.
    model_config = ConfigDict(from_attributes=True)
