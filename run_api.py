from pyngrok import ngrok
import uvicorn
import threading

# Start FastAPI app on port 8000 in another thread
def start_server():
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=False)

# Run the server in a thread
server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()

# Create public URL using ngrok
public_url = ngrok.connect(8001)
print(f"\n🚀 Your API is live at: {public_url}\n")
print("📡 Send your mobile requests to this link.\n")

# Keep script alive
input("Press Enter to stop...\n")
