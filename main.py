# python
from typing import Optional
# Pydantic
from pydantic import BaseModel

# FastAPI
from fastapi import FastAPI
from fastapi import Body, Query

class Person(BaseModel):
    firt_name:str
    last_name:str
    age:int
    hair_color:Optional[str] = None
    is_married:Optional[bool] = None

app=FastAPI()

@app.get("/")
def home():
    return{"helllo":"world"}

@app.post("/person/new")
def create_person(person:Person=Body(...)):
    return person

# validaciones con query parameters

@app.get("/person/detail")
def show_person(
    name:Optional[str]=Query(None,min_length=1,max_length=50),
    age:Optional[int]=Query(None,min_value=1,max_value=100)
 ):
    return {name:age}
    
    