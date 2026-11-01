const API_BASE = 'http://localhost:8000';

export const ApiClient = {
    async fetchGraph() {
        const res = await fetch(`${API_BASE}/graph`);
        return res.json();
    },
    async ingestConcept(title, category, tags) {
        const res = await fetch(`${API_BASE}/ingest`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title, category, tags })
        });
        return res.json();
    },
    async consultTwin() {
        const res = await fetch(`${API_BASE}/consult-twin`, { method: 'POST' });
        return res.json();
    }
};