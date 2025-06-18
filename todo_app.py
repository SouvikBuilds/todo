from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from typing import Literal
import certifi

# MONGO_URL = "mongodb+srv://SouvikBuilds:souvik1234@cluster0.r5l5h1i.mongodb.net/TodoCollection?retryWrites=true&w=majority"
client = MongoClient(
    "mongodb+srv://SouvikBuilds:souvik1234@cluster0.r5l5h1i.mongodb.net/TodoCollection?retryWrites=true&w=majority",
    tls=True,
    tlsCAFile= certifi.where()
)
db = client["TodoCollection"]
collection = db["user"]

app = FastAPI()
class TodoModel(BaseModel):
    title: str
    description: str
    status: Literal["C","NC"]
    datestamp: str
    id: str

@app.post("/add_works")

def add_works(works: TodoModel):
    if collection.find_one({"id": works.id}):
        raise HTTPException(status_code= 400 , detail= "Task Id Already exist")
    
    collection.insert_one({
        "title": works.title,
        "Description": works.description,
        "Status": works.status,
        "DateStamp": works.datestamp,
        "id": works.id
        
    })
    
    return {"Message": f"Task with {works.id} Added Successfully"}

@app.get("/works")

def view_works():
    
    works = list(collection.find({},{"_id": 0}))
    
    return {"tasks": works}

@app.delete("/works/{id}")

def delete_work(id: str):
    
    result = collection.delete_one({"id": id})
    if result.deleted_count == 0:
        raise HTTPException(status_code= 404, detail= "Task Not Found")
    
    return {"Message": f"Task with id {id} deleted Successfully"}

@app.put("/works/{id}")
def update_works(id: str, works: TodoModel):
    result = collection.update_one(
        {"id": id },
        {"$set": {
            "title": works.title,
            "desription": works.description,
            "status": works.status,
            "datestamp": works.datestamp
        }}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="work not found")
    return {"message": "work updated successfully"}
    

    

    
    