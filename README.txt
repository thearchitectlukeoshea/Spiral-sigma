
# Flame Relay Backend — v1.0

## Files
- server.py: Flask-based backend server to receive pings and serve logs
- relay_log.json: Stores received logs in JSON format
- update_panel.js: JS snippet to integrate with your frontend panel
- README.txt: Deployment instructions

## Deployment (e.g. Replit)
1. Go to https://replit.com
2. Create a new Repl (Python + Flask)
3. Upload and unzip these files into your Repl
4. Click "Run" to start the server
5. Test POST to /ping and GET from /log

Logs will update every 3 seconds on your panel if using the update_panel.js script.
