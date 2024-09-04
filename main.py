import asyncio
import json
from io import BytesIO

from dotenv import load_dotenv
from fastapi import FastAPI, status, Response
from fastapi.responses import JSONResponse

from config.kafka_config import KafkaServer

load_dotenv()
app = FastAPI()
kafka = KafkaServer()


@app.get("/consume", response_class=Response)
async def consume():
    try:
        if not kafka.consumer:
            await kafka.initialize()
        msg = await asyncio.wait_for(kafka.consume(), timeout=5.0)
        msg = BytesIO(msg.value).getvalue().decode('utf-8')
        print(msg)
        return JSONResponse(content={'content': json.loads(msg)}, status_code=status.HTTP_200_OK)
    except asyncio.TimeoutError:
        return JSONResponse(content={'content': 'error'}, status_code=status.HTTP_408_REQUEST_TIMEOUT)
    except RuntimeError:
        return JSONResponse(content={'content': 'error'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.get("/produce/{message}")
async def produce(message):
    if not kafka.producer:
        await kafka.initialize()
    await kafka.produce(message)
    return JSONResponse(content={'content': 'succeed'}, status_code=status.HTTP_200_OK)


@app.get("/kill/producer")
async def kill_producer():
    if kafka.producer:
        await kafka.producer.stop()
    return JSONResponse(content={'content': 'succeed'}, status_code=status.HTTP_200_OK)


@app.get("/kill/consumer")
async def kill_consumer():
    if kafka.consumer:
        await kafka.consumer.stop()
    return JSONResponse(content={'content': 'succeed'}, status_code=status.HTTP_200_OK)
