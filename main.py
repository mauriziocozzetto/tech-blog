import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

app = FastAPI()

# Connessione al Database (Usa la variabile che abbiamo impostato su Render)
MONGO_DETAILS = os.getenv("MONGO_DETAILS")
client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.blog_database 
posts_collection = database.get_collection("posts_collection")

# --- ROTTE PER LE PAGINE HTML ---

@app.get("/")
async def read_index():
    return FileResponse('index.html')

@app.get("/detail.html") # Serve per far funzionare il link diretto
async def read_detail():
    return FileResponse('detail.html')

# --- ROTTE API (I DATI) ---

@app.get("/api/posts")
async def get_posts():
    posts = []
    async for post in posts_collection.find():
        post["id"] = str(post["_id"])
        del post["_id"]
        posts.append(post)
    return posts

@app.get("/api/posts/{id}")
async def get_post(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID non valido")
    
    post = await posts_collection.find_one({"_id": ObjectId(id)})
    if post:
        post["id"] = str(post["_id"])
        del post["_id"]
        return post
    raise HTTPException(status_code=404, detail="Post non trovato")