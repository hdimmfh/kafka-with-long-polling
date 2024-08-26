import asyncio
from io import BytesIO

from dotenv import load_dotenv
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from config.kafka_config import KafkaServer

load_dotenv()
app = FastAPI()
kafka = KafkaServer()


@app.get("/consume")
async def consume():
    try:
        if not kafka.consumer:
            await kafka.initialize()
        msg = await asyncio.wait_for(kafka.consume(), timeout=5.0)
        msg = BytesIO(msg.value).getvalue().decode('utf-8')
        return JSONResponse(content={'content': msg}, status_code=status.HTTP_200_OK)
    except asyncio.TimeoutError as e:
        return JSONResponse(content={'content': 'no content'}, status_code=status.HTTP_204_NO_CONTENT)


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
