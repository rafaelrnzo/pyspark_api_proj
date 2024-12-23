from fastapi import APIRouter, WebSocket

router = APIRouter(prefix="/ws", tags=["WebSocket"])

@router.websocket("/live-data")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Simulated live data
            data = {"message": "Hello from WebSocket!"}
            await websocket.send_json(data)
    except Exception as e:
        await websocket.close()
