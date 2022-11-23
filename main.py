# python
from typing import Optional
# Pydantic
from pydantic import BaseModel

# FastAPI
from fastapi import FastAPI
from fastapi import Body, Query,Path

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
    name:Optional[str]=Query(
        None,
        min_length=1,
        max_length=50,
        title="Person Name",
        description="This is the person name. It´s between 1 and 50 characters"

        ),
    age:Optional[int]=Query(
        None,gt=0,
        lt=50,
        title="Person Age",
        description="This is the person age"
        )

 ):
    return {name:age}
    
# validaciones path parameters
@app.get("/person/details/{person_id}")
def show_person(
    person_id:int =Path(
        ...,
        gt=0,
        title="this is the person id parameters. Path parameter",
        description="This is the description of the person"
        ),
):
    return {person_id:"It´s exist"}
    
    