import json
import math
import random
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ai.embeddings import find_related_nodes, get_embedding
from ai.twin_agent import generate_twin_directive

app = FastAPI(title="NeuroTwin AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_FILE = Path(__file__).parent / "data" / "mind_graph.json"

def load_graph() -> dict:
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return {"nodes": []}

def save_graph(data: dict):
    DATA_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")

class IngestRequest(BaseModel):
    title: str
    category: str
    tags: list[str]

@app.get("/graph")
async def get_graph():
    return load_graph()

@app.post("/ingest")
async def ingest_concept(req: IngestRequest):
    graph = load_graph()
    nodes = graph["nodes"]

    matches = await find_related_nodes(req.title, req.tags, nodes)

    # Calculate 3D coordinates near matched nodes
    if matches:
        cx = sum(m["node"]["pos"][0] for m in matches) / len(matches)
        cy = sum(m["node"]["pos"][1] for m in matches) / len(matches)
        cz = sum(m["node"]["pos"][2] for m in matches) / len(matches)
        angle = random.uniform(0, math.pi * 2)
        pos = [round(cx + math.cos(angle) * 6.5, 2), round(max(2.5, cy + random.uniform(-1.5, 1.5)), 2), round(cz + math.sin(angle) * 6.5, 2)]
    else:
        pos = [round(random.uniform(-14, 14), 2), round(random.uniform(3, 7), 2), round(random.uniform(-14, 14), 2)]

    vec = await get_embedding(f"{req.title}: {', '.join(req.tags)}")
    new_node = {
        "id": f"n{len(nodes) + 1}",
        "title": req.title,
        "category": req.category,
        "tags": req.tags,
        "mastery": 78,
        "pos": pos,
        "embedding": vec
    }

    nodes.append(new_node)
    save_graph(graph)

    return {
        "node": new_node,
        "links": [{"target_id": m["node"]["id"], "target_title": m["node"]["title"], "score": m["score"]} for m in matches]
    }

@app.post("/consult-twin")
async def consult_twin():
    graph = load_graph()
    return await generate_twin_directive(graph["nodes"])