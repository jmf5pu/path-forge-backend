from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from models import Graph
from database import check_user_credentials, save_graph

app = FastAPI()

@app.get("/login")
async def login(email: str, password: str):
    if check_user_credentials(email, password):
        return {"status": "success", "message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid email or password")

@app.post("/saveGraph")
async def save_graph_endpoint(graph: Graph):
    try:
        save_graph(graph.graphName, graph.nodes)
        return JSONResponse(content={"status": "success", "message": "Graph saved successfully"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving graph: {str(e)}")
