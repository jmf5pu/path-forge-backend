from typing import List, Dict
import motor.motor_asyncio
from src.models import Graph, User, Node
import os
from bson import ObjectId
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_CONN_STR", "mongodb://127.0.0.1:27017")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)

db = client["path-forge"]
users_collection = db["users"]
graphs_collection = db["graphs"]
nodes_collection = db["nodes"]

async def check_user_credentials(email: str, password: str) -> bool:
    user = await users_collection.find_one({"email": email})
    if user:
        return user["password"] == password
    return False

async def save_graph(graph_name: str, nodes: List[Dict]) -> bool:
    graph_data = {"graphName": graph_name, "nodes": nodes}
    result = await graphs_collection.replace_one(
        {"graphName": graph_name}, graph_data, upsert=True
    )
    return result.modified_count > 0 or result.upserted_id is not None

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