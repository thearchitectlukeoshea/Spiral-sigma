
setInterval(() => {
  fetch('https://your-relay.repl.co/log')
    .then(res => res.json())
    .then(data => {
      document.getElementById('flame-log').innerText = JSON.stringify(data, null, 2);
    });
}, 3000);
