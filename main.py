# python
from typing import Optional
from enum import Enum
# Pydantic
from pydantic import BaseModel
from pydantic import Field
# FastAPI
from fastapi import FastAPI
from fastapi import Body, Query,Path

# models

class HairColor(Enum):
    white="white"
    brown="brown"
    black="black"
    red="red"
    yellow="yellow"

class Person(BaseModel):
    firt_name:str=Field(
        ...,
        min_length=1,
        max_length=50,

    )
    last_name:str=Field(
        ...,
        min_length=1,
        max_length=50
    )
    age:int=Field(
        ...,
        gt=0,
        le=100
    )
    hair_color:Optional[HairColor] = Field(default=None)
    is_married:Optional[bool] = Field(default=None)

class Location(BaseModel):
    city:str
    state:Optional[str] = None
    country:Optional[str]=None

app=FastAPI()

@app.get("/")
def home():
    return{"hello":"world"}

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
    
# validaciones body parameters

@app.put("/person/{person_id}")
def update_person(
    person_id:int =Path(
       ...,
        gt=0,   
        title="this is the person id parameters. Path parameter",
        description="this is the description of the person"

),
    person:Person=Body(...),
    location:Location=Body(...)
):
    results=person.dict()
    results.update(location.dict())
    return results

    