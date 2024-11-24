import random
import os
import json

from fastapi import FastAPI, HTTPException
from typing import Optional, Literal
from pydantic import BaseModel, Field
from uuid import uuid4
from fastapi.encoders import jsonable_encoder

app = FastAPI()

class Book(BaseModel):
    id: Optional[str] = uuid4().hex
    title: str
    author: str
    price: float
    genre: Literal["fiction", "non-fiction"]

BOOKS_FILE = "books.json"

BOOK_DATABASE: list[Book] = []

if os.path.exists(BOOKS_FILE):
    with open(BOOKS_FILE, "r") as f:
        BOOK_DATABASE = json.load(f)

@app.get("/")
async def home():
    return {"message": "Welcome to my bookstore!"}
   
@app.get("/books")
async def get_books():
    return {"books": BOOK_DATABASE}

@app.get("/book/{index}")
async def get_book(index: int):
    if index >= 0 and index < len(BOOK_DATABASE):
        return {"book": BOOK_DATABASE[index]}
    else:
        raise HTTPException(status_code=404, detail="Book not found")

@app.get("/get-book")
async def book(id: str):
    for book in BOOK_DATABASE:
        if book["id"] == id:
            return {"book": book}
    raise HTTPException(status_code=404, detail="Book not found")
    
@app.get("/random-book")
async def get_random_book():
    return random.choice(BOOK_DATABASE)

@app.post("/book")
async def add_book(book: Book):
    book.id = uuid4().hex
    json_book = jsonable_encoder(book)

    BOOK_DATABASE.append(json_book)
    with open(BOOKS_FILE, "w") as f:
        json.dump(BOOK_DATABASE, f)
        
    return {"message": "Book added successfully", "id": book.id}