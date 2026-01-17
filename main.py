#import asyncio
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId # Importante per gestire gli ID di MongoDB
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

# Configurazione CORS (stessa di prima)
#app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permette a qualsiasi sito (anche file locali) di chiamare l'API
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CONNESSIONE A MONGODB ATLAS ---
# Sostituisci <password> e l'indirizzo con i tuoi dati reali
#MONGO_DETAILS = "mongodb+srv://mauriziocozzetto:DuoSStpERzq0IjrA@techblogcluster.3hokggo.mongodb.net/?appName=TechBlogCluster"

MONGO_DETAILS = os.getenv("MONGO_DETAILS")

client = AsyncIOMotorClient(MONGO_DETAILS)
db = client.blog_database        # Nome del database
collection = db.posts_collection # Nome della collezione (tabella)

# Helper per convertire il formato MongoDB in JSON pulito per il frontend
def post_helper(post) -> dict:
    return {
        "id": str(post["_id"]),
        "titolo": post["titolo"],
        "testo": post["testo"],
        "autore": post["autore"],
        "url": post["url"],
        "tags": post.get("tags", []),
        "like": post.get("like", 0),
        "views": post.get("views", 0),
        "commenti": post.get("commenti", [])
    }

@app.get("/api/posts")
async def get_posts():
    posts = []
    # Recupera tutti i documenti dalla collezione
    async for post in collection.find():
        posts.append(post_helper(post))
    return posts

@app.get("/api/posts/{post_id}")
async def get_post(post_id: str):
    try:
        # Cerchiamo per l'ID speciale di MongoDB
        post = await collection.find_one({"_id": ObjectId(post_id)})
        if post:
            return post_helper(post)
        raise HTTPException(status_code=404, detail="Post non trovato")
    except Exception:
        # Se l'ID passato non è un formato valido per MongoDB (es. "123")
        raise HTTPException(status_code=400, detail="ID non valido")