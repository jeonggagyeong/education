# api/main.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class TextInput(BaseModel):
    text: str

@app.get("/api/hello")
def say_hello():
    return {"message": "Hello from FastAPI"}

@app.post("/api/length")
def get_length(data: TextInput):
    return {"length": len(data.text)}
