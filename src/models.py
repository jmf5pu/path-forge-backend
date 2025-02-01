from pydantic import BaseModel
from typing import List, Dict

class Node(BaseModel):
    id: str
    label: str
    position: Dict[str, float]  # Expecting {'x': float, 'y': float}

class Graph(BaseModel):
    graphName: str
    nodes: List[Node]