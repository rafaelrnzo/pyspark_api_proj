from fastapi import APIRouter
from app.services.spark_service import run_analytics

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/summary")
def get_summary():
    try:
        result = run_analytics()
        return {"status": "success", "summary": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}
