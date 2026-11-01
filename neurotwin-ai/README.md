# 🧠 NEUROTWIN AI // 3D Cognitive Digital Twin & Spatial Second Brain

[![Hacktoberfest 2026](https://img.shields.io/badge/Hacktoberfest-2026-orange?style=for-the-badge)](https://hacktoberfest.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-cyan.svg?style=for-the-badge)](./LICENSE)
[![Three.js](https://img.shields.io/badge/Three.js-r160-black?style=for-the-badge&logo=three.js)](https://threejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Ollama](https://img.shields.io/badge/Ollama-Local_AI-blue?style=for-the-badge)](https://ollama.com/)

> **An open-source 3D spatial knowledge graph and autonomous cognitive replica that maps what you learn, discovers hidden connections between concepts, and tells you what to build next.**

---

## 🚀 The Problem

Traditional note-taking and "second brain" tools (Notion, Obsidian, static flashcards) trap human knowledge in flat 2D text files:
1. **Passive Storage:** They store notes but never actively tell you where your skill bottlenecks are.
2. **Hidden Connections:** As a student or engineer learning across AI, 3D Graphics, and Systems, it is hard to see how a new concept mathematically bridges your existing skills.
3. **Cloud Lock-In:** Most AI assistants rely on paid, closed-source cloud APIs with zero spatial awareness of your personal knowledge graph.

## 💡 The Solution: NeuroTwin AI

**NeuroTwin AI** combines a **60 FPS Three.js WebGL Cognitive Plane**, a **Rigged 3D Self-Avatar**, and **100% Local Open-Source AI (Ollama)** into an interactive command center for your mind:
* **3D Spatial Knowledge Plane:** Every skill, lecture, or project lives as a glowing node in 3D space, clustered by domain with real-time synaptic energy pulses showing connection strength.
* **Automatic Semantic Linker:** Ingest a new thought or topic, and NeuroTwin computes vector embeddings (`nomic-embed-text`) and Cosine Similarity to automatically fire glowing Bezier synapses to related pre-existing concepts.
* **Proactive Executive Twin Directive:** Click **"Consult Digital Twin"** and your central 3D avatar scans your graph for low-connectivity bottlenecks, turns toward the weak node, and speaks a concrete 45-minute action plan aloud via Web Speech API + real-time jaw lip-sync.

---

## 🏗️ System Architecture

```mermaid
graph TD
    subgraph Frontend ["Frontend: Three.js WebGL & Spatial HUD"]
        UI["Glassmorphic HUD Panels"]
        Scene["3D Mind Plane (UnrealBloomPass + CSS2D)"]
        Avatar["3D Self-Avatar Rig (GLB + Lip-Sync)"]
        TTS["Browser Web Speech API"]
    end

    subgraph Backend ["Backend: FastAPI + Persistent Graph Store"]
        API["FastAPI Server (/graph, /ingest, /consult-twin)"]
        DB[("mind_graph.json / Vector Store")]
        Fallback["Zero-Latency Jaccard Fallback"]
    end

    subgraph LocalAI ["Local Open-Source AI Layer (Ollama)"]
        Embed["nomic-embed-text (Vector Embeddings)"]
        LLM["Qwen2.5-3B / Llama-3.2-3B (Twin Reasoning)"]
    end

    UI -->|POST /ingest| API
    UI -->|POST /consult-twin| API
    API <--> DB
    API -->|Compute Cosine Similarity| Embed
    API -->|Offline Safety Net| Fallback
    API -->|Analyze Graph Gaps| LLM
    API -->|3D Coords + Synaptic Links| Scene
    API -->|Directive Text + Target Node| Avatar
    Avatar -->|Voice Synthesis & Jaw Morphs| TTS