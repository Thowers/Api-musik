from db.database import database
from models.models import Noticias
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from bson import ObjectId

load_dotenv()

MONGO = os.getenv('MONGO')
COLLECTION = os.getenv('COLLECTION')

def scrap(pagina=1):
    if pagina == 1:
        url = "https://www.billboard.com/c/espanol/noticias/"
    else:
        url = f"https://www.billboard.com/c/espanol/noticias/page/{pagina}/"
    headers = {'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/58.0.3029.110 Safari/537.3'
        )
    }
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    docs = []
    for elem in soup.find_all("div", class_="a-story-grid"):
        data = {
            "imagen": elem.find("img")["src"],
            "nombre": elem.find("a", class_="c-title__link lrv-a-unstyle-link lrv-u-color-brand-primary:hover").text.strip(),
            "autor": elem.find("span").text.strip(),
            "link": elem.find("a")["href"]
        }
        noticia = Noticias(**data)
        docs.append(noticia.dict())

    if docs:
        collection = database.get_collection(COLLECTION)
        try:
            result = collection.insert_many(docs, ordered=False)
            return {"mensaje": "Se insertó correctamente"}
        except Exception as e:
            return {"error": str(e)}
    else:
        return {"mensaje": "No hay noticias a insertar."}


def borrar(noticia_id: str):
    collection = database.get_collection(COLLECTION)
    try:
        noti_id = ObjectId(noticia_id)
    except:
        return None
    result = collection.delete_one({"_id": noti_id})
    if result.deleted_count == 0:
        return {"mensaje": "Noticia no encontrada"}
    return {"mensaje": "Noticia eliminada"}