from fastapi import FastAPI
from app.routes import websocket, kafka_data, analytics  # Adjust based on your folder structure
from app.middleware.setup_cors import setup_cors

app = FastAPI()

setup_cors(app)

app.include_router(kafka_data.router)
app.include_router(websocket.router)
app.include_router(analytics.router)

@app.get("/")
def root():
    return {"message": "Application is running successfully!"}