from db.database import database
from models.models import Noticias
import requests
from bs4 import BeautifulSoup

def scrap():
    url = "https://www.billboard.com/c/espanol/noticias/"
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
        collection = database.get_collection("noticias")
        try:
            result = collection.insert_many(docs, ordered=False)
            return {"mensaje": "Se insertó correctamente"}
        except Exception as e:
            return {"error": str(e)}
    else:
        return {"message": "No news found to insert."}


def borrar():
    collection = database.get_collection("noticias")
    result = collection.delete_many({})
    return {"mensaje": f"Se eliminaron {result.deleted_count} noticias."}
    