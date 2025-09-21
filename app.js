
async function fetchLogs() {
  try {
    const res = await fetch(BACKEND_URL + "/logs");
    const data = await res.json();
    document.getElementById("log-output").innerText = JSON.stringify(data, null, 2);
    document.getElementById("status").innerText = "✅ Logs fetched successfully.";
  } catch (err) {
    document.getElementById("log-output").innerText = "Error loading logs.";
    document.getElementById("status").innerText = "❌ Failed to fetch logs.";
  }
}
