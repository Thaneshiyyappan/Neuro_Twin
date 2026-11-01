import httpx
import numpy as np

OLLAMA_EMBED_URL = "http://localhost:11434/api/embeddings"
EMBED_MODEL = "nomic-embed-text"

async def get_embedding(text: str) -> list[float] | None:
    try:
        async with httpx.AsyncClient(timeout=2.5) as client:
            res = await client.post(
                OLLAMA_EMBED_URL,
                json={"model": EMBED_MODEL, "prompt": text}
            )
            if res.status_code == 200:
                return res.json().get("embedding")
    except Exception:
        pass
    return None

def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    a = np.array(vec_a)
    b = np.array(vec_b)
    norm = np.linalg.norm(a) * np.linalg.norm(b)
    return float(np.dot(a, b) / norm) if norm > 0 else 0.0

def fallback_tag_similarity(tags_a: list[str], tags_b: list[str]) -> float:
    set_a = {t.lower().strip() for t in tags_a}
    set_b = {t.lower().strip() for t in tags_b}
    union = len(set_a | set_b)
    return len(set_a & set_b) / union if union > 0 else 0.0

async def find_related_nodes(new_title: str, new_tags: list[str], existing_nodes: list[dict]) -> list[dict]:
    query_text = f"{new_title}: {', '.join(new_tags)}"
    new_vec = await get_embedding(query_text)
    scored = []

    for node in existing_nodes:
        score = 0.0
        if new_vec and "embedding" in node and node["embedding"]:
            score = cosine_similarity(new_vec, node["embedding"])
        else:
            score = fallback_tag_similarity(new_tags, node.get("tags", []))

        if score > 0.12:
            scored.append({"node": node, "score": round(score, 3)})

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:3]