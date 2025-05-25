from fastapi import APIRouter, HTTPException, status,Depends
from typing import List
from models.models import Noticias
from services.services import scrap, borrar
from db.database import database
import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordRequestForm
from services.auth import authenticate_user, create_access_token, get_current_user
from datetime import timedelta

load_dotenv()

router = APIRouter()

@router.post("/noticias/{pagina}",status_code=status.HTTP_201_CREATED)
async def crear_noticias(pagina: int):
    nuevos = scrap(pagina)
    if nuevos is None:
        raise HTTPException(status_code=500, detail="Error al insertar en la base de datos")
    return {"inserted": nuevos}

@router.get("/noticias",response_model=List[Noticias])
async def leer_noticias():
    col = database.get_collection(os.getenv("COLLECTION"))
    docs = list(col.find({}, {"_id": False}))
    return docs

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if not authenticate_user(form_data.username, form_data.password):
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")
    access_token = create_access_token(
        data={"sub": form_data.username},
        expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.delete("/noticias")
def eliminar_noticias(current_user: str = Depends(get_current_user)):
    return borrar()