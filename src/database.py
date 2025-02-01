from typing import List, Dict

users_db = {
    "user@example.com": {"password": "password123"}  # Example user data
}

graphs_db = {}

def check_user_credentials(email: str, password: str) -> bool:
    return users_db.get(email, {}).get("password") == password

def save_graph(graph_name: str, nodes: List[Dict]) -> bool:
    graphs_db[graph_name] = nodes
    return True