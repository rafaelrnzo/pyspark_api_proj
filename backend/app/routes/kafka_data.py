from fastapi import APIRouter
from app.services.kafka_service import get_kafka_data
from app.services.spark_service import parse_and_flatten_kafka_data

router = APIRouter(prefix="/kafka", tags=["Kafka Data"])

@router.get("/all-data")
def get_all_data():
    try:
        kafka_df = get_kafka_data()
        data = parse_and_flatten_kafka_data(kafka_df)
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}
