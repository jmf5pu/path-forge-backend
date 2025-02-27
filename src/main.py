from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from src.models import Graph, User, Node, UserAuth
from src.database import (
    check_user_credentials, save_graph, get_user, create_user, delete_user,
    create_node, get_all_nodes, delete_node, get_graph
)
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from typing import Optional
import logging
import sys

load_dotenv()

logger = logging.getLogger('uvicorn.error')

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/login")
async def login(email: str, password: str):
    if await check_user_credentials(email, password):
        return {"status": "success", "message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid email or password")

@app.post("/graphs")
async def save_graph_endpoint(graph: Graph):
    try:
        await save_graph(graph.graphName, graph.nodes, graph.edges)
        return JSONResponse(content={"status": "success", "message": "Graph saved successfully"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving graph: {str(e)}")

@app.get("/graphs/{graph_id}")
async def get_graph_endpoint(graph_id: str):
    try:
        graph: Graph = await get_graph(graph_id)
        return JSONResponse(content={"status": "success", "message": "Graph retrieved successfully", "graph": graph.model_dump()},
                            status_code=200)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=404, detail="Graph not found")

@app.post("/users", response_model=Optional[dict])
async def get_profile_endpoint(auth: UserAuth):
    try:
        user = await get_user(auth)
        return JSONResponse(content=user, status_code=200)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=404, detail="User not found")
    
@app.post("/users")
async def create_user_endpoint(user: User):
    await create_user(user)
    return {"status": "success", "message": "User created successfully"}

@app.delete("/users/{email}")
async def delete_user_endpoint(email: str):
    await delete_user(email)
    return {"status": "success", "message": "User deleted successfully"}

@app.post("/nodes")
async def create_node_endpoint(node: Node):
    node_id = await create_node(node)
    return {"status": "success", "message": "Node created successfully", "id": str(node_id)}

@app.get("/nodes")
async def get_nodes_endpoint():
    nodes = await get_all_nodes()
    return {"status": "success", "nodes": nodes}

@app.delete("/nodes/{node_id}")
async def delete_node_endpoint(node_id: str):
    await delete_node(node_id)
    return {"status": "success", "message": "Node deleted successfully"}
