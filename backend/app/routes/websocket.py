import asyncio
from fastapi import APIRouter, WebSocket
from pyspark.sql.functions import expr, col, from_json, avg
from app.schemas.kafka_schema import schema
from app.services.kafka_service import get_kafka_data
from app.utils.helpers import format_response

router = APIRouter(prefix="/ws", tags=["WebSocket"])

@router.websocket("/live-data")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = {"message": "Hello from WebSocket!"}
            await websocket.send_json(data)
            await asyncio.sleep(1)  # Adjust the interval as needed
    except Exception as e:
        await websocket.send_json({"status": "error", "message": str(e)})
    finally:
        await websocket.close()


@router.websocket("/count-data")
async def websocket_count_data(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            cleaned_kafka_df = get_kafka_data()

            streaming_df = cleaned_kafka_df.withColumn(
                "values_json", from_json(col("clean_value"), schema)
            ).selectExpr("values_json.*")

            flattened_df = streaming_df.select(col("fullDocument.OrderCount").alias("order_count"))
            total_count = flattened_df.groupBy().sum("order_count").collect()[0][0] or 0

            await websocket.send_json({"status": "success", "total_order_count": total_count})

            await asyncio.sleep(5)
    except Exception as e:
        await websocket.send_json({"status": "error", "message": str(e)})
    finally:
        await websocket.close()

@router.websocket("/count-standard-cost")
async def websocket_average_cost(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = get_kafka_data()  # Ensure this function is defined and returns a DataFrame

            if data is None or data.isEmpty():  # Check if data is None or empty
                await websocket.send_json({"status": "error", "message": "No data available."})
                await asyncio.sleep(5)
                continue

            streaming_df = data.withColumn(
                "values_json", from_json(col("clean_value"), schema)
            ).selectExpr("values_json.*")

            flattened_df = streaming_df.select(
                col("fullDocument.StandardCost").cast("float").alias("standard_cost")
            )

            avg_standard_cost = flattened_df.agg(avg("standard_cost")).collect()[0][0] or 0

            await websocket.send_json({"status": "success", "average": avg_standard_cost})

            await asyncio.sleep(5)

    except Exception as e:
        await websocket.send_json({"status": "error", "message": str(e)})
    finally:
        await websocket.close()
