from typing import List, Dict
import motor.motor_asyncio
from src.models import Graph, User, Node, Edge, UserAuth
import os
from bson import ObjectId
from dotenv import load_dotenv
from pymongo import ReturnDocument
from datetime import datetime

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_CONN_STR", "mongodb://127.0.0.1:27017")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)

db = client["path-forge"]
users_collection = db["users"]
graphs_collection = db["graphs"]
nodes_collection = db["nodes"]

async def check_user_credentials(email: str, password: str) -> bool:
    user = await users_collection.find_one({"auth.email": email})
    if user:
        return user["auth"]["password"] == password
    return False

async def save_graph(graph_name: str, nodes: List[Node], edges: List[Edge]):
    graph_data = {
        "graphName": graph_name,
        "nodes": [node.model_dump() for node in nodes],  # Convert to dictionaries
        "edges": [edge.model_dump() for edge in edges],  # Convert to dictionaries
    }

    # Insert or update the graph in MongoDB
    result = await graphs_collection.find_one_and_update(
        {"graphName": graph_name},
        {"$set": graph_data},
        upsert=True,  # If the graph doesn't exist, create it
        return_document=ReturnDocument.AFTER,
    )

    return result


def serialize_user(user):
    """Convert ObjectId and datetime to strings for JSON compatibility."""
    if not user:
        return None
    user["_id"] = str(user["_id"]) if "_id" in user else None
    user["graph_id"] = str(user["graph_id"]) if "graph_id" in user else None
    if "start_date" in user and isinstance(user["start_date"], datetime):
        user["start_date"] = user["start_date"].isoformat()
    return user

async def get_user(auth: UserAuth):
    user = await users_collection.find_one({"auth": auth.model_dump()})

    if not user:
        raise Exception("User not found")

    user.pop("auth", None)

    return serialize_user(user)


async def create_user(user: User):
    await users_collection.insert_one(user.model_dump_json())

async def delete_user(email: str):
    await users_collection.delete_one({"email": email})

async def create_node(node: Node):
    result = await nodes_collection.insert_one(node.model_dump_json())
    return result.inserted_id

async def get_all_nodes():
    nodes = await nodes_collection.find().to_list(length=100)

    # store _id as id and remove old member
    for node in nodes:
        node["id"] = str(node["_id"])
        del node["_id"]

    return nodes

async def delete_node(node_id: str):
    await nodes_collection.delete_one({"_id": ObjectId(node_id)})