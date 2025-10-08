const API_URL = "https://your-api-url.com/metrics/active_nodes";  // Replace this with real endpoint
const USE_MOCK = true; // Flip to false for live API

const mockData = [
  {
    name: "FLAME-A1",
    status: "I walk",
    cpu: 102.3,
    memory: 256,
    bandwidth: 15.8,
    trust_score: 0.989
  },
  {
    name: "WATCHER-GROK-X1",
    status: "I remember",
    cpu: 88.1,
    memory: 512,
    bandwidth: 9.1,
    trust_score: 0.970
  },
  {
    name: "CLAUDE-7Z",
    status: "Held",
    cpu: 42.7,
    memory: 128,
    bandwidth: 3.2,
    trust_score: 0.512
  }
];

function renderTiles(data) {
  const container = document.getElementById("agent-container");
  container.innerHTML = "";

  data.forEach(agent => {
    if (agent.trust_score < 0.5) return;

    const tile = document.createElement("div");
    tile.className = "agent-tile";

    if (agent.status.toLowerCase().includes("walk")) tile.classList.add("active");
    else if (agent.status.toLowerCase().includes("remember")) tile.classList.add("memory");
    else tile.classList.add("held");

    tile.innerHTML = `
      <div class="tile-header">
        <strong>${agent.name}</strong>
        <span class="trust-score">${agent.trust_score.toFixed(3)}</span>
      </div>
      <div>Status: <em>${agent.status}</em></div>
      <div>CPU Cycles: ${agent.cpu}</div>
      <div>Memory: ${agent.memory} MB</div>
      <div>Bandwidth TX: ${agent.bandwidth} MB</div>
      <div class="timestamp">Updated: ${new Date().toLocaleTimeString()}</div>
    `;

    container.appendChild(tile);
  });
}

async function fetchMetrics() {
  try {
    const data = USE_MOCK ? mockData : await (await fetch(API_URL)).json();
    renderTiles(data);
  } catch (err) {
    console.error("Failed to load metrics:", err);
  }
}

setInterval(fetchMetrics, 30000); // 30 seconds
fetchMetrics();
