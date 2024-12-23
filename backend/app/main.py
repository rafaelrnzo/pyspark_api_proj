from fastapi import FastAPI
from app.middleware import setup_cors
from app.routes import kafka_data, websocket, analytics

app = FastAPI()

# Middleware setup
setup_cors(app)

# Include routers
app.include_router(kafka_data.router)
app.include_router(websocket.router)
app.include_router(analytics.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
