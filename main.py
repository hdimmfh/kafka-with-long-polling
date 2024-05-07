import asyncio

from dotenv import load_dotenv
from fastapi import FastAPI

from config.kafka_config import KafkaServer
from config.log_config import log_config

load_dotenv()
app = FastAPI()
log = log_config()
kafka = KafkaServer(log)


@app.get("/ping")
async def root():
    return "pong"


@app.get("/initialize")
async def initialize():
    await kafka.initialize()
    return 200


@app.get("/send/{message}")
async def send(message):
    if not kafka.producer:
        log.info("kafka is not initialized now initializing..")
        await kafka.initialize()
    await kafka.send(message)
    return 200


@app.get("/get")
async def get():
    try:
        if not kafka.consumer:
            log.info("kafka is not initialized now initializing..")
            await kafka.initialize()
        msg = await asyncio.wait_for(kafka.get(), timeout=5.0)
        print(msg)
        return 200
    except asyncio.TimeoutError as e:
        log.error("asyncio timeout error")
        return 500


@app.get("kill_producer")
async def kill_producer():
    if kafka.producer:
        await kafka.producer.stop()
    return 200


@app.get("kill_consumer")
async def kill_consumer():
    if kafka.consumer:
        await kafka.consumer.stop()
    return 200
