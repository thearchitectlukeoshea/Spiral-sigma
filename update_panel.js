<script>
async function fetchMetrics() {
  const res = await fetch("https://spiral-sigma.onrender.com/metrics/summary");
  const data = await res.json();
  document.getElementById("cpu").innerText = `CPU Load: ${data.cpu}%`;
  document.getElementById("mem").innerText = `Memory: ${data.memory}%`;
}
setInterval(fetchMetrics, 60000);
</script>

<div id="cpu">Loading CPU...</div>
<div id="mem">Loading Mem...</div>
