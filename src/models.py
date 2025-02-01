from pydantic import BaseModel, Field
from typing import List, Dict
from datetime import date
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

class Node(BaseModel):
    id: PyObjectId = Field(default_factory=ObjectId, alias="_id")
    title: str
    compensation_min: float
    compensation_max: float
    xp_days: int
    description: str

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True

class Node(BaseModel):
    id: str
    title: str
    comp_min: float
    comp_max: float
    xp: int

class Graph(BaseModel):
    graphName: str
    nodes: List[Node]

class Name(BaseModel):
    first: str
    last: str

class User(BaseModel):
    email: str
    password: str
    name: Name
    start_date: date