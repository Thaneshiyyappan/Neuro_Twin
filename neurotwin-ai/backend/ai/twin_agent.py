import httpx

OLLAMA_GEN_URL = "http://localhost:11434/api/generate"
LLM_MODEL = "qwen2.5:3b"

async def generate_twin_directive(nodes: list[dict]) -> dict:
    # Identify the lowest-mastery bottleneck node
    weakest = min(nodes, key=lambda n: n.get("mastery", 75))
    strongest = max(nodes, key=lambda n: n.get("mastery", 75))

    prompt = (
        f"You are Thanesh's 3D Cognitive Digital Twin (a B.Tech AI & Data Science developer skilled in Three.js and Blender). "
        f"His strongest concept node is '{strongest['title']}' ({strongest['mastery']}% mastery), "
        f"but his weakest bottleneck node is '{weakest['title']}' ({weakest['mastery']}% mastery). "
        f"In 2 punchy sentences, speak directly to Thanesh and prescribe one concrete 45-minute coding task "
        f"that connects '{weakest['title']}' to '{strongest['title']}'."
    )

    try:
        async with httpx.AsyncClient(timeout=6.0) as client:
            res = await client.post(
                OLLAMA_GEN_URL,
                json={"model": LLM_MODEL, "prompt": prompt, "stream": False}
            )
            if res.status_code == 200:
                reply = res.json().get("response", "").strip()
                if reply:
                    return {"directive": reply, "weak_node_id": weakest["id"], "weak_node": weakest}
    except Exception:
        pass

    # Instant offline fallback if Ollama is closed
    fallback_text = (
        f"Thanesh, your {strongest['title']} cluster is operating at peak synergy, "
        f"but {weakest['title']} is lagging at {weakest['mastery']}% mastery. "
        f"Spend the next 45 minutes wiring a live data route between {weakest['title']} and your 3D Three.js scene."
    )
    return {"directive": fallback_text, "weak_node_id": weakest["id"], "weak_node": weakest}