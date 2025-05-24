from pydantic import BaseModel
from typing import List, Optional

class Noticias(BaseModel):
    imagen: str
    nombre: str
    autor: str
    link: str