# python
from typing import Optional
from enum import Enum
# Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import IPvAnyAddress
from pydantic import EmailStr



# FastAPI
from fastapi import FastAPI
from fastapi import Body, Query,Path,Form, Cookie, Header, UploadFile, File
from fastapi import status
from fastapi import HTTPException
# models

class HairColor(Enum):
    white="white"
    brown="brown"
    black="black"
    red="red"
    yellow="yellow"
    
class PersonBase(BaseModel):
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
    ip:Optional[IPvAnyAddress]= Field(default=None)
    email:Optional[EmailStr]=Field(default=None)

class Person(PersonBase):
    password:str=Field(..., min_length=8)
    class Config:
        schema_extra = {
            "example": {
                "firt_name": "Eduardo",
                "last_name": "Flores",
                "age": 34,
                "hair_color": HairColor.brown,
                "is_married": False,
                "ip": "127.0.0.1",
                "email":"eduflo1530@gmail.com",
                "password":"12345678"

            }
            }

class PersonOut(PersonBase):
    pass


class Location(BaseModel):
    city:str=Field(
        ...,
        min_length=1,
        max_length=50
    )
    state:Optional[str] = Field(
        ...,
        min_length=1,
        max_length=50

    )
    country:Optional[str]=Field(
        ...,
        min_length=1,
        max_length=50
    )

    class Config:
        schema_extra = {
            "example": {
                "city": "Cali",
                "state": "Valle",
                "country": "Colombia"
            }
            }

class LoginOut(BaseModel):
    username:str=Field(..., max_length=20,example="eduardo2020")
    message:str=Field(default="Login success!!")

app=FastAPI()

# Path operations
@app.get(
    path="/", 
    status_code=status.HTTP_200_OK,
    tags=["Enlaces"],
    summary="Home page"
    )
def home():
    """
    Home
    -This path operations only return and hello world for test proposals:

        -parameters:None
        -return: a message
    """
    
    return{"hello":"world"}

@app.post(
    path="/person/new",
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED,
    tags=["persons"],
    summary="Create person on the app"
    )
def create_person(person:Person=Body(...)):
    """
    Create Person
    
    This path operations create a person in the app and save the information in a database
    Parameters:
    - Request body parameters:
         - **person:Person** -> A person model with fisrt_name, last_name, age, hair color, marital status, ip address, email address, and password
    - Returns:
         - **Person** -> a person model with fisrt_name, last_name, age, hair color, marital status, ip address, email address, and password

    """
    return person

# validaciones con query parameters

@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK,
    tags=["persons"]
    )
def show_person(
    name:Optional[str]=Query(
        None,
        min_length=1,
        max_length=50,
        title="Person Name",
        description="This is the person name. It??s between 1 and 50 characters",
        example="Eduardo"
        ),
    age:Optional[int]=Query(
        None,gt=0,
        lt=50,
        title="Person Age",
        description="This is the person age",
        example=34
        )
 ):
    """
    Person Details.

    This path operations show the details of and person

    Parameters:
    - Request path parameters:
    - Return: two parameters: name and age

    """
    return {name:age}
    
persons=[1,2,3,4,5]
# validaciones path parameters
@app.get(
    path="/person/details/{person_id}",
    tags=["persons"]
    )
def show_person(
    person_id:int =Path(
        ...,
        gt=0,
        title="this is the person id parameters. Path parameter",
        description="This is the description of the person",
        example=1
        ),
):
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This person does not exist"
        )
    return {person_id:"It??s exist"}
    
    
# validaciones body parameters

@app.put(
    path="/person/{person_id}",
    tags=["persons"],
    deprecated=True
    )
def update_person(
    person_id:int =Path(
       ...,
        gt=0,   
        title="this is the person id parameters. Path parameter",
        description="this is the description of the person",
        example=4

),
    person:Person=Body(...),
    location:Location=Body(...)
):
    results=person.dict()
    results.update(location.dict())
    return results

    
@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
    tags=["persons"]
    )

def login(
    username:str=Form(...),
    password:str=Form(...)
):
    return LoginOut(username=username)

# cookies and headers parameters.

@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK,
    tags=["Enlaces"]

)
def contact(
    firt_name:str=Form(
        ...,
        max_length=20,
        min_length=1
        ),
    lastname:str=Form(
        ..., 
        max_length=20,
        min_length=1
        ),
    email:EmailStr=Form(...),
    message:str=Form(
        ...,
        min_length=20,
    ),
    user_agent:Optional[str]=Header(default=None),
    ads:Optional[str]=Cookie(default=None)
):
    return user_agent

# files

@app.post(
    path="/post-image",
    tags=["Enlaces"]
)
def post_image(
    image:UploadFile=File(...)
):
    return {
        "Filename":image.filename,
        "format":image.content_type,
        "Size(kb)":round(len(image.file.read())/1024,ndigits=2)
    }
