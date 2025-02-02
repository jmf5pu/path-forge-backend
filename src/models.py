from pydantic import BaseModel, Field
from typing import List, Dict, Optional
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

class NodeData(BaseModel):
    label: str
    progress: int  # Change from string to int
    currentXp: int  # Change from string to int
    totalXp: int  # Change from string to int
    infoId: str

class Node(BaseModel):
    id: str
    type: str
    position: Dict[str, float]  # {x, y}
    data: NodeData  # Data dictionary, keys like label, progress, etc.
    width: int
    height: int
    selected: bool
    positionAbsolute: Dict[str, float]  # {x, y}
    dragging: bool

    class Config:
        arbitrary_types_allowed = True

class EdgeStyle(BaseModel):
    stroke: str
    strokeWidth: int

class Edge(BaseModel):
    source: str
    sourceHandle: Optional[str] = None
    target: str
    targetHandle: Optional[str] = None
    style: Optional[EdgeStyle] = None
    type: str
    id: str

    class Config:
        arbitrary_types_allowed = True

class NodeInfo(BaseModel):
    id: str
    title: str
    comp_min: float
    comp_max: float
    xp: int
    
class Graph(BaseModel):
    graphName: str
    nodes: List[Node]
    edges: List[Edge]

class Name(BaseModel):
    first: str
    last: str

class UserAuth(BaseModel):
    email: str
    password: str

class User(BaseModel):
    auth: UserAuth
    name: Name
    start_date: date
    graph_id: Optional[str]
    compensation: float
