from fastapi import APIRouter, HTTPException, status
from typing import List
from models.models import Noticias
from services.services import scrap, borrar
from db.database import database
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

@router.post("/noticias",status_code=status.HTTP_201_CREATED)
async def create_noticias():
    nuevos = scrap()
    if nuevos is None:
        raise HTTPException(status_code=500, detail="Error al insertar en la base de datos")
    return {"inserted": nuevos}

@router.get("/noticias",response_model=List[Noticias])
async def read_noticias():
    col = database.get_collection(os.getenv("COLLECTION"))
    docs = list(col.find({}, {"_id": False}))
    return docs

@router.delete("/noticias")
def eliminar_todas_las_noticias():
    return borrar()